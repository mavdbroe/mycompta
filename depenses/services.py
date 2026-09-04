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