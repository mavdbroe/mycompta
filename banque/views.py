import csv
import io
from datetime import datetime
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LigneReleve
from factures.models import Facture
from django.contrib.auth.decorators import login_required, permission_required

@permission_required('banque.add_lignereleve', login_url='/accounts/login/')
def import_releve(request):
    if request.method == 'POST':
        fichier = request.FILES.get('fichier_csv')
        if not fichier:
            messages.error(request, "Aucun fichier sélectionné.")
            return redirect('import_releve')

        contenu = fichier.read().decode('utf-8')
        lecteur = csv.reader(io.StringIO(contenu), delimiter=';')

        nb_importees = 0
        nb_rapprochees = 0

        for ligne in lecteur:
            if len(ligne) < 3:
                continue
            date_str, montant_str, communication = ligne[0], ligne[1], ligne[2]
            try:
                date_operation = datetime.strptime(date_str.strip(), '%d/%m/%Y').date()
                montant = Decimal(montant_str.strip().replace(',', '.'))
            except (ValueError, InvalidOperation):
                continue

            ligne_releve = LigneReleve.objects.create(
                date_operation=date_operation,
                montant=montant,
                communication=communication.strip(),
            )
            nb_importees += 1

            if montant > 0:
                candidates = Facture.objects.exclude(statut__in=['payee', 'annulee'])
                facture_trouvee = None
                for facture in candidates:
                    if facture.numero in communication or facture.total_ttc == montant:
                        facture_trouvee = facture
                        break
                if facture_trouvee:
                    ligne_releve.facture = facture_trouvee
                    ligne_releve.rapprochee = True
                    ligne_releve.save()
                    facture_trouvee.statut = 'payee'
                    facture_trouvee.save()
                    nb_rapprochees += 1

        messages.success(request, f"{nb_importees} ligne(s) importée(s), {nb_rapprochees} rapprochée(s) automatiquement.")
        return redirect('import_releve')

    return render(request, 'banque/import_releve.html', {
        'lignes_recentes': LigneReleve.objects.all()[:20],
    })