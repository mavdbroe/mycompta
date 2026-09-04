from django import forms
from .models import Depense


class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = ['fournisseur', 'description', 'categorie', 'montant_ht', 'taux_tva', 'date_depense', 'justificatif']
        widgets = {
            'date_depense': forms.DateInput(attrs={'type': 'date'}),
        }