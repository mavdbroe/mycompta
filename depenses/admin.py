from django.contrib import admin, messages
from .models import Depense
from comptabilite.services import generer_ecritures_depense

@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ('fournisseur', 'description', 'categorie', 'date_depense', 'montant_ttc')
    list_filter = ('categorie',)
    actions = ['action_generer_ecritures']

    @admin.action(description="Générer les écritures comptables")
    def action_generer_ecritures(self, request, queryset):
        if not request.user.has_perm('depenses.change_depense'):
                    self.message_user(request, "Vous n'avez pas la permission d'effectuer cette action.", level=messages.ERROR)
                    return
        succes = 0
        for depense in queryset:
            ok, message = generer_ecritures_depense(depense)
            if ok:
                succes += 1
            else:
                self.message_user(request, f"{depense.fournisseur} : {message}", level=messages.WARNING)
        if succes:
            self.message_user(request, f"{succes} dépense(s) traitée(s) avec succès.", level=messages.SUCCESS)