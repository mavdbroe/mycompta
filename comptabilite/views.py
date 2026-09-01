from django.shortcuts import render
from django.db.models import Sum
from .models import CompteComptable


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