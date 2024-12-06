from .models import Komentaras
from django import forms

class KomentarasForm(forms.ModelForm):
    class Meta:
        model = Komentaras
        fields = ('uzsakymaskom', 'vartotojas', 'turinys',)
        widgets = {'uzsakymaskom': forms.HiddenInput(), 'vartotojas': forms.HiddenInput()}