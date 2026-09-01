from django.shortcuts import render
from django.db.models import Sum
from .models import CompteComptable
from django.contrib.auth.decorators import login_required

@login_required
def balance_comptes(request):
    comptes = CompteComptable.objects.all()
    lignes = []
    total_debit = 0
    total_credit = 0

    for compte in comptes:
        debit = compte.ecritures_debit.aggregate(total=Sum('montant'))['total'] or 0
        credit = compte.ecritures_credit.aggregate(total=Sum('montant'))['total'] or 0
        solde = debit - credit

        if debit or credit:
            lignes.append({
                'compte': compte,
                'debit': debit,
                'credit': credit,
                'solde': solde,
            })
            total_debit += debit
            total_credit += credit

    return render(request, 'comptabilite/balance.html', {
        'lignes': lignes,
        'total_debit': total_debit,
        'total_credit': total_credit,
        'total_solde': total_debit - total_credit,
    })


from datetime import date
from django.db.models import Sum
from .models import CompteComptable, EcritureComptable

COMPTE_TVA_COLLECTEE = '451000'
COMPTE_TVA_DEDUCTIBLE = '411100'

@login_required
def rapport_tva(request):
    aujourd_hui = date.today()
    date_debut = request.GET.get('date_debut', date(aujourd_hui.year, aujourd_hui.month, 1).isoformat())
    date_fin = request.GET.get('date_fin', aujourd_hui.isoformat())

    ecritures_periode = EcritureComptable.objects.filter(
        date_ecriture__gte=date_debut,
        date_ecriture__lte=date_fin,
    )

    tva_collectee = ecritures_periode.filter(
        compte_credit__numero=COMPTE_TVA_COLLECTEE
    ).aggregate(total=Sum('montant'))['total'] or 0

    tva_deductible = ecritures_periode.filter(
        compte_debit__numero=COMPTE_TVA_DEDUCTIBLE
    ).aggregate(total=Sum('montant'))['total'] or 0

    tva_a_payer = tva_collectee - tva_deductible

    return render(request, 'comptabilite/rapport_tva.html', {
        'date_debut': date_debut,
        'date_fin': date_fin,
        'tva_collectee': tva_collectee,
        'tva_deductible': tva_deductible,
        'tva_a_payer': tva_a_payer,
    })