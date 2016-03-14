from django.shortcuts import render, get_object_or_404, redirect
from django.template import Template,Context
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import admin

from django.core.paginator import Paginator

from rest_framework import response
from rest_framework.decorators import api_view

from formtools.wizard.views import SessionWizardView

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

        html = redirect("/provchanges/%s/view/" % obj.pk)

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

    ### WARNING: id_1-date is hacky for now, may not always work...
    
    def render(self, name, value, attrs = None):
        output = super(CustomDateWidget, self).render(name, value, attrs)
        output += """
<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/smoothness/jquery-ui.css">
<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>

<script>
$('#id_1-date').datepicker({
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

from django.forms.widgets import RadioFieldRenderer

class TypeChangeRenderer(RadioFieldRenderer):

    def render(self):
        extrainfo = {"NewInfo": {"label": "NewInfo",
                                 "short": "A change was made to a province's name, codes, or capital.",
                                  "descr": """
                                            Most province changes are as simple as changes in their basic information. In addition, provinces splitting up, 
                                            merging together, or experiencing other major territorial changes are often accompanied by changes
                                            to their name and codes as well. 
                                            """,
                                  "img": '<img style="width:100px" src="http://www.gov.mb.ca/conservation/climate/images/climate_affect.jpg"/>',
                                  },
                      "PartTransfer": {"label": "PartTransfer",
                                       "short": "Part of a province's territory was transferred to another province.",
                                      "descr": """
                                                The transferred territory can be
                                                given to an existing province or serve as part of the foundation for an entirely new province.
                                                (Requires a map showing the province outline prior to the transfer of territory)
                                                """,
                                      "img": '<img style="width:100px" src="http://www.gov.mb.ca/conservation/climate/images/climate_affect.jpg"/>',
                                      },
                     "FullTransfer": {"label": "FullTransfer",
                                      "short": "An entire province ceased to exist and became part of another province.",
                                      "descr": """
                                                For instance, if multiple existing provinces merged together
                                                you would register multiple 'fulltransfer' changes. The transferred territory can be
                                                given to an existing province or serve as part of the foundation for an entirely new province.
                                                (Requires a map showing the now defunct province) 
                                                """,
                                      "img": '<img style="width:100px" src="http://www.gov.mb.ca/conservation/climate/images/climate_affect.jpg"/>',
                                      },
                      "Breakaway": {"label": "Breakaway",
                                    "short": "A new province was created by breaking away from an existing province.",
                                      "descr": """
                                                For instance, if a province split into multiple new provinces
                                                you would register multiple 'breakaway' changes, one for each.
                                                """,
                                      "img": '<img style="width:100px" src="http://www.gov.mb.ca/conservation/climate/images/climate_affect.jpg"/>',
                                      },
                       }
        choices = [(w,extrainfo[w.choice_label]) for w in self if "-" not in w.choice_label]
        html = """
            <table class="myradio">
            {% for choice,extra in choices %}
            <tr>
                <td>{{ choice }}<td>
                <td>{{ extra.img|safe }}</td>
                <td>
                    <h4>{{ extra.short|safe }}</h4>
                    <p>{{ extra.descr|safe }}</p>
                </td>
            </tr>
            {% endfor %}
            </table>
            """
        rendered = Template(html).render(Context({"choices":choices }))
        return rendered

class TypeChangeForm(forms.ModelForm):

    step_title = "Type of Change"
    step_descr = """
                    What type of province change do you want to register? (AcTUALLY sTART WITH FORM TO REgIsTER souRCE...)
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=TypeChangeRenderer) }

class GeneralChangeForm(forms.ModelForm):

    step_title = "Context"
    step_descr = """
                    What was the place and time of the change?
                   """

    class Meta:
        model = ProvChange
        fields = ['country', 'date']
        widgets = {"date": CustomDateWidget()}

class FromChangeForm(forms.ModelForm):

    step_title = "From Province"
    step_descr = """
                    Please identify the province prior to the change or that transferred territory?
                   """

    class Meta:
        model = ProvChange
        fields = 'fromname fromiso fromfips fromhasc fromcapital fromtype'.split()

