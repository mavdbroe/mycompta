from django.contrib import admin, messages
from .models import LigneReleve

@admin.register(LigneReleve)
class LigneReleveAdmin(admin.ModelAdmin):
    list_display = ('date_operation', 'montant', 'communication', 'facture', 'rapprochee')
    list_filter = ('rapprochee',)
    actions = ['action_marquer_rapprochee']

    @admin.action(description="Marquer comme rapprochée et la facture liée comme payée")
    def action_marquer_rapprochee(self, request, queryset):
        if not request.user.has_perm('banque.change_lignereleve'):
            self.message_user(request, "Vous n'avez pas la permission d'effectuer cette action.", level=messages.ERROR)
            return
        nb = 0
        for ligne in queryset:
            ligne.rapprochee = True
            ligne.save()
            if ligne.facture:
                ligne.facture.statut = 'payee'
                ligne.facture.save()
            nb += 1
        self.message_user(request, f"{nb} ligne(s) traitée(s).", level=messages.SUCCESS)