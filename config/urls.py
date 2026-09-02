from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from comptabilite.views import balance_comptes, rapport_tva
from factures.views import facture_pdf, facture_creer
from config.views import tableau_de_bord, documents
from banque.views import import_releve

urlpatterns = [
    path('', tableau_de_bord, name='tableau_de_bord'),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('comptabilite/balance/', balance_comptes, name='balance_comptes'),
    path('comptabilite/tva/', rapport_tva, name='rapport_tva'),
    path('factures/<int:facture_id>/pdf/', facture_pdf, name='facture_pdf'),
    path('banque/import/', import_releve, name='import_releve'),
    path('documents/', documents, name='documents'),
    path('factures/nouvelle/', facture_creer, name='facture_creer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)