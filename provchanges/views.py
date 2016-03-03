from django.shortcuts import render, get_object_or_404, redirect
from django.template import Template,Context
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

        html = redirect("/contribute/")

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
            html = redirect("/contribute/")
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
def contribute(request):
    print request, request.user
    changelist = ProvChange.objects.all()
    pages = Paginator(changelist, 10)

    page = request.GET.get("page", 1)
    if page:
        changelist = pages.page(page)
    
    html = render(request, 'provchanges/contribute.html', {'changelist': changelist})
    return html

def contribute(request):
    return contribute_accepted(request)

def contribute_accepted(request):
    bannertitle = "Contributing is easy! Here is how:"
    bannerleft = """
                    <div style="text-align:left">
                        <ol>
			<li>Find a source documenting a province change, eg <a href="http://www.statoids.com">the Statoids website</a>.</li>
			<li>Go to the submission form and fill in the information.</li>
			<li>Send it and wait for a moderator to verify and accept your submission!</li>
			</ol>
			
			Your submitted information will be included in the next updated version of the downloadable Pshapes dataset.
		    </div>
    """
    bannerright = """
			<a href="/submitchange" style="background-color:orange; color:white; border-radius:5px; padding:5px">
			<b>Submit New Change...</b>
			</a>
    """

    changes = ProvChange.objects.filter(status="Accepted").order_by("-added") # the dash reverses the order
    changestable = model2table(request, title="", objects=changes,
                              fields=["date","type","fromname","toname","country","user","added","status"])

    tabs = """
            <style>
            .curtab {
                display:table-cell;
                background-color:orange;
                color:white;
                border-radius:10px;
                padding:10px; 
                }
            .tab {
                display:table-cell;
                background-color:null;
                color:black;
                border-radius:10px;
                padding:10px;
                }
            </style>

            <div class="curtab"><h4><a href="/contribute/accepted" style="color:inherit">Accepted</a></h4></div>
            <div class="tab"><h4><a href="/contribute/pending" style="color:inherit">Pending</a></h4></div>
            <div class="tab"><h4><a href="/contribute/countries" style="color:inherit">Countries</a></h4></div>

            <br>
            <br>
            
            """
    content = tabs + changestable
    
    grids = []
    grids.append(dict(title="Browse province changes:",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

def contribute_pending(request):
    bannertitle = "Contributing is easy! Here is how:"
    bannerleft = """
                    <div style="text-align:left">
                        <ol>
			<li>Find a source documenting a province change, eg <a href="http://www.statoids.com">the Statoids website</a>.</li>
			<li>Go to the submission form and fill in the information.</li>
			<li>Send it and wait for a moderator to verify and accept your submission!</li>
			</ol>
			
			Your submitted information will be included in the next updated version of the downloadable Pshapes dataset.
		    </div>
    """
    bannerright = """
			<a href="/submitchange" style="background-color:orange; color:white; border-radius:5px; padding:5px">
			<b>Submit New Change...</b>
			</a>
    """

    changes = ProvChange.objects.filter(status="Pending").order_by("-added") # the dash reverses the order
    changestable = model2table(request, title="", objects=changes,
                              fields=["date","type","fromname","toname","country","user","added","status"])

    tabs = """
            <style>
            .curtab {
                display:table-cell;
                background-color:orange;
                color:white;
                border-radius:10px;
                padding:10px; 
                }
            .tab {
                display:table-cell;
                background-color:null;
                color:black;
                border-radius:10px;
                padding:10px;
                }
            </style>

            <div class="tab"><h4><a href="/contribute/accepted" style="color:inherit">Accepted</a></h4></div>
            <div class="curtab"><h4><a href="/contribute/pending" style="color:inherit">Pending</a></h4></div>
            <div class="tab"><h4><a href="/contribute/countries" style="color:inherit">Countries</a></h4></div>

            <br>
            <br>
            
            """
    content = tabs + changestable
    
    grids = []
    grids.append(dict(title="Browse province changes:",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

def contribute_countries(request):
    bannertitle = "Contributing is easy! Here is how:"
    bannerleft = """
                    <div style="text-align:left">
                        <ol>
			<li>Find a source documenting a province change, eg <a href="http://www.statoids.com">the Statoids website</a>.</li>
			<li>Go to the submission form and fill in the information.</li>
			<li>Send it and wait for a moderator to verify and accept your submission!</li>
			</ol>
			
			Your submitted information will be included in the next updated version of the downloadable Pshapes dataset.
		    </div>
    """
    bannerright = """
			<a href="/submitchange" style="background-color:orange; color:white; border-radius:5px; padding:5px">
			<b>Submit New Change...</b>
			</a>
    """

    from django.db.models import Count,Max,Min
    
    fields = ["country","entries","mindate","maxdate"]
    lists = []
    for rowdict in ProvChange.objects.values("country").annotate(entries=Count('pk'),
                                                             mindate=Min("date"),
                                                             maxdate=Max("date") ):
        row = [rowdict[f] for f in fields]
        url = "/contribute/countries/%s" % rowdict["country"]
        lists.append((url,row))
    
    countriestable = lists2table(request, lists=lists,
                              fields=fields)

    tabs = """
            <style>
            .curtab {
                display:table-cell;
                background-color:orange;
                color:white;
                border-radius:10px;
                padding:10px; 
                }
            .tab {
                display:table-cell;
                background-color:null;
                color:black;
                border-radius:10px;
                padding:10px;
                }
            </style>

            <div class="tab"><h4><a href="/contribute/accepted" style="color:inherit">Accepted</a></h4></div>
            <div class="tab"><h4><a href="/contribute/pending" style="color:inherit">Pending</a></h4></div>
            <div class="curtab"><h4><a href="/contribute/countries" style="color:inherit">Countries</a></h4></div>

            <br>
            <br>
            
            """
    content = tabs + countriestable
    
    grids = []
    grids.append(dict(title="Browse province changes:",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )


def contribute_countries_country(request, country):
    bannertitle = "Contributing is easy! Here is how:"
    bannerleft = """
                    <div style="text-align:left">
                        <ol>
			<li>Find a source documenting a province change, eg <a href="http://www.statoids.com">the Statoids website</a>.</li>
			<li>Go to the submission form and fill in the information.</li>
			<li>Send it and wait for a moderator to verify and accept your submission!</li>
			</ol>
			
			Your submitted information will be included in the next updated version of the downloadable Pshapes dataset.
		    </div>
    """
    bannerright = """
			<a href="/submitchange" style="background-color:orange; color:white; border-radius:5px; padding:5px">
			<b>Submit New Change...</b>
			</a>
    """

    changes = ProvChange.objects.filter(country=country).order_by("-added") # the dash reverses the order
    changestable = model2table(request, title="", objects=changes,
                              fields=["date","type","fromname","toname","country","user","added","status"])

    tabs = """
            <style>
            .curtab {
                display:table-cell;
                background-color:orange;
                color:white;
                border-radius:10px;
                padding:10px; 
                }
            .tab {
                display:table-cell;
                background-color:null;
                color:black;
                border-radius:10px;
                padding:10px;
                }
            </style>

            <div class="tab"><h4><a href="/contribute/accepted" style="color:inherit">Accepted</a></h4></div>
            <div class="curtab"><h4><a href="/contribute/pending" style="color:inherit">Pending</a></h4></div>
            <div class="tab"><h4><a href="/contribute/countries" style="color:inherit">Countries</a></h4></div>

            <br>
            <br>
            
            """
    content = tabs + changestable
    
    grids = []
    grids.append(dict(title="Browse province changes:",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

@login_required
def submitchange(request):
    
    if request.method == "POST":
        print "data",request.POST
        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))
        formfieldvalues["user"] = request.user.username
        formfieldvalues["added"] = datetime.date.today()
        formfieldvalues["bestversion"] = True
        print formfieldvalues
        obj = ProvChange.objects.create(**formfieldvalues)
        obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions
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

def model2table(request, title, objects, fields):
    html = """
		<table class="modeltable"> 
		
			<style>
			table {
				border-collapse: collapse;
				width: 100%;
			}

			th, td {
				text-align: left;
				padding: 8px;
			}

			tr:nth-child(even){background-color: #f2f2f2}

			th {
				background-color: orange;
				color: white;
			}
			</style>
		
			<tr>
				<th> 
				</th>

				{% for field in fields %}
                                    <th>
                                        <b>{{ field }}</b>
                                    </th>
                                {% endfor %}
                                    
			</tr>
			</a>
			
			{% for pk,changerow in changelist %}
				<tr>
					<td>
					<a href="{% url 'viewchange' pk=pk %}">View</a>
					</td>
					
                                        {% for value in changerow %}
                                            <td>{{ value }}</td>
                                        {% endfor %}
					
				</tr>
			{% endfor %}
		</table>
                """
    changelist = ((change.pk, [getattr(change,field) for field in fields]) for change in objects)
    rendered = Template(html).render(Context({"request":request, "fields":fields, "changelist":changelist, "title":title}))
    return rendered


def lists2table(request, lists, fields):
    html = """
		<table> 
		
			<style>
			table {
				border-collapse: collapse;
				width: 100%;
			}

			th, td {
				text-align: left;
				padding: 8px;
			}

			tr:nth-child(even){background-color: #f2f2f2}

			th {
				background-color: orange;
				color: white;
			}
			</style>
		
			<tr>
				<th> 
				</th>

				{% for field in fields %}
                                    <th>
                                        <b>{{ field }}</b>
                                    </th>
                                {% endfor %}
                                    
			</tr>
			</a>
			
			{% for url,row in lists %}
				<tr>
					<td>
					<a href="{{ url }}">View</a>
					</td>
					
                                        {% for value in row %}
                                            <td>{{ value }}</td>
                                        {% endfor %}
					
				</tr>
			{% endfor %}
		</table>
                """
    rendered = Template(html).render(Context({"request":request, "fields":fields, "lists":lists}))
    return rendered

def viewchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)

    if not change.bestversion:
        note = """
                <div style="background-color:rgb(248,234,150); outline: black solid thick; padding:1%%; font-family: comic sans ms">
                <p style="font-size:large; font-weight:bold">Note:</p>
                <p style="font-size:medium; font-style:italic">
                There is a more recent version of this province change <a href="/provchange/%s/view/">here</a>.
                </p>
                </div>
                <br>
                """ % ProvChange.objects.get(changeid=change.changeid, bestversion=True).pk
    else:
        note = ""

    pendingedits = ProvChange.objects.filter(changeid=change.changeid, status="Pending").order_by("-added") # the dash reverses the order
    pendingeditstable = model2table(request, title="New Edits:", objects=pendingedits,
                              fields=["date","type","fromname","toname","country","user","added","status"])

    oldversions = ProvChange.objects.filter(changeid=change.changeid, status="NonActive").order_by("-added") # the dash reverses the order
    oldversionstable = model2table(request, title="Revision History:", objects=oldversions,
                              fields=["date","type","fromname","toname","country","user","added","status"])

    args = {'pk': pk,
            'note': note,
            'metachange': MetaChangeForm(instance=change),
            'typechange': TypeChangeForm(instance=change),
            'generalchange': GeneralChangeForm(instance=change),
            'fromchange': FromChangeForm(instance=change),
            'geochange': GeoChangeForm(instance=change),
            'tochange': ToChangeForm(instance=change),
            "pendingeditstable": pendingeditstable,
            "oldversionstable": oldversionstable,
            }
    
    for key,val in args.items():
        if hasattr(val,"fields"):
            for field in val.fields.values():
                field.widget.attrs['readonly'] = "readonly"
                
    html = render(request, 'provchanges/viewchange.html', args)
        
    return html

@login_required
def editchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)

    if request.method == "POST":
        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))
        formfieldvalues["user"] = request.user.username
        formfieldvalues["added"] = datetime.date.today()
        formfieldvalues["status"] = "Pending"

        if request.user.username == change.user:
            for c in ProvChange.objects.filter(changeid=change.changeid):
                # all previous versions by same user become nonactive and nonbestversion
                c.bestversion = False
                c.status = "NonActive"
                c.save()
            formfieldvalues["bestversion"] = True
        
        print formfieldvalues

        change.__dict__.update(**formfieldvalues)
        change.pk = None # nulling the pk will add a modified copy of the instance
        change.save()

        html = redirect("/provchange/%s/view/" % change.pk)
        
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
        widgets = {"password":forms.PasswordInput()}

class LoginInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["username","password"]
        widgets = {"password":forms.PasswordInput()}

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
