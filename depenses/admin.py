from django.contrib import admin, messages
from .models import Depense
from comptabilite.services import generer_ecritures_depense
from .services import valider_depense

@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ('fournisseur', 'description', 'categorie', 'date_depense', 'montant_ttc', 'statut_validation')
    list_filter = ('categorie', 'statut_validation')
    actions = ['action_generer_ecritures', 'action_valider']

    @admin.action(description="Générer les écritures comptables")
    def action_generer_ecritures(self, request, queryset):
        succes = 0
        for depense in queryset:
            if depense.statut_validation != 'validee':
                self.message_user(request, f"{depense.fournisseur} : dépense non validée, écritures non générées.", level=messages.WARNING)
                continue
            ok, message = generer_ecritures_depense(depense)
            if ok:
                succes += 1
            else:
                self.message_user(request, f"{depense.fournisseur} : {message}", level=messages.WARNING)
        if succes:
            self.message_user(request, f"{succes} dépense(s) traitée(s) avec succès.", level=messages.SUCCESS)

    @admin.action(description="Valider les dépenses sélectionnées")
    def action_valider(self, request, queryset):
        if not request.user.has_perm('depenses.change_depense'):
            self.message_user(request, "Vous n'avez pas la permission d'effectuer cette action.", level=messages.ERROR)
            return
        nb = 0
        for depense in queryset:
            valider_depense(depense, request.user)
            nb += 1
        self.message_user(request, f"{nb} dépense(s) validée(s).", level=messages.SUCCESS)