from django.contrib.gis import admin

# Register your models here.

from models import ProvChange

admin.site.register(ProvChange, admin.GeoModelAdmin)
