from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import admin

from django.core.paginator import Paginator

from rest_framework import response
from rest_framework.decorators import api_view

from .models import ProvChange

import datetime


# Create your views here.

def registration(request):
    
    if request.method == "POST":
        print "data",request.POST
        fieldnames = [f.name for f in User._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))
        print formfieldvalues
        obj = User.objects.create_user(**formfieldvalues)
        print obj
        obj.save()

        html = redirect("/dashboard/")

    elif request.method == "GET":
        args = {'logininfo': LoginInfoForm(),
                'userinfo': UserInfoForm(),
                }
        html = render(request, 'provchanges/registration.html', args)

    return html

def login(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print username,password
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            auth_login(request, user)
            html = redirect("/dashboard/")
        else:
            args = {'login': LoginForm(),
                    'errormessage': "Could not find that username or password",
                    }
            html = render(request, 'provchanges/login.html', args)
            
    elif request.method == "GET":
        print request, request.user
        args = {'login': LoginForm(),
                }
        html = render(request, 'provchanges/login.html', args)

    return html

@login_required
def logout(request):
    print request, request.user
    auth_logout(request)
    html = render(request, 'provchanges/logout.html')
    return html

@login_required
def dashboard(request):
    print request, request.user
    changelist = ProvChange.objects.all()
    pages = Paginator(changelist, 10)

    page = request.GET.get("page", 1)
    if page:
        changelist = pages.page(page)
    
    html = render(request, 'provchanges/dashboard.html', {'changelist': changelist})
    return html

@login_required
def submitchange(request):
    
    if request.method == "POST":
        print "data",request.POST
        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))
        formfieldvalues["user"] = request.user.username
        formfieldvalues["added"] = datetime.date.today()
        print formfieldvalues
        obj = ProvChange.objects.create(**formfieldvalues)
        print obj
        obj.save()

        # hmmmm # need to make get request to editchange to just return basic html of the get

        html = redirect("/provchange/%s/view/" % obj.pk)

    elif request.method == "GET":
        args = {'typechange': TypeChangeForm(),
                'generalchange': GeneralChangeForm(),
                'fromchange': FromChangeForm(),
                'geochange': GeoChangeForm(),
                'tochange': ToChangeForm(),}
        html = render(request, 'provchanges/submitchange.html', args)
        
    return html

def viewchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)

    args = {'pk': pk,
            'metachange': MetaChangeForm(instance=change),
            'typechange': TypeChangeForm(instance=change),
            'generalchange': GeneralChangeForm(instance=change),
            'fromchange': FromChangeForm(instance=change),
            'geochange': GeoChangeForm(instance=change),
            'tochange': ToChangeForm(instance=change),}
    for key,form in args.items():
        if key == "pk": continue
        for field in form.fields.values():
            field.widget.attrs['readonly'] = "readonly"
    for key,form in args.items():
        if key == "pk": continue
        for field in form.fields.values():
            print "------",key,field,field.widget.attrs['readonly']
    html = render(request, 'provchanges/viewchange.html', args)
        
    return html

@login_required
def editchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)

    if request.method == "POST":
        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))
        formfieldvalues["user"] = request.user.username
        print formfieldvalues

        changeobj = ProvChange.objects.get(pk=pk)
        changeobj.__dict__.update(**formfieldvalues)
        changeobj.save()

        html = redirect("/provchange/%s/view/" % pk)
        
    elif request.method == "GET":
        args = {'pk': pk,
                'typechange': TypeChangeForm(instance=change),
                'generalchange': GeneralChangeForm(instance=change),
                'fromchange': FromChangeForm(instance=change),
                'geochange': GeoChangeForm(instance=change),
                'tochange': ToChangeForm(instance=change),}
        html = render(request, 'provchanges/editchange.html', args)
        
    return html






# Date...

class CustomDateWidget(admin.widgets.AdminDateWidget):
    
    def render(self, name, value, attrs = None):
        output = super(CustomDateWidget, self).render(name, value, attrs)
        output += """
<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/smoothness/jquery-ui.css">
<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>

<script>
$('#id_date').datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: "yy-mm-dd",
    defaultDate: "2014-12-31",
    yearRange: '1946:2014',

});
</script>
"""
        return output

    


# Auth forms

from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username","password"]

class LoginInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username","password"]

class UserInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["first_name","last_name","email"]

        


# Change form

