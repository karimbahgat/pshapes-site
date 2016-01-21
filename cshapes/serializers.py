from cshapes.models import cshapes
from rest_framework_gis import serializers


class CshapesSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = cshapes
        geo_field = "geom"
        fields = ('cntry_name', 'capname',
                  "gwsyear", "gwsmonth", "gwsday",
                  "gweyear", "gwemonth", "gweday")


