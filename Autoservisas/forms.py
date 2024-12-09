from django.contrib.auth.models import User

from .models import Komentaras, Profilis
from django import forms

class KomentarasForm(forms.ModelForm):
    class Meta:
        model = Komentaras
        fields = ('uzsakymaskom', 'vartotojas', 'turinys',)
        widgets = {'uzsakymaskom': forms.HiddenInput(), 'vartotojas': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']