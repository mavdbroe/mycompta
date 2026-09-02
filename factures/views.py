from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
from .models import Facture
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import FactureForm, LigneFactureFormSet

@login_required
def facture_pdf(request, facture_id):
    facture = get_object_or_404(Facture, id=facture_id)

    html_string = render_to_string('factures/facture_pdf.html', {
        'facture': facture,
        'entreprise': settings.MON_ENTREPRISE,
    })

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="facture_{facture.numero}.pdf"'
    return response

@permission_required('factures.add_facture', login_url='/accounts/login/')
def facture_creer(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        formset = LigneFactureFormSet(request.POST, prefix='lignes')
        if form.is_valid() and formset.is_valid():
            facture = form.save()
            formset.instance = facture
            formset.save()
            messages.success(request, f"Facture {facture.numero} créée avec succès.")
            return redirect('facture_pdf', facture_id=facture.id)
        else:
            messages.error(request, "Le formulaire contient des erreurs, vérifie les champs en rouge.")
    else:
        form = FactureForm()
        formset = LigneFactureFormSet(prefix='lignes')

    return render(request, 'factures/facture_form.html', {
        'form': form,
        'formset': formset,
    })