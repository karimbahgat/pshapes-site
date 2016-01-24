from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from rest_framework import response
from rest_framework.decorators import api_view

from .models import ProvChange


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
    html = render(request, 'provchanges/dashboard.html', {'changelist': changelist})
    return html

@login_required
def submitchange(request):
    
    if request.method == "POST":
        print "data",request.POST
        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))
        print formfieldvalues
        obj = ProvChange.objects.create(**formfieldvalues)
        print obj
        obj.save()

        # hmmmm # need to make get request to editchange to just return basic html of the get

        html = redirect("/provchange/%s/edit/" % obj.pk)

    elif request.method == "GET":
        args = {'typechange': TypeChangeForm(),
                'generalchange': GeneralChangeForm(),
                'fromchange': FromChangeForm(),
                'geochange': GeoChangeForm(),
                'tochange': ToChangeForm(),}
        html = render(request, 'provchanges/submitchange.html', args)
        
    return html

@login_required
def editchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)

    if request.method == "POST":
        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))
        print formfieldvalues

        changeobj = ProvChange.objects.get(pk=pk)
        changeobj.__dict__.update(**formfieldvalues)
        changeobj.save()

        html = redirect("/provchange/%s/edit/" % pk)
        
    elif request.method == "GET":
        args = {'pk': pk,
                'typechange': TypeChangeForm(instance=change),
                'generalchange': GeneralChangeForm(instance=change),
                'fromchange': FromChangeForm(instance=change),
                'geochange': GeoChangeForm(instance=change),
                'tochange': ToChangeForm(instance=change),}
        html = render(request, 'provchanges/editchange.html', args)
        
    return html






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
