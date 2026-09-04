from rest_framework import viewsets
from .models import Depense
from .serializers import DepenseSerializer


class DepenseViewSet(viewsets.ModelViewSet):
    queryset = Depense.objects.all().order_by('-date_depense')
    serializer_class = DepenseSerializer