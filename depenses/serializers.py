from rest_framework import serializers
from .models import Depense


class DepenseSerializer(serializers.ModelSerializer):
    montant_ttc = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Depense
        fields = ['id', 'fournisseur', 'description', 'categorie', 'montant_ht',
                   'taux_tva', 'montant_ttc', 'date_depense', 'statut_validation']