class MetaChangeForm(forms.ModelForm):

    class Meta:
        model = ProvChange
        fields = ['user','added','status']

class TypeChangeForm(forms.ModelForm):

    class Meta:
        model = ProvChange
        fields = ['type']

class GeneralChangeForm(forms.ModelForm):

    class Meta:
        model = ProvChange
        fields = ['country', 'date']
        widgets = {"date": CustomDateWidget()}

class FromChangeForm(forms.ModelForm):

    class Meta:
        model = ProvChange
        fields = 'fromname fromiso fromfips fromhasc fromcapital fromtype'.split()

class ToChangeForm(forms.ModelForm):

    class Meta:
        model = ProvChange
        fields = 'toname toiso tofips tohasc tocapital totype'.split()




#################################################
# BUILTIN

from django.contrib.gis.forms.widgets import OpenLayersWidget

##class GeoChangeForm(forms.ModelForm):
##
##    class Meta:
##        model = ProvChange
##        fields = ["transfer_source","transfer_geom"]
##        widgets = {'transfer_geom': OpenLayersWidget()}

class CustomOLWidget(OpenLayersWidget):
    default_zoom = 1
    
    def render(self, name, value, attrs = None):
        output = super(CustomOLWidget, self).render(name, value, attrs)
        output += """
<script>
function syncwms() {
var wmsurl = document.getElementById('id_transfer_source').value;
if (wmsurl.trim() != "") {
    var layerlist = geodjango_transfer_geom.map.getLayersByName('Custom WMS');
    if (layerlist.length >= 1) 
        {
        // replace existing
        geodjango_transfer_geom.map.removeLayer(layerlist[0]);
        customwms = new OpenLayers.Layer.WMS("Custom WMS", wmsurl, {layers: 'basic'} );
        customwms.isBaseLayer = false;
        geodjango_transfer_geom.map.addLayer(customwms);
        } 
    else {
        // add as new
        customwms = new OpenLayers.Layer.WMS("Custom WMS", wmsurl, {layers: 'basic'} );
        customwms.isBaseLayer = false;
        geodjango_transfer_geom.map.addLayer(customwms);
        };
};
};

// at startup
syncwms();

</script>
"""
        return output

class GeoChangeForm(forms.ModelForm):

    class Meta:
        model = ProvChange
        fields = ["transfer_source","transfer_reference","transfer_geom"]
        
    def __init__(self, *args, **kwargs):
        super(GeoChangeForm, self).__init__(*args, **kwargs)

        # autozoom map to country depending on country
##        self.fields['country'].widget.attrs.update({
##            'onchange': "".join(["var cntr = document.getElementById('id_country').value;",
##                                 #"alert(cntr);",
##                                 "var bbox = [0,0,180,90];", #%s[cntr];" % dict([(c.iso3,getbox(c)) for c in pc.all_countries() if getbox(c)]),
##                                 #"alert(bbox);",
##                                 "geodjango_transfer_geom.map.zoomToExtent(bbox);",
##                                ])
##            })

        # TODO: Also alter required status dynamically

##        # hide map widgets on startup
##        self.fields['sourceurl'].widget.attrs.update({"style":"display:none"})
##        self.fields['changepart'].widget.attrs.update({"style":"display:none"}) # grabbing wrong widget so not yet working
##
##        # show/hide map widget depending on changetype
##        self.fields['changetype'].widget.attrs.update({
##            'onchange': "".join(["var changetype = document.getElementById('id_changetype').value;",
##                                "if (changetype == 'PartTransfer') ",
##                                "{",
##                                "document.getElementById('id_changepart_admin_map').style.display = 'block';",
##                                "document.getElementById('id_sourceurl').style.display = 'block';",
##                                "} ",
##                                "else {",
##                                "document.getElementById('id_changepart_admin_map').style.display = 'none';",
##                                "document.getElementById('id_sourceurl').style.display = 'none';",
##                                "};",
##                                ])
##            })

        # make wms auto add/update at startup
        # by overriding widget's render func and adding custom js
        self.fields['transfer_geom'].widget = CustomOLWidget()

        # also load wms on sourceurl input
        self.fields['transfer_source'].widget.attrs.update({
            'oninput': "syncwms();",

            # http://mapwarper.net/maps/wms/11512?request=GetMap&version=1.1.1&format=image/png
            #'onclick': """geodjango_changepart.map.layers.sourceurl = new OpenLayers.Layer.WMS("Custom WMS","http://mapwarper.net/maps/wms/11512?request=GetMap&version=1.1.1&format=image/png", {layers: 'basic'} ); geodjango_changepart.map.addLayer(geodjango_changepart.map.layers.sourceurl);"""
            #'onclick': """window.open ("http://www.javascript-coder.com","mywindow","menubar=1,resizable=1,width=350,height=250");"""
            #'onclick': """alert(geodjango_changepart.map)"""
            #'onclick': """alert(Object.getOwnPropertyNames(geodjango_changepart.map))"""
            
        })





