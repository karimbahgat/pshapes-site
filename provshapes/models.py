from django.db import models
from django.contrib.gis.db import models

# Create your models here.

class ProvShape(models.Model):
    added = models.DateField(auto_now_add=True, null=True)
    
    name = models.CharField(max_length=100)
    alterns = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=100)
    iso = models.CharField(max_length=10, null=True)
    fips = models.CharField(max_length=10, null=True)
    hasc = models.CharField(max_length=10, null=True)
    start = models.DateField()
    end = models.DateField()

    simplify = models.FloatField(db_index=True, null=True) # allows varying levels of detail
    geom = models.MultiPolygonField(srid=4326)
    geoj = models.TextField(null=True) # precomputed geojson string
    
    objects = models.GeoManager()



