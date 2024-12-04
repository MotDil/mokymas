from lib2to3.fixes.fix_input import context

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Paslauga, Uzsakymas, AutomobilisKlientas, AutomobilioModelis, UzsakymoEilute

def index(request):
    statistika = {
        'sk_paslauga': Paslauga.objects.count(),
        'sk_uzsakymas': Uzsakymas.objects.filter(statusas__exact='A').count(),
        'sk_automobiliskliento': AutomobilisKlientas.objects.count(),
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

class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymas_detail.html'
    context_object_name = 'detalus'

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





