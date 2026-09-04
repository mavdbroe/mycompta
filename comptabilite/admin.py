from django.utils import timezone
from django.contrib import admin, messages
from .models import CompteComptable, EcritureComptable, ExerciceComptable
from django.db.models import Sum
from django.core.exceptions import ValidationError

@admin.register(CompteComptable)
class CompteComptableAdmin(admin.ModelAdmin):
    list_display = ('numero', 'nom', 'type_compte')
    list_filter = ('type_compte',)

@admin.register(EcritureComptable)
class EcritureComptableAdmin(admin.ModelAdmin):
    list_display = ('date_ecriture', 'libelle', 'compte_debit', 'compte_credit', 'montant')
    list_filter = ('date_ecriture',)

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
        except ValidationError as e:
            form.add_error(None, e)
            return
        super().save_model(request, obj, form, change)

@admin.register(ExerciceComptable)
class ExerciceComptableAdmin(admin.ModelAdmin):
    list_display = ('annee', 'date_debut', 'date_fin', 'cloture', 'date_cloture')
    actions = ['action_cloturer']

    @admin.action(description="Clôturer l'exercice sélectionné")
    def action_cloturer(self, request, queryset):
        nb = 0
        for exercice in queryset:
            if exercice.cloture:
                self.message_user(request, f"Exercice {exercice.annee} déjà clôturé.", level=messages.WARNING)
                continue
            exercice.cloture = True
            exercice.date_cloture = timezone.now()
            exercice.save()
            nb += 1
        if nb:
            self.message_user(request, f"{nb} exercice(s) clôturé(s).", level=messages.SUCCESS)