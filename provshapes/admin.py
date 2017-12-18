from django.contrib.gis import admin

# Register your models here.

from models import ProvShape

admin.site.register(ProvShape, admin.GeoModelAdmin)
