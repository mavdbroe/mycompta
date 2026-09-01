from django.contrib import admin
from .models import Depense

@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ('fournisseur', 'description', 'categorie', 'date_depense', 'montant_ttc')
    list_filter = ('categorie',)