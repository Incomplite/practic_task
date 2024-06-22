from django_filters import rest_framework as filters
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D, Area as GISArea
from .models import Building

class BuildingFilter(filters.FilterSet):
    min_area = filters.NumberFilter(method='filter_min_area')
    max_area = filters.NumberFilter(method='filter_max_area')
    max_distance = filters.NumberFilter(method='filter_max_distance')

    class Meta:
        model = Building
        fields = ['min_area', 'max_area', 'max_distance']

    def filter_min_area(self, queryset, name, value):
        return queryset.filter(area__gte=GISArea(sq_m=float(value)))
    
    def filter_max_area(self, queryset, name, value):
        return queryset.filter(area__lte=GISArea(sq_m=float(value)))

    def filter_max_distance(self, queryset, name, value):
        longitude = self.request.query_params.get('longitude')
        latitude = self.request.query_params.get('latitude')

        if longitude and latitude:
            point = Point(float(longitude), float(latitude), srid=4326)
            return queryset.filter(geom__distance_lte=(point, D(m=float(value))))
        return queryset