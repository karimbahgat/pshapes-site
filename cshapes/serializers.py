from cshapes.models import cshapes
from rest_framework_gis import serializers


# currently not being used since is very very slow...

class CshapesSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = cshapes
        geo_field = "geom"
        fields = ('cntry_name', 'capname',
                  "gwsyear", "gwsmonth", "gwsday",
                  "gweyear", "gwemonth", "gweday")


