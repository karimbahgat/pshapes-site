from django.contrib.gis import admin

# Register your models here.

from models import cshapes

admin.site.register(cshapes, admin.GeoModelAdmin)
