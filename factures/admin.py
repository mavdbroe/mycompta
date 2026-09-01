from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from .models import Facture, LigneFacture
from comptabilite.services import generer_ecritures_facture

class LigneFactureInline(admin.TabularInline):
    model = LigneFacture
    extra = 1

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero', 'client', 'date_emission', 'statut', 'total_ttc', 'voir_pdf')
    inlines = [LigneFactureInline]
    actions = ['action_generer_ecritures']

    def voir_pdf(self, obj):
        url = reverse('facture_pdf', args=[obj.id])
        return format_html('<a href="{}" target="_blank">Voir PDF</a>', url)
    voir_pdf.short_description = 'PDF'

    @admin.action(description="Générer les écritures comptables")
    def action_generer_ecritures(self, request, queryset):
        succes = 0
        for facture in queryset:
            ok, message = generer_ecritures_facture(facture)
            if ok:
                succes += 1
            else:
                self.message_user(request, f"{facture.numero} : {message}", level=messages.WARNING)
        if succes:
            self.message_user(request, f"{succes} facture(s) traitée(s) avec succès.", level=messages.SUCCESS)