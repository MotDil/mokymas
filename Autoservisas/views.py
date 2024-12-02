from lib2to3.fixes.fix_input import context

from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Paslauga, Uzsakymas, AutomobilisKlientas, AutomobilioModelis, UzsakymoEilute


# Index view for displaying statistics
def index(request):
    statistika = {
        'sk_paslauga': Paslauga.objects.count(),
        'sk_uzsakymas': Uzsakymas.objects.filter(statusas__exact='A').count(),
        'sk_automobiliskliento': AutomobilisKlientas.objects.count(),
    }
    return render(request, 'index.html', context=statistika)

def automobiliu_sarasas(request):
    automobiliai =AutomobilioModelis.objects.all()
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
    template_name = 'uzsakymas_list.html'

class UzsakymasDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = 'uzsakymas_detail.html'
    context_object_name = 'detalus'

    def get_context_data(self, **kwargs):
        context = super(UzsakymasDetailView, self).get_context_data(**kwargs)
        context['eilutes'] = self.object.uzsakymoeilute_set.all
        return context





