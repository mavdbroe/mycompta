import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import EnveloppePaiement
from .services import creer_enveloppe, marquer_envoyee
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DepenseForm
from .models import Depense


@permission_required('depenses.add_depense', login_url='/accounts/login/')
def depense_creer(request):
    if request.method == 'POST':
        form = DepenseForm(request.POST, request.FILES)
        if form.is_valid():
            depense = form.save()
            messages.success(request, f"Dépense chez {depense.fournisseur} créée avec succès.")
            return redirect('depenses_liste')
        else:
            messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form = DepenseForm()

    return render(request, 'depenses/depense_form.html', {'form': form})


def depenses_liste(request):
    depenses = Depense.objects.all().order_by('-date_depense')
    return render(request, 'depenses/depenses_liste.html', {'depenses': depenses})


@permission_required('depenses.change_depense', login_url='/accounts/login/')
def enveloppes_liste(request):
    if request.method == 'POST':
        depenses_ids = request.POST.getlist('depenses')
        if depenses_ids:
            enveloppe = creer_enveloppe(depenses_ids)
            messages.success(request, f"Enveloppe #{enveloppe.id} créée avec {len(depenses_ids)} dépense(s).")
        else:
            messages.error(request, "Sélectionne au moins une dépense.")
        return redirect('enveloppes_liste')

    depenses_a_payer = Depense.objects.filter(
        statut_validation='validee',
        enveloppe__isnull=True,
        date_paiement__isnull=True,
    )
    enveloppes = EnveloppePaiement.objects.all()

    return render(request, 'depenses/enveloppes_liste.html', {
        'depenses_a_payer': depenses_a_payer,
        'enveloppes': enveloppes,
    })


@permission_required('depenses.change_depense', login_url='/accounts/login/')
def enveloppe_export_csv(request, enveloppe_id):
    enveloppe = EnveloppePaiement.objects.get(id=enveloppe_id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="enveloppe_{enveloppe.id}.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Fournisseur', 'Montant TTC', 'Communication'])
    for depense in enveloppe.depenses.all():
        writer.writerow([depense.fournisseur, f"{depense.montant_ttc:.2f}", depense.description])

    return response


@permission_required('depenses.change_depense', login_url='/accounts/login/')
def enveloppe_marquer_envoyee(request, enveloppe_id):
    enveloppe = EnveloppePaiement.objects.get(id=enveloppe_id)
    marquer_envoyee(enveloppe)
    messages.success(request, f"Enveloppe #{enveloppe.id} marquée comme envoyée. Dépenses payées.")
    return redirect('enveloppes_liste')