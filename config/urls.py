from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from comptabilite.views import balance_comptes, rapport_tva
from factures.views import facture_pdf, facture_creer
from factures.api import FactureViewSet
from config.views import tableau_de_bord, documents
from banque.views import import_releve
from clients.views import client_creer, clients_liste, client_detail
from clients.api import ClientViewSet
from depenses.views import depense_creer, depenses_liste, enveloppes_liste, enveloppe_export_csv, enveloppe_marquer_envoyee
from depenses.api import DepenseViewSet

router = DefaultRouter()
router.register('clients', ClientViewSet, basename='api-clients')
router.register('factures', FactureViewSet, basename='api-factures')
router.register('depenses', DepenseViewSet, basename='api-depenses')

urlpatterns = [
    path('', tableau_de_bord, name='tableau_de_bord'),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('comptabilite/balance/', balance_comptes, name='balance_comptes'),
    path('comptabilite/tva/', rapport_tva, name='rapport_tva'),
    path('factures/<int:facture_id>/pdf/', facture_pdf, name='facture_pdf'),
    path('factures/nouvelle/', facture_creer, name='facture_creer'),
    path('banque/import/', import_releve, name='import_releve'),
    path('documents/', documents, name='documents'),
    path('clients/', clients_liste, name='clients_liste'),
    path('clients/nouveau/', client_creer, name='client_creer'),
    path('clients/<int:client_id>/', client_detail, name='client_detail'),
    path('depenses/', depenses_liste, name='depenses_liste'),
    path('depenses/nouvelle/', depense_creer, name='depense_creer'),
    path('api/', include(router.urls)),
    path('api/token/', obtain_auth_token, name='api_token'),
    path('depenses/enveloppes/', enveloppes_liste, name='enveloppes_liste'),
    path('depenses/enveloppes/<int:enveloppe_id>/csv/', enveloppe_export_csv, name='enveloppe_export_csv'),
    path('depenses/enveloppes/<int:enveloppe_id>/envoyer/', enveloppe_marquer_envoyee, name='enveloppe_marquer_envoyee'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)