from .models import EnveloppePaiement
from django.utils import timezone

def valider_depense(depense, utilisateur):
    depense.statut_validation = 'validee'
    depense.validee_par = utilisateur
    depense.date_validation = timezone.now()
    depense.save()


def demander_correction(depense, utilisateur, commentaire):
    depense.statut_validation = 'a_corriger'
    depense.commentaire_comptable = commentaire
    depense.validee_par = utilisateur
    depense.date_validation = timezone.now()
    depense.save()

def creer_enveloppe(depenses_ids):
    enveloppe = EnveloppePaiement.objects.create()
    depenses = []
    for depense_id in depenses_ids:
        from .models import Depense
        depense = Depense.objects.get(id=depense_id)
        depense.enveloppe = enveloppe
        depense.save()
        depenses.append(depense)
    return enveloppe


def marquer_envoyee(enveloppe):
    enveloppe.statut = 'envoyee'
    enveloppe.date_envoi = timezone.now()
    enveloppe.save()
    for depense in enveloppe.depenses.all():
        depense.date_paiement = timezone.now().date()
        depense.save()