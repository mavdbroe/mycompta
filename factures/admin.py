from django.contrib import admin
from .models import Facture, LigneFacture

class LigneFactureInline(admin.TabularInline):
    model = LigneFacture
    extra = 1

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero', 'client', 'date_emission', 'statut', 'total_ttc')
    inlines = [LigneFactureInline]