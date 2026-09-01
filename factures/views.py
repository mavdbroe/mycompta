from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
from .models import Facture
from django.contrib.auth.decorators import login_required

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