from django.shortcuts import render, get_object_or_404
from django import forms

from .models import ProvChange


# Create your views here.

def dashboard(request):
    changelist = ProvChange.objects.all()
    html = render(request, 'provchanges/dashboard.html', {'changelist': changelist})
    return html

def submitchange(request):
    args = {'typechange': TypeChangeForm(),
            'generalchange': GeneralChangeForm(),
            'fromchange': FromChangeForm(),
            'geochange': GeoChangeForm(),
            'tochange': ToChangeForm(),}
    html = render(request, 'provchanges/submitchange.html', args)
    return html

def editchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)
    args = {'typechange': TypeChangeForm(instance=change),
            'generalchange': GeneralChangeForm(instance=change),
            'fromchange': FromChangeForm(instance=change),
            'geochange': GeoChangeForm(instance=change),
            'tochange': ToChangeForm(instance=change),}
    html = render(request, 'provchanges/editchange.html', args)
    return html






# Change form

class TypeChangeForm(forms.ModelForm):

    class Meta:
        model = ProvChange
        fields = ['type']

class GeneralChangeForm(forms.ModelForm):

    class Meta:
        model = ProvChange
        fields = ['country', 'date']

class FromChangeForm(forms.ModelForm):

    class Meta:
        model = ProvChange
        fields = 'fromname fromiso fromfips fromhasc fromcapital fromtype'.split()

class ToChangeForm(forms.ModelForm):

    class Meta:
        model = ProvChange
        fields = 'toname toiso tofips tohasc tocapital totype'.split()


from django.contrib.gis.forms import ModelForm as GeoModelForm

class GeoChangeForm(GeoModelForm):

    class Meta:
        model = ProvChange
        fields = ["transfer_source","transfer_geom"]
        
##    def __init__(self, *args, **kwargs):
##        super(ProvChangeForm, self).__init__(*args, **kwargs)

        # autozoom map to country depending on country
##        import pycountries as pc
##        self.fields['country'].widget.attrs.update({
##            'onchange': "".join(["var cntr = document.getElementById('id_country').value;",
##                                 #"alert(cntr);",
##                                 "var bbox = [0,0,180,90];", #%s[cntr];" % dict([(c.iso3,getbox(c)) for c in pc.all_countries() if getbox(c)]),
##                                 #"alert(bbox);",
##                                 "geodjango_changepart.map.zoomToExtent(bbox);",
##                                ])
##            })

##        self.fields = (
##                    (None, {
##                        'fields': ('country', 'date', 'type')
##                    }),
##                    ('Map', {
##                        'classes': ('collapse',),
##                        'fields': ('transfer_source', 'transfer_geom'),
##                    }),
##                    ("From Province", {
##                        'fields': tuple('fromname fromiso fromfips fromhasc fromcapital fromtype'.split())
##                    }),
##                    ("To Province", {
##                        'fields': tuple('toname toiso tofips tohasc tocapital totype'.split())
##                    }),
##                )

        # make wms auto add/update on sourceurl input
##        self.fields['transfer_source'].widget.attrs.update({
##            'oninput': "".join(["var wmsurl = document.getElementById('id_transfer_source').value;",
##                                "var layerlist = geodjango_transfer_geom.map.getLayersByName('Custom WMS');",
##                                "if (layerlist.length >= 1) ",
##                                "{",
##                                "layerlist[0].url = wmsurl;",
##                                "} ",
##                                "else {",
##                                """customwms = new OpenLayers.Layer.WMS("Custom WMS", wmsurl, {layers: 'basic'} );""",
##                                """customwms.isBaseLayer = false;""",
##                                """geodjango_transfer_geom.map.addLayer(customwms);""",
##                                "};",
##                                ])
