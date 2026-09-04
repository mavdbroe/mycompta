from rest_framework import serializers
from .models import Facture, LigneFacture


class LigneFactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LigneFacture
        fields = ['id', 'description', 'quantite', 'prix_unitaire_ht', 'taux_tva', 'total_ht']


class FactureSerializer(serializers.ModelSerializer):
    lignes = LigneFactureSerializer(many=True, read_only=True)
    client_nom = serializers.CharField(source='client.nom', read_only=True)
    total_ht = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_tva = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_ttc = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Facture
        fields = ['id', 'numero', 'client', 'client_nom', 'date_emission', 'date_echeance',
                   'statut', 'lignes', 'total_ht', 'total_tva', 'total_ttc']