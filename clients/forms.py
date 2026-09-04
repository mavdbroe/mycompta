from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'numero_entreprise', 'email', 'telephone', 'adresse', 'ville', 'code_postal', 'pays']