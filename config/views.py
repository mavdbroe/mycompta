from django.shortcuts import render
from django.db.models import Sum
from datetime import date
from factures.models import Facture
from depenses.models import Depense


def tableau_de_bord(request):
    factures_impayees = Facture.objects.exclude(statut__in=['payee', 'annulee'])
    factures_en_retard = [f for f in factures_impayees if f.est_en_retard]

    total_a_recevoir = sum(f.total_ttc for f in factures_impayees)

    aujourd_hui = date.today()
    depenses_mois = Depense.objects.filter(
        date_depense__year=aujourd_hui.year,
        date_depense__month=aujourd_hui.month,
    )
    total_depenses_mois = depenses_mois.aggregate(total=Sum('montant_ht'))['total'] or 0

    return render(request, 'tableau_de_bord.html', {
        'factures_impayees': factures_impayees,
        'factures_en_retard': factures_en_retard,
        'total_a_recevoir': total_a_recevoir,
        'total_depenses_mois': total_depenses_mois,
        'nb_depenses_mois': depenses_mois.count(),
    })

def documents(request):
    factures = Facture.objects.all().order_by('-date_emission')
    depenses_avec_justificatif = Depense.objects.exclude(justificatif='').order_by('-date_depense')
    depenses_sans_justificatif = Depense.objects.filter(justificatif='').order_by('-date_depense')

    return render(request, 'documents.html', {
        'factures': factures,
        'depenses_avec_justificatif': depenses_avec_justificatif,
        'depenses_sans_justificatif': depenses_sans_justificatif,
    })