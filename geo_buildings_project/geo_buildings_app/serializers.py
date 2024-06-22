from .models import Building
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers

class BuildingSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Building
        fields = ('id', 'geom', 'address')
        geo_field = 'geom'

    def validate_geom(self, value):
        print(value)
        if not value.valid:
            raise serializers.ValidationError("Invalid geometry")
        return value