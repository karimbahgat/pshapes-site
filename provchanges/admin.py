from django.contrib.gis import admin

# Register your models here.

from models import ProvChange, User, Vouch, Comment

admin.site.register(User, admin.GeoModelAdmin)
admin.site.register(ProvChange, admin.GeoModelAdmin)
admin.site.register(Vouch, admin.GeoModelAdmin)
admin.site.register(Comment, admin.GeoModelAdmin)
