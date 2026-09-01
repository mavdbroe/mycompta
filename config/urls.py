from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from comptabilite.views import balance_comptes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comptabilite/balance/', balance_comptes, name='balance_comptes'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)