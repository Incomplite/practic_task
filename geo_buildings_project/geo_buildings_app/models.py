from django.contrib.gis.db import models

class Building(models.Model):
    geom = models.PolygonField(srid=4326)
    address = models.CharField(max_length=255)