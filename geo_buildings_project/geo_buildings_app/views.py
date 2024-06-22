from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Building
from .serializers import BuildingSerializer
from django.contrib.gis.db.models.functions import Area
from .filters import BuildingFilter

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BuildingFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(area=Area('geom'))
        return queryset