#################################################
# LEAFLET VERSION

##from leaflet.forms.widgets import LeafletWidget
##
##LeafletWidget.settings_overrides.update({"RESET_VIEW":False,                                         })
##
##class GeoChangeForm(forms.ModelForm):
##
##    class Meta:
##        model = ProvChange
##        fields = ["transfer_source","transfer_geom"]
##        widgets = {'transfer_geom': LeafletWidget()}

##    def __init__(self, *args, **kwargs):
##        forms.ModelForm.__init__(self, *args, **kwargs)
##        # make wms auto add/update on sourceurl input
##        self.fields['transfer_source'].widget.attrs.update({
##            "onload":"""
##$(document).ready(function() {
##    // Store the variable to hold the map in scope
##    var map;
##    alert("hello");
##    
##    // Populate the map var during the map:init event (see Using Javascript callback function)
##    // here https://github.com/makinacorpus/django-leaflet
##    $(window).on('map:init', function(e) {
##      map = e.originalEvent.detail.map;
##      alert(map);
##    });
##""",
##            "onchange": """
##var map = L.Map.djangoMap('id_transfer_geom_map') //window['loadmap' + 'id_transfer_geom_map'];
##alert(map);
##var nexrad = L.tileLayer.wms("http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi", {
##    layers: 'nexrad-n0r-900913',
##    format: 'image/png',
##    transparent: true,
##    attribution: "Weather data 2012 IEM Nexrad"
##});
##map.addLayer(nexrad);
##"""
##            })

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
        


################################################################
# OLWIDGET APPROACH

###from django.contrib.gis.forms.widgets import OpenLayersWidget
##from olwidget.fields import EditableLayerField, MapField, MapModelForm
##
##
##
##class GeoChangeForm(MapModelForm):
##
##    class Meta:
##        model = ProvChange
##        fields = ["transfer_source","transfer_geom"]
##
####    def __init__(self, *args, **kwargs):
####        super(MapModelForm, self).__init__(*args, **kwargs)
##
####        # autozoom map to country depending on country
######        import pycountries as pc
######        self.fields['country'].widget.attrs.update({
######            'onchange': "".join(["var cntr = document.getElementById('id_country').value;",
######                                 #"alert(cntr);",
######                                 "var bbox = [0,0,180,90];", #%s[cntr];" % dict([(c.iso3,getbox(c)) for c in pc.all_countries() if getbox(c)]),
######                                 #"alert(bbox);",
######                                 "geodjango_changepart.map.zoomToExtent(bbox);",
######                                ])
######            })
####
######        self.fields = (
######                    (None, {
######                        'fields': ('country', 'date', 'type')
######                    }),
######                    ('Map', {
######                        'classes': ('collapse',),
######                        'fields': ('transfer_source', 'transfer_geom'),
######                    }),
######                    ("From Province", {
######                        'fields': tuple('fromname fromiso fromfips fromhasc fromcapital fromtype'.split())
######                    }),
######                    ("To Province", {
######                        'fields': tuple('toname toiso tofips tohasc tocapital totype'.split())
######                    }),
######                )
##
##        # make wms auto add/update on sourceurl input
####        self.fields['transfer_geom'].widget = EditableLayerField().widget
####        self.fields['transfer_source'].widget.attrs.update({
####            "onload": "alert(OpenLayers);",
####            'oninput': "".join(["alert(OpenLayers.objectName);","var wmsurl = document.getElementById('id_transfer_source').value;",
####                                "alert(wmsurl);",
####                                """var customwms = new OpenLayers.Layer.WMS("Custom WMS", wmsurl, {layers: 'basic'} );""",
####                                #"""customwms.isBaseLayer = false;""",
####                                "alert(customwms.objectName);",
####                                """geodjango_transfer_geom.map.addLayer(customwms);""",
####                                ])
####            })