class ToChangeForm(forms.ModelForm):

    step_title = "To Province"
    step_descr = """
                    Please identify the province after the change or that received territory?
                   """

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
    wms = ""
    
    def render(self, name, value, attrs = None):
        output = super(CustomOLWidget, self).render(name, value, attrs)
        output += """
<script>
function syncwms() {
var wmsurl = "%s";
if (wmsurl.trim() != "") {
    var layerlist = geodjango_5_transfer_geom.map.getLayersByName('Custom WMS');
    
    if (layerlist.length >= 1) 
        {
        // replace existing
        geodjango_5_transfer_geom.map.removeLayer(layerlist[0]);
        };
        
    customwms = new OpenLayers.Layer.WMS("Custom WMS", wmsurl, {layers: 'basic'} );
    customwms.isBaseLayer = false;
    geodjango_5_transfer_geom.map.addLayer(customwms);
    geodjango_5_transfer_geom.map.setLayerIndex(customwms, 1);

    // zoom to country bbox somehow
    //geodjango_5_transfer_geom.map.zoomToExtent(customwms.getDataExtent());
};
};

// at startup
syncwms();

</script>
""" % self.wms # NOTE REQUIRES THAT THE WIZARD SETS THE WIDGET'S WMS ATTRIBUTE BASED ON GEOREF FORM
        
##        output += """
##<script>
##function syncwms() {
##var wmsurl = document.getElementById('id_3-transfer_source').value;
##if (wmsurl.trim() != "") {
##    var layerlist = geodjango_3_transfer_geom.map.getLayersByName('Custom WMS');
##    if (layerlist.length >= 1) 
##        {
##        // replace existing
##        geodjango_3_transfer_geom.map.removeLayer(layerlist[0]);
##        customwms = new OpenLayers.Layer.WMS("Custom WMS", wmsurl, {layers: 'basic'} );
##        customwms.isBaseLayer = false;
##        geodjango_3_transfer_geom.map.addLayer(customwms);
##        } 
##    else {
##        // add as new
##        customwms = new OpenLayers.Layer.WMS("Custom WMS", wmsurl, {layers: 'basic'} );
##        customwms.isBaseLayer = false;
##        geodjango_3_transfer_geom.map.addLayer(customwms);
##        };
##};
##};
##
##// at startup
##syncwms();
##
##</script>
##"""
        return output


class HistoMapForm(forms.ModelForm):

    step_title = "Historical Map"
    step_descr = """
                    Find a historical map from before the change. 
                   """

    class Meta:
        model = ProvChange
        fields = ["transfer_reference"]

    def as_p(self):
        html = """
                        The map should show the giving province as it was prior to the change.
                        This can be either an image you find online or a physical map that you scan.
                        In the field below identify and reference the source, author, and year of the
                        map in as much detail as possible.

                        <div style="padding:20px"><b>Map Reference: </b>{{ form.transfer_reference }}</div>

                            <div style="background-color:rgb(248,234,150); outline: black solid thick; font-family: comic sans ms">
                            <p style="font-size:large; font-weight:bold">Note:</p>
                            <p style="font-size:medium; font-style:italic">
                            Note: In accordance with the open-source
                            nature of the Pshapes project, the map source must be free to share and use without any license restrictions.
                            Submissions that are based on copyrighted map sources will not be used in the final data. 
                            </p>
                            </div>
                """
        rendered = Template(html).render(Context({"form":self}))
        return rendered


class GeorefForm(forms.ModelForm):

    step_title = "Georeference"
    step_descr = """
                    Georeference the historical map image. 
                   """

    class Meta:
        model = ProvChange
        fields = ["transfer_source"]
        
    def as_p(self):
        html = """
                        Georeferencing is as easy as matching a handful of control points on your historical map image with the equivalent
                        locations on a real-world map.
                        For this you must <a href="http://mapwarper.net/">create an account or login to the MapWarper project website</a>.

                        <img style="display:block" align="middle" height=300px src="http://dirtdirectory.org/sites/dirtdirectory.org/files/screenshots/mapwarper.PNG"/>

                        Once finished with georeferencing, click on the "Export" tab of your MapWarper map page,
                        right click the part that says "WMS Capabilities URL" and select "copy the link address".
                        Paste this link address into the "Transfer source" field below.

                        <div style="padding:20px"><b>Georeferenced WMS Link: </b>{{ form.transfer_source }}</div>
                """
        rendered = Template(html).render(Context({"form":self}))
        return rendered


