from .models import Komentaras
from django import forms

class KomentarasForm(forms.ModelForm):
    class Meta:
        model = Komentaras
        fields = ('uzsakymas_komentaras', 'vartotojas', 'turinys',)
        widgets = {'uzsakymas_komentaras': forms.HiddenInput(), 'vartotojas': forms.HiddenInput()}