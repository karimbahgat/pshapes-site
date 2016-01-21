from django.db import models

# Create your models here.

# This is an auto-generated Django model module created by ogrinspect.

from django.contrib.gis.db import models



class cshapes(models.Model):

    sp_id = models.CharField(max_length=5)

    cntry_name = models.CharField(max_length=30)

    area = models.FloatField()

    capname = models.CharField(max_length=19)

    caplong = models.FloatField()

    caplat = models.FloatField()

    featureid = models.IntegerField()

    cowcode = models.IntegerField()

    cowsyear = models.IntegerField()

    cowsmonth = models.IntegerField()

    cowsday = models.IntegerField()

    coweyear = models.IntegerField()

    cowemonth = models.IntegerField()

    coweday = models.IntegerField()

    gwcode = models.IntegerField()

    gwsyear = models.FloatField(db_index=True)

    gwsmonth = models.FloatField(db_index=True)

    gwsday = models.FloatField(db_index=True)

    gweyear = models.FloatField(db_index=True)

    gwemonth = models.FloatField(db_index=True)

    gweday = models.FloatField(db_index=True)

    isoname = models.CharField(max_length=42)

    iso1num = models.IntegerField()

    iso1al2 = models.CharField(max_length=7)

    iso1al3 = models.CharField(max_length=7)

    geom = models.MultiPolygonField(srid=-1)

    objects = models.GeoManager()



# Auto-generated `LayerMapping` dictionary for cshapes model

cshapes_mapping = {

    'sp_id' : 'SP_ID',

    'cntry_name' : 'CNTRY_NAME',

    'area' : 'AREA',

    'capname' : 'CAPNAME',

    'caplong' : 'CAPLONG',

    'caplat' : 'CAPLAT',

    'featureid' : 'FEATUREID',

    'cowcode' : 'COWCODE',

    'cowsyear' : 'COWSYEAR',

    'cowsmonth' : 'COWSMONTH',

    'cowsday' : 'COWSDAY',

    'coweyear' : 'COWEYEAR',

    'cowemonth' : 'COWEMONTH',

    'coweday' : 'COWEDAY',

    'gwcode' : 'GWCODE',

    'gwsyear' : 'GWSYEAR',

    'gwsmonth' : 'GWSMONTH',

    'gwsday' : 'GWSDAY',

    'gweyear' : 'GWEYEAR',

    'gwemonth' : 'GWEMONTH',

    'gweday' : 'GWEDAY',

    'isoname' : 'ISONAME',

    'iso1num' : 'ISO1NUM',

    'iso1al2' : 'ISO1AL2',

    'iso1al3' : 'ISO1AL3',

    'geom' : 'MULTIPOLYGON',

}
