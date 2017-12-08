from django.contrib.gis.db import models
from django.contrib.auth.models import User as OrigUser

# Create your models here.


class User(OrigUser):
    institution = models.CharField(max_length=400)
                             

class Vouch(models.Model):
    "A user vouches for a particular provchange id."
    user = models.CharField(max_length=200)
    changeid = models.IntegerField(null=True)
    added = models.DateTimeField()
    status = models.CharField(choices=[("Active","Active"),
                                       ("Withdrawn","Withdrawn"),
                                        ],
                              default="Active",
                              max_length=40)


class Comment(models.Model):
    "A note is assigned to a country, and optionally a prov changeid."
    user = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    changeid = models.IntegerField(null=True)
    added = models.DateTimeField()
    status = models.CharField(choices=[("Active","Active"),
                                       ("Withdrawn","Withdrawn"),
                                        ],
                              default="Active",
                              max_length=40)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=2000)


class ProvChange(models.Model):

    # TODO: Add verbose_name=...

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
    source = models.CharField(max_length=400, verbose_name=u"Source of information")
    date = models.DateField(verbose_name=u"Date of change")
    type = models.CharField(choices=[("NewInfo","NewInfo"),
                                       ("PartTransfer","PartTransfer"),
                                       ("FullTransfer","FullTransfer"),
                                       ("Breakaway","Breakaway"), 
                                        ],
                            verbose_name=u"Type of Change",
                            max_length=40,)

    # should only show if changetype requires border delimitation...
    transfer_source = models.CharField(max_length=200, verbose_name=u"Link to map data")
    transfer_reference = models.CharField(max_length=400, verbose_name=u"Map description")
    transfer_geom = models.MultiPolygonField(null=True, blank=True, verbose_name=u"Province geometry")

    fromcountry = models.CharField(max_length=40, verbose_name=u"From country")
    fromname = models.CharField(max_length=40, verbose_name=u"From province name")
    fromalterns = models.CharField(max_length=40, blank=True, verbose_name=u"From alternate province names")
    fromiso = models.CharField(max_length=40, blank=True, verbose_name=u"From province ISO code")
    fromfips = models.CharField(max_length=40, blank=True, verbose_name=u"From province FIPS code")
    fromhasc = models.CharField(max_length=40, blank=True, verbose_name=u"From province HASC code")
    fromcapitalname = models.CharField(max_length=40, blank=True, verbose_name=u"From province capital (name change)")
    fromcapital = models.CharField(max_length=40, blank=True, verbose_name=u"From province capital (moved)")
    fromtype = models.CharField(choices=[("Province","Province"),
                                         ("Municipality","Municipality"),
                                         ("District","District"),
                                         ("County","County"),
                                         ("State","State"),
                                         ("Parish","Parish"),
                                         ("Region","Region"),
                                         ("Prefecture","Prefecture"),
                                         ("Department","Department"),
                                         ("Governate","Governate"),
                                         ("Other...","Other...")
                                         ],
                                verbose_name=u"From province type",
                                max_length=40, blank=True)

    tocountry = models.CharField(max_length=40, verbose_name=u"To country")
    toname = models.CharField(max_length=40, verbose_name=u"To province name")
    toalterns = models.CharField(max_length=40, blank=True, verbose_name=u"To province alternate names")
    toiso = models.CharField(max_length=40, blank=True, verbose_name=u"To province ISO code")
    tofips = models.CharField(max_length=40, blank=True, verbose_name=u"To province FIPS code")
    tohasc = models.CharField(max_length=40, blank=True, verbose_name=u"To province HASC code")
    tocapitalname = models.CharField(max_length=40, blank=True, verbose_name=u"To province capital (name change)")
    tocapital = models.CharField(max_length=40, blank=True, verbose_name=u"To province capital (moved)")
    totype = models.CharField(choices=[("Province","Province"),
                                         ("Municipality","Municipality"),
                                         ("District","District"),
                                         ("County","County"),
                                         ("State","State"),
                                         ("Parish","Parish"),
                                         ("Region","Region"),
                                         ("Prefecture","Prefecture"),
                                         ("Department","Department"),
                                         ("Governate","Governate"),
                                         ("Other...","Other...")
                                         ],
                                verbose_name=u"To province type",
                                max_length=40, blank=True)
