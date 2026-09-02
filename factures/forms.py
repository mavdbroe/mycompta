from django import forms
from django.forms import inlineformset_factory
from .models import Facture, LigneFacture


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['client', 'numero', 'date_emission', 'date_echeance', 'statut', 'notes']
        widgets = {
            'date_emission': forms.DateInput(attrs={'type': 'date'}),
            'date_echeance': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


LigneFactureFormSet = inlineformset_factory(
    Facture,
    LigneFacture,
    fields=['description', 'quantite', 'prix_unitaire_ht', 'taux_tva'],
    extra=3,
    can_delete=True,
)