from django.contrib import admin
from .models import CompteComptable, EcritureComptable

@admin.register(CompteComptable)
class CompteComptableAdmin(admin.ModelAdmin):
    list_display = ('numero', 'nom', 'type_compte')
    list_filter = ('type_compte',)

@admin.register(EcritureComptable)
class EcritureComptableAdmin(admin.ModelAdmin):
    list_display = ('date_ecriture', 'libelle', 'compte_debit', 'compte_credit', 'montant')
    list_filter = ('date_ecriture',)