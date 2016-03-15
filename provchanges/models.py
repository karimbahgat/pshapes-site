from django.contrib.gis.db import models
from django.contrib.auth.models import User as OrigUser

# Create your models here.


class User(OrigUser):
    institution = models.CharField(max_length=400)
                             

class ProvChange(models.Model):

    changeid = models.IntegerField(null=True)
    bestversion = models.BooleanField(default=False)

    user = models.CharField(max_length=200)
    added = models.DateTimeField()
    status = models.CharField(choices=[("Pending","Pending"),
                                       ("Accepted","Accepted"),
                                       ("NonActive","NonActive"),
                                        ],
                              default="Pending",
                              max_length=40)

    #import pycountries as pc
    source = models.CharField(max_length=400)
    country = models.CharField(choices=[("Vietnam","Vietnam"),("Tanzania","Tanzania")], #(c.iso3,c.name) for c in pc.all_countries()],
                                max_length=40)
    date = models.DateField()
    type = models.CharField(choices=[("NewInfo","NewInfo"),
                                       ("PartTransfer","PartTransfer"),
                                       ("FullTransfer","FullTransfer"),
                                       ("Breakaway","Breakaway"), 
                                        ],
                                    max_length=40,)

    # should only show if changetype requires border delimitation...
    transfer_source = models.CharField(max_length=200)
    transfer_reference = models.CharField(max_length=400)
    transfer_geom = models.MultiPolygonField(null=True, blank=True)
    
    fromname = models.CharField(max_length=40)
    fromiso = models.CharField(max_length=40)
    fromfips = models.CharField(max_length=40)
    fromhasc = models.CharField(max_length=40)
    fromcapital = models.CharField(max_length=40, blank=True)
    fromtype = models.CharField(choices=[("Province","Province"),
                                         ("Municipality","Municipality"),
                                         ],
                                max_length=40, blank=True)

    toname = models.CharField(max_length=40)
    toiso = models.CharField(max_length=40)
    tofips = models.CharField(max_length=40)
    tohasc = models.CharField(max_length=40)
    tocapital = models.CharField(max_length=40, blank=True)
    totype = models.CharField(choices=[("Province","Province"),
                                         ("Municipality","Municipality"),
                                         ],
                                max_length=40, blank=True)
