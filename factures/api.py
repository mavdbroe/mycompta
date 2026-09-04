from rest_framework import viewsets
from .models import Facture
from .serializers import FactureSerializer


class FactureViewSet(viewsets.ModelViewSet):
    queryset = Facture.objects.all().order_by('-date_emission')
    serializer_class = FactureSerializer