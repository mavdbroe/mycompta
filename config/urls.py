from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from comptabilite.views import balance_comptes, rapport_tva
from factures.views import facture_pdf
from config.views import tableau_de_bord

urlpatterns = [
    path('', tableau_de_bord, name='tableau_de_bord'),
    path('admin/', admin.site.urls),
    path('comptabilite/balance/', balance_comptes, name='balance_comptes'),
    path('comptabilite/tva/', rapport_tva, name='rapport_tva'),
    path('factures/<int:facture_id>/pdf/', facture_pdf, name='facture_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)