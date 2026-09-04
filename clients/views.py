from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .forms import ClientForm
from .models import Client
from django.shortcuts import get_object_or_404
from factures.models import Facture

@permission_required('clients.add_client', login_url='/accounts/login/')
def client_creer(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f"Client {client.nom} créé avec succès.")
            return redirect('clients_liste')
        else:
            messages.error(request, "Le formulaire contient des erreurs.")
    else:
        form = ClientForm()

    return render(request, 'clients/client_form.html', {'form': form})


def clients_liste(request):
    clients = Client.objects.all().order_by('nom')
    return render(request, 'clients/clients_liste.html', {'clients': clients})


def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    factures = client.factures.all().order_by('-date_emission')

    total_facture = sum(f.total_ttc for f in factures)
    total_du = sum(f.total_ttc for f in factures if f.statut not in ['payee', 'annulee'])

    return render(request, 'clients/client_detail.html', {
        'client': client,
        'factures': factures,
        'total_facture': total_facture,
        'total_du': total_du,
    })