class GeoChangeForm(forms.ModelForm):

    step_title = "Territory"
    step_descr = """
                    What part of the province's territory was transferred?
                   """

    class Meta:
        model = ProvChange
        fields = ["transfer_geom"]
        #widgets = {"transfer_geom": CustomOLWidget() }
        
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
##        self.fields['transfer_source'].widget.attrs.update({
##            'oninput': "syncwms();",
##
##            # http://mapwarper.net/maps/wms/11512?request=GetMap&version=1.1.1&format=image/png
##            #'onclick': """geodjango_changepart.map.layers.sourceurl = new OpenLayers.Layer.WMS("Custom WMS","http://mapwarper.net/maps/wms/11512?request=GetMap&version=1.1.1&format=image/png", {layers: 'basic'} ); geodjango_changepart.map.addLayer(geodjango_changepart.map.layers.sourceurl);"""
##            #'onclick': """window.open ("http://www.javascript-coder.com","mywindow","menubar=1,resizable=1,width=350,height=250");"""
##            #'onclick': """alert(geodjango_changepart.map)"""
##            #'onclick': """alert(Object.getOwnPropertyNames(geodjango_changepart.map))"""
##            
##        })

    def as_p(self):
        html = """
                        Finally, draw on the map. Identify the borders of the province that received the territory, drawing only the part of the territory that actually changed.
                        This is equivalent to drawing the areas that overlap/intersect between the pre-change giving province and the post-change receiving province.

                        <img style="display:block" align="middle" height=300px src="http://localnepaltoday.com/wp-content/uploads/2015/08/image8.jpg"/>

                        <div style="padding:20px"><b>Transferred Territory:</b></div>

                        <div>{{ form.transfer_geom }}</div>
                        
                    """
        rendered = Template(html).render(Context({"form":self}))
        return rendered





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



class SubmitChangeWizard(SessionWizardView):
    form_list = [TypeChangeForm,
                      GeneralChangeForm,
                      FromChangeForm,
                     HistoMapForm,
                     GeorefForm,
                      GeoChangeForm,
                      ToChangeForm,
                      ]
        
##    def __init__(self, *args, **kwargs):
##        self.form_list = [TypeChangeForm,
##                      GeneralChangeForm,
##                      FromChangeForm,
##                      GeoChangeForm,
##                      ToChangeForm,
##                      ]
##        SessionWizardView.__init__(self, *args, **kwargs)

##    @property
##    def form_list(self):
##        return [TypeChangeForm,
##                      GeneralChangeForm,
##                      FromChangeForm,
##                      GeoChangeForm,
##                      ToChangeForm,
##                      ]

    def __iter__(self):
        for step in self.get_form_list():
            yield self.get_form(step=step)

    def get_context_data(self, form, **kwargs):
        context = super(SubmitChangeWizard, self).get_context_data(form=form, **kwargs)
        context.update({'wizard_subclass': self})
        return context

    def get_form(self, step=None, data=None, files=None):
        # SKIP GEOFORM IF NOT NEEDED
        form = super(SubmitChangeWizard, self).get_form(step, data, files)
        if isinstance(form, HistoMapForm):
            typeformdata = self.get_cleaned_data_for_step("0") or {"type":"NewInfo"}
            if not "Transfer" in typeformdata["type"]:
                # skip til after geoform
                self.step = bytes(int(step)+3)
                form = super(SubmitChangeWizard, self).get_form(self.step, data, files)
        elif isinstance(form, GeoChangeForm):
            typeformdata = self.get_cleaned_data_for_step("0") or {"type":"NewInfo"}
            if "Transfer" in typeformdata["type"]:
                wmsdata = self.get_cleaned_data_for_step("4") or {}
                wms = wmsdata.get("transfer_source")
                if wms:
                    wms = wms.split("?")[0]+"?service=wms&format=image/png" # trim away junk wms params and ensure uses transparency
                    form.fields['transfer_geom'].widget.wms = wms
        return form
        
    def get_template_names(self):
        return ["provchanges/submitchange.html"]

    def done(self, form_list, form_dict, **kwargs):
        # NOT YET DONE...
        print form_list, form_dict, kwargs
        
        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
        formfieldvalues = dict(((k,v) for form in form_list for k,v in form.cleaned_data.items() if k in fieldnames))
        formfieldvalues["user"] = self.request.user.username
        formfieldvalues["added"] = datetime.date.today()
        formfieldvalues["bestversion"] = True
        print formfieldvalues

        obj = ProvChange.objects.create(**formfieldvalues)
        obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions
        print obj
        
        obj.save()
        html = redirect("/provchanges/%s/view/" % obj.pk)

        return html

