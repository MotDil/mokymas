from django.shortcuts import render
from .models import Paslauga, Uzsakymas, AutomobilisKlientas

# Create your views here.

def index(request):
    statistika = {
        'sk_paslauga': Paslauga.objects.count(),
        'sk_uzsakymas': Uzsakymas.objects.filter(statusas__exact='A').count(),
        'sk_automobiliskliento': AutomobilisKlientas.objects.count(),
    }
    return render(request, 'index.html', context=statistika)