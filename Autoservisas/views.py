from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin

from .forms import KomentarasForm, UserUpdateForm, ProfilisUpdateForm
from .models import Paslauga, Uzsakymas, AutomobilisKlientas, AutomobilioModelis, UzsakymoEilute, Komentaras


def index(request):
    sk_apsilankymai = request.session.get('sk_apsilankymai', 0)
    request.session['sk_apsilankymai'] = sk_apsilankymai + 1

    statistika = {
        'sk_paslauga': Paslauga.objects.count(),
        'sk_uzsakymas': Uzsakymas.objects.filter(statusas__exact='A').count(),
        'sk_automobiliskliento': AutomobilisKlientas.objects.count(),
        'sk_apsilankymai': sk_apsilankymai + 1
    }
    return render(request, 'index.html', context=statistika)

def automobiliu_sarasas(request):
    paginator = Paginator(AutomobilioModelis.objects.all(), 2)
    page_number = request.GET.get('page')
    automobiliai = paginator.get_page(page_number)
    # automobiliai =AutomobilioModelis.objects.all()
    return render(request, 'automobiliai.html', {'automobiliai': automobiliai})

def automobilis_klientai(request, modelis_id):
    modelis = get_object_or_404(AutomobilioModelis, pk=modelis_id)
    klientai = AutomobilisKlientas.objects.filter(modelis=modelis)
    sarasas = {
        'modelis': modelis,
        'klientai': klientai,
    }
    return render(request, 'automobilis_klientai.html', context=sarasas)


class UzsakymaiListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 3
    template_name = 'uzsakymas_list.html'

class UzsakymasDetailView(FormMixin, generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymas_detail.html'
    context_object_name = 'detalus'
    form_class = KomentarasForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse('uzsakymas_detail', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.uzsakymaskom = self.object
        form.instance.vartotojas = self.request.user
        form.save()
        return super(UzsakymasDetailView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(UzsakymasDetailView, self).get_context_data(**kwargs)
        context['eilutes'] = self.object.uzsakymoeilute_set.all
        return context

def search(request):

    query = request.GET.get('query')
    search_results = AutomobilisKlientas.objects.filter(
        Q(klientas__icontains=query) |
        Q(modelis__marke__icontains=query) |
        Q(modelis__modelis__icontains=query) |
        Q(valstybinis_nr__icontains=query) |
        Q(vin_kodas__icontains=query)
    )
    return render(request, 'search.html', {'automobiliai': search_results, 'query': query})



class ServiceByUserListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas
    template_name = 'user_autoservisas.html'
    context_object_name = 'uzsakymai'
    paginate_by = 10

    def get_queryset(self):
        return Uzsakymas.objects.filter(klientas=self.request.user).order_by('grazinimo_terminas')


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'register.html')


@login_required
def profilis(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profilis')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profilis.html', context)