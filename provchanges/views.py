from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import Template,Context,RequestContext
from django.template.loader import get_template
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import admin

from django.utils.http import urlquote, urlencode

from django.core.paginator import Paginator

from rest_framework import response
from rest_framework.decorators import api_view

from formtools.wizard.views import SessionWizardView

from .models import ProvChange, Vouch, Comment, Source, Map
from provshapes.models import ProvShape

from django.db.models import Count

import datetime
import urllib2


# Create your views here.

countries = [(u'Afghanistan', u'Afghanistan'), (u'\xc5land Islands', u'\xc5land Islands'), (u'Albania', u'Albania'), (u'Algeria', u'Algeria'), (u'American Samoa', u'American Samoa'), (u'Andorra', u'Andorra'), (u'Angola', u'Angola'), (u'Anguilla', u'Anguilla'), (u'Antigua and Barbuda', u'Antigua and Barbuda'), (u'Argentina', u'Argentina'), (u'Armenia', u'Armenia'), (u'Aruba', u'Aruba'), (u'Australia', u'Australia'), (u'Austria', u'Austria'), (u'Azerbaijan', u'Azerbaijan'), (u'The Bahamas', u'The Bahamas'), (u'Bahrain', u'Bahrain'), (u'Bangladesh', u'Bangladesh'), (u'Barbados', u'Barbados'), (u'Belarus', u'Belarus'), (u'Belgium', u'Belgium'), (u'Belize', u'Belize'), (u'Benin', u'Benin'), (u'Bermuda', u'Bermuda'), (u'Bhutan', u'Bhutan'), (u'Bolivia', u'Bolivia'), (u'Bonaire', u'Bonaire'), (u'Bosnia and Herzegovina', u'Bosnia and Herzegovina'), (u'Botswana', u'Botswana'), (u'Bouvet Island', u'Bouvet Island'), (u'Brazil', u'Brazil'), (u'British Indian Ocean Territory', u'British Indian Ocean Territory'), (u'United States Minor Outlying Islands', u'United States Minor Outlying Islands'), (u'British Virgin Islands', u'British Virgin Islands'), (u'Brunei', u'Brunei'), (u'Bulgaria', u'Bulgaria'), (u'Burkina Faso', u'Burkina Faso'), (u'Burundi', u'Burundi'), (u'Cambodia', u'Cambodia'), (u'Cameroon', u'Cameroon'), (u'Canada', u'Canada'), (u'Cape Verde', u'Cape Verde'), (u'Cayman Islands', u'Cayman Islands'), (u'Central African Republic', u'Central African Republic'), (u'Chad', u'Chad'), (u'Chile', u'Chile'), (u'China', u'China'), (u'Christmas Island', u'Christmas Island'), (u'Cocos (Keeling) Islands', u'Cocos (Keeling) Islands'), (u'Colombia', u'Colombia'), (u'Comoros', u'Comoros'), (u'Republic of the Congo', u'Republic of the Congo'), (u'Democratic Republic of the Congo', u'Democratic Republic of the Congo'), (u'Cook Islands', u'Cook Islands'), (u'Costa Rica', u'Costa Rica'), (u'Croatia', u'Croatia'), (u'Cuba', u'Cuba'), (u'Cura\xe7ao', u'Cura\xe7ao'), (u'Cyprus', u'Cyprus'), (u'Czech Republic', u'Czech Republic'), (u'Denmark', u'Denmark'), (u'Djibouti', u'Djibouti'), (u'Dominica', u'Dominica'), (u'Dominican Republic', u'Dominican Republic'), (u'Ecuador', u'Ecuador'), (u'Egypt', u'Egypt'), (u'El Salvador', u'El Salvador'), (u'Equatorial Guinea', u'Equatorial Guinea'), (u'Eritrea', u'Eritrea'), (u'Estonia', u'Estonia'), (u'Ethiopia', u'Ethiopia'), (u'Falkland Islands', u'Falkland Islands'), (u'Faroe Islands', u'Faroe Islands'), (u'Fiji', u'Fiji'), (u'Finland', u'Finland'), (u'France', u'France'), (u'French Guiana', u'French Guiana'), (u'French Polynesia', u'French Polynesia'), (u'French Southern and Antarctic Lands', u'French Southern and Antarctic Lands'), (u'Gabon', u'Gabon'), (u'The Gambia', u'The Gambia'), (u'Georgia', u'Georgia'), (u'Germany', u'Germany'), (u'Ghana', u'Ghana'), (u'Gibraltar', u'Gibraltar'), (u'Greece', u'Greece'), (u'Greenland', u'Greenland'), (u'Grenada', u'Grenada'), (u'Guadeloupe', u'Guadeloupe'), (u'Guam', u'Guam'), (u'Guatemala', u'Guatemala'), (u'Guernsey', u'Guernsey'), (u'Guinea', u'Guinea'), (u'Guinea-Bissau', u'Guinea-Bissau'), (u'Guyana', u'Guyana'), (u'Haiti', u'Haiti'), (u'Heard Island and McDonald Islands', u'Heard Island and McDonald Islands'), (u'Honduras', u'Honduras'), (u'Hong Kong', u'Hong Kong'), (u'Hungary', u'Hungary'), (u'Iceland', u'Iceland'), (u'India', u'India'), (u'Indonesia', u'Indonesia'), (u'Ivory Coast', u'Ivory Coast'), (u'Iran', u'Iran'), (u'Iraq', u'Iraq'), (u'Republic of Ireland', u'Republic of Ireland'), (u'Isle of Man', u'Isle of Man'), (u'Israel', u'Israel'), (u'Italy', u'Italy'), (u'Jamaica', u'Jamaica'), (u'Japan', u'Japan'), (u'Jersey', u'Jersey'), (u'Jordan', u'Jordan'), (u'Kazakhstan', u'Kazakhstan'), (u'Kenya', u'Kenya'), (u'Kiribati', u'Kiribati'), (u'Kuwait', u'Kuwait'), (u'Kyrgyzstan', u'Kyrgyzstan'), (u'Laos', u'Laos'), (u'Latvia', u'Latvia'), (u'Lebanon', u'Lebanon'), (u'Lesotho', u'Lesotho'), (u'Liberia', u'Liberia'), (u'Libya', u'Libya'), (u'Liechtenstein', u'Liechtenstein'), (u'Lithuania', u'Lithuania'), (u'Luxembourg', u'Luxembourg'), (u'Macau', u'Macau'), (u'Republic of Macedonia', u'Republic of Macedonia'), (u'Madagascar', u'Madagascar'), (u'Malawi', u'Malawi'), (u'Malaysia', u'Malaysia'), (u'Maldives', u'Maldives'), (u'Mali', u'Mali'), (u'Malta', u'Malta'), (u'Marshall Islands', u'Marshall Islands'), (u'Martinique', u'Martinique'), (u'Mauritania', u'Mauritania'), (u'Mauritius', u'Mauritius'), (u'Mayotte', u'Mayotte'), (u'Mexico', u'Mexico'), (u'Federated States of Micronesia', u'Federated States of Micronesia'), (u'Moldova', u'Moldova'), (u'Monaco', u'Monaco'), (u'Mongolia', u'Mongolia'), (u'Montenegro', u'Montenegro'), (u'Montserrat', u'Montserrat'), (u'Morocco', u'Morocco'), (u'Mozambique', u'Mozambique'), (u'Myanmar', u'Myanmar'), (u'Namibia', u'Namibia'), (u'Nauru', u'Nauru'), (u'Nepal', u'Nepal'), (u'Netherlands', u'Netherlands'), (u'New Caledonia', u'New Caledonia'), (u'New Zealand', u'New Zealand'), (u'Nicaragua', u'Nicaragua'), (u'Niger', u'Niger'), (u'Nigeria', u'Nigeria'), (u'Niue', u'Niue'), (u'Norfolk Island', u'Norfolk Island'), (u'North Korea', u'North Korea'), (u'Northern Mariana Islands', u'Northern Mariana Islands'), (u'Norway', u'Norway'), (u'Oman', u'Oman'), (u'Pakistan', u'Pakistan'), (u'Palau', u'Palau'), (u'Palestine', u'Palestine'), (u'Panama', u'Panama'), (u'Papua New Guinea', u'Papua New Guinea'), (u'Paraguay', u'Paraguay'), (u'Peru', u'Peru'), (u'Philippines', u'Philippines'), (u'Pitcairn Islands', u'Pitcairn Islands'), (u'Poland', u'Poland'), (u'Portugal', u'Portugal'), (u'Puerto Rico', u'Puerto Rico'), (u'Qatar', u'Qatar'), (u'Republic of Kosovo', u'Republic of Kosovo'), (u'R\xe9union', u'R\xe9union'), (u'Romania', u'Romania'), (u'Russia', u'Russia'), (u'Rwanda', u'Rwanda'), (u'Saint Barth\xe9lemy', u'Saint Barth\xe9lemy'), (u'Saint Helena', u'Saint Helena'), (u'Saint Kitts and Nevis', u'Saint Kitts and Nevis'), (u'Saint Lucia', u'Saint Lucia'), (u'Saint Martin', u'Saint Martin'), (u'Saint Pierre and Miquelon', u'Saint Pierre and Miquelon'), (u'Saint Vincent and the Grenadines', u'Saint Vincent and the Grenadines'), (u'Samoa', u'Samoa'), (u'San Marino', u'San Marino'), (u'S\xe3o Tom\xe9 and Pr\xedncipe', u'S\xe3o Tom\xe9 and Pr\xedncipe'), (u'Saudi Arabia', u'Saudi Arabia'), (u'Senegal', u'Senegal'), (u'Serbia', u'Serbia'), (u'Seychelles', u'Seychelles'), (u'Sierra Leone', u'Sierra Leone'), (u'Singapore', u'Singapore'), (u'Sint Maarten', u'Sint Maarten'), (u'Slovakia', u'Slovakia'), (u'Slovenia', u'Slovenia'), (u'Solomon Islands', u'Solomon Islands'), (u'Somalia', u'Somalia'), (u'South Africa', u'South Africa'), (u'South Georgia', u'South Georgia'), (u'South Korea', u'South Korea'), (u'South Sudan', u'South Sudan'), (u'Spain', u'Spain'), (u'Sri Lanka', u'Sri Lanka'), (u'Sudan', u'Sudan'), (u'Suriname', u'Suriname'), (u'Svalbard and Jan Mayen', u'Svalbard and Jan Mayen'), (u'Swaziland', u'Swaziland'), (u'Sweden', u'Sweden'), (u'Switzerland', u'Switzerland'), (u'Syria', u'Syria'), (u'Taiwan', u'Taiwan'), (u'Tajikistan', u'Tajikistan'), (u'Tanzania', u'Tanzania'), (u'Thailand', u'Thailand'), (u'East Timor', u'East Timor'), (u'Togo', u'Togo'), (u'Tokelau', u'Tokelau'), (u'Tonga', u'Tonga'), (u'Trinidad and Tobago', u'Trinidad and Tobago'), (u'Tunisia', u'Tunisia'), (u'Turkey', u'Turkey'), (u'Turkmenistan', u'Turkmenistan'), (u'Turks and Caicos Islands', u'Turks and Caicos Islands'), (u'Tuvalu', u'Tuvalu'), (u'Uganda', u'Uganda'), (u'Ukraine', u'Ukraine'), (u'United Arab Emirates', u'United Arab Emirates'), (u'United Kingdom', u'United Kingdom'), (u'United States', u'United States'), (u'Uruguay', u'Uruguay'), (u'Uzbekistan', u'Uzbekistan'), (u'Vanuatu', u'Vanuatu'), (u'Venezuela', u'Venezuela'), (u'Vietnam', u'Vietnam'), (u'Wallis and Futuna', u'Wallis and Futuna'), (u'Western Sahara', u'Western Sahara'), (u'Yemen', u'Yemen'), (u'Zambia', u'Zambia'), (u'Zimbabwe', u'Zimbabwe')]

def advancedchanges(request):
    bannertitle = "Advanced Change View"
    
    grids = []

    fields = [f.name for f in ProvChange._meta.get_fields()]
    changes = ProvChange.objects.filter(status__in="Pending Active".split())
    content = model2table(request, "Title", changes, fields)
    
    grids.append(dict(title="Change Table:",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none; overflow:scroll",
                      width="99%",
                      ))
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           }
                  )

# Comments

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = 'user country changeid added status title text'.split()
        widgets = {"text":forms.Textarea(attrs=dict(style="font-family:inherit",cols=90,rows=5)),
                   'user':forms.HiddenInput(),
                   'country':forms.HiddenInput(),
                   'changeid':forms.HiddenInput(),
                   'added':forms.HiddenInput(),
                   'status':forms.HiddenInput(),
                   }

class ReplyForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = 'user country changeid added status title text'.split()
        widgets = {"text":forms.Textarea(attrs=dict(style="font-family:inherit",cols=90,rows=5)),
                   'title':forms.HiddenInput(),
                   'user':forms.HiddenInput(),
                   'country':forms.HiddenInput(),
                   'changeid':forms.HiddenInput(),
                   'added':forms.HiddenInput(),
                   'status':forms.HiddenInput(),
                   }

@login_required
def addcomment(request):
    data = request.POST
    if data.get('changeid'):
        # change-specific comment
        commentinst = Comment(user=request.user.username, country=data['country'], changeid=data['changeid'],
                            added=datetime.datetime.now(),
                              title=data['title'], text=data['text'])
        commentinst.save()
        print 'change-specific comment added'
    else:
        # country comment
        commentinst = Comment(user=request.user.username, country=data['country'],
                            added=datetime.datetime.now(),
                              title=data['title'], text=data['text'])
        commentinst.save()
        print 'country comment added'
    return redirect(request.META['HTTP_REFERER'])

@login_required
def dropcomment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.username == comment.user:
        comment.status = 'Withdrawn'
        comment.save()
        print 'comment dropped'
    return redirect(request.META['HTTP_REFERER'])


# Vouches

@login_required
def addvouch(request, pk):
    # pk belongs to provchange
    change = get_object_or_404(ProvChange, pk=pk)
    if request.user.username != change.user:
        # can only vouch for others' provchange, not your own...
        vouch = next(iter(Vouch.objects.filter(user=request.user.username, changeid=change.changeid)), None)
        if vouch:
            # vouch already exists
            vouch.status = "Active"
            vouch.save()
        else:
            # create new vouch
            vouch = Vouch(user=request.user.username, changeid=change.changeid, added=datetime.datetime.now())
            vouch.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def withdrawvouch(request, pk):
    vouch = get_object_or_404(Vouch, user=request.user.username, changeid=pk)
    if request.user.username == vouch.user:
        vouch.status = "Withdraw"
        vouch.save()
    return redirect(request.META['HTTP_REFERER'])


# Sources

def get_country_sources(country):
    sources = Source.objects.filter(status='Active').order_by('title')
    if not country:
        for s in sources:
            if not s.country:
                # only non-country-specific
                yield s
    else:
        countries = [cn.strip().lower() for cn in country.split('|') if cn.strip()]
        for s in sources:
            scountries = [cn.strip().lower() for cn in s.country.split('|') if cn.strip()]
            if any((cn in scountries for cn in countries)):
                # if in countrylist
                yield s

class SourceForm(forms.ModelForm):

    class Meta:
        model = Source
        fields = 'status title citation note url country'.split()
        widgets = {"country":forms.TextInput(attrs=dict(style="width:98%")),
                   "title":forms.TextInput(attrs=dict(style="width:98%")),
                   "citation":forms.Textarea(attrs=dict(style="font-family:inherit")),
                   "note":forms.Textarea(attrs=dict(style="font-family:inherit")),
                   #"country":forms.HiddenInput(),
                   }

    def as_custom(self):
        return get_template("provchanges/sourceform.html").render({'sourceform':self})

##    def as_griditem(self):
##        source = self.instance
##        color = 'rgb(122,122,122)'
##        griditem = """
##                <a href="/viewsource/{pk}/" style="text-decoration:none; color:inherit;">
##                    <div class="griditem" style="float:left; width:200px; margin:10px">
##                        <div class="gridheader" style="background-color:{color}; padding-top:10px">
##                            <img src="http://www.pvhc.net/img28/hgicvxtrvbwmfpuozczo.png" height="40px">
##                            <h4 style="display:inline-block">{title}</h4>
##                        </div>
##                        
##                        <div class="gridcontent">
##                            <p>{citation}</p>
##                        </div>
##                    </div>
##                </a>
##                    """.format(title=source.title, citation=source.citation, pk=source.pk, color=color)
##        return griditem

@login_required
def addsource(request):
    if request.method == "GET":
        # new empty form
        sourceform = SourceForm(initial=request.GET.dict())
        return render(request, "provchanges/addsource.html", {'sourceform':sourceform})
    
    elif request.method == "POST":
        # save submitted info
        fields = [f.name for f in Source._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fields))
        formfieldvalues.update(added=datetime.datetime.now(),
                               modified=datetime.datetime.now())
        print formfieldvalues
        src = Source(**formfieldvalues)
        src.save()
        # TODO: find way to refer back to referrer, http_refererer doesnt work...
        return redirect("/viewsource/%s" % src.pk)

@login_required
def viewsource(request, pk):
    obj = get_object_or_404(Source, pk=pk)
    sourceform = SourceForm(instance=obj)
    for field in sourceform.fields.values():
        field.disabled = True
        field.widget.disabled = True
        field.widget.attrs['readonly'] = 'readonly'
    return render(request, "provchanges/viewsource.html", {'sourceform':sourceform, 'pk':obj.pk})

@login_required
def editsource(request, pk):
    obj = get_object_or_404(Source, pk=pk)
    if request.method == "GET":
        sourceform = SourceForm(instance=obj)
        return render(request, "provchanges/editsource.html", {'sourceform':sourceform, 'pk':obj.pk})

    elif request.method == "POST":
        # save submitted info
        fields = [f.name for f in Source._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fields))
        formfieldvalues.update(modified=datetime.datetime.now())
        print formfieldvalues
        for k,v in formfieldvalues.items():
            setattr(obj, k, v)
        obj.save()
        return redirect("/viewsource/%s" % obj.pk)

@login_required
def dropsource(request, pk):
    obj = get_object_or_404(Source, pk=pk)
    obj.status = "Withdrawn"
    obj.modified = datetime.datetime.now()
    obj.save()
    return redirect("/viewsource/%s" % obj.pk)


# Maps

def get_country_maps(country):
    maps = Map.objects.filter(status='Active').order_by('year','title')
    if not country:
        for m in maps:
            if not m.country:
                # only non-country-specific
                yield s
    else:
        countries = [cn.strip().lower() for cn in country.split('|') if cn.strip()]
        for m in maps:
            mcountries = [cn.strip().lower() for cn in m.country.split('|') if cn.strip()]
            if any((cn in mcountries for cn in countries)):
                # if in countrylist
                yield m
    
class MapForm(forms.ModelForm):

    class Meta:
        model = Map
        fields = 'status title year country note source url wms'.split()
        widgets = {"country":forms.TextInput(attrs=dict(style="width:98%")),
                   "note":forms.Textarea(attrs=dict(style="font-family:inherit")),
                   #"country":forms.HiddenInput(),
                   }

    def __init__(self, *args, **kwargs):
        super(MapForm, self).__init__(*args, **kwargs)

        # new
        if 'initial' in kwargs and kwargs["initial"].get('country'):
            # means country was set in GET param, so get only sources relevant for that country
            country = kwargs["initial"]["country"]
            sources = get_country_sources(country)
        elif 'instance' in kwargs and kwargs["instance"].country:
            # means country was set in existing instance (edit mode), so get only sources relevant for that country
            country = kwargs["instance"].country
            sources = get_country_sources(country)
        else:
            # NOTE: This prob should never be the case...
            # get only the global sources
            sources = get_country_sources("")
        #choices = [(s.pk, SourceForm(instance=s).as_griditem()) for s in sources]
        choices = [(s.pk, "{title} - {citation}".format(title=s.title.encode('utf8'), citation=s.citation.encode('utf8'))) for s in sources]
        #self.fields["source"].widget = GridSelectOneWidget(choices=choices)
        self.fields["source"].widget = forms.Select(choices=[('','')]+choices, attrs=dict(style="width:99%")) 

        wms = self.instance.wms
        if wms:
            try:
                self.wms_helper = WMS_Helper(wms)
            except:
                self.wms_helper = None # something went wrong, skip gracefully

    def as_custom(self):
        wms = self.instance.wms
        if wms and self.wms_helper:
            extent = self.wms_helper.bbox
##            params = self.wms_helper.get_link_params(width=400)
##            wmslink = wms + "?" + params
##            wmsimage = '<img src="{wmslink}" width="40%">'.format(wmslink=wmslink)
        else:
            extent = None
##            wmslink = "http://icons.iconarchive.com/icons/icons8/android/512/Maps-Map-Marker-icon.png"
##            wmsimage = '<img src="{wmslink}" style="opacity:0.1; width:40%">'.format(wmslink=wmslink)
        return get_template("provchanges/mapform.html").render({'mapform':self, 'extent':extent})

##    def as_griditem(self):
##        mapp = self.instance
##        wms = self.instance.wms
##        if wms and self.wms_helper:
##            params = self.wms_helper.get_link_params(height=40)
##            wmslink = wms + "?" + params
##            wmsimage = '<img src="{wmslink}" height="40px">'.format(wmslink=wmslink)
##        else:
##            wmslink = "http://icons.iconarchive.com/icons/icons8/android/512/Maps-Map-Marker-icon.png"
##            wmsimage = '<img src="{wmslink}" style="opacity:0.1; height:40px">'.format(wmslink=wmslink)
##        color = 'rgb(58,177,73)'
##        griditem = """
##                <a href="/viewmap/{pk}/" style="text-decoration:none; color:inherit;">
##                    <div class="griditem" style="float:left; width:200px; margin:10px">
##                        <div class="gridheader" style="background-color:{color}; padding:10px;">
##                            {wmsimage}
##                            <h4 style="display:inline-block">{year}</h4>
##                        </div>
##                        
##                        <div class="gridcontent">
##                            <p>{title}</p>
##                        </div>
##                    </div>
##                </a>
##                    """.format(year=mapp.year, title=mapp.title, note=mapp.note, wmsimage=wmsimage, pk=mapp.pk, color=color)
##        return griditem

class WMS_Helper:
    def __init__(self, url):
        self.url = url
        wmsmeta = urllib2.urlopen(url+"?service=wms&request=getcapabilities").read()
        bbox = wmsmeta.split('<BoundingBox SRS="EPSG:4326"')[-1].strip().split()[:4] # hacky, can be multiple, just choosing last
        self.bbox = [float(xory.split('=')[-1].strip('"')) for xory in bbox]

    def image_url(self, width=None, height=None):
        bbox = self.bbox
        if width and height:
            pass
        elif height:
            ratio = (bbox[2]-bbox[0]) / (bbox[3]-bbox[1])
            width = height * ratio
        elif width:
            ratio = (bbox[3]-bbox[1]) / (bbox[2]-bbox[0])
            height = width * ratio
        else:
            raise Exception('Either width or height must be set')
        # Note: better to get unrectified, via "&STATUS=unwarped", but in that case not sure how to find raw image bbox (ie width & height)
        params = "service=wms&version=1.1.1&request=getmap&format=image/png&srs=EPSG%3A4326&bbox={bbox}&width={width}&height={height}".format(bbox=",".join(map(str,self.bbox)), width=width, height=height)
        return self.url + "?" + params

@login_required
def addmap(request):
    if request.method == "GET":
        # new empty form
        mapform = MapForm(initial=request.GET.dict())
        return render(request, "provchanges/addmap.html", {'mapform':mapform})
    
    elif request.method == "POST":
        # save submitted info
        fields = [f.name for f in Map._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fields))
        formfieldvalues.update(added=datetime.datetime.now(),
                               modified=datetime.datetime.now())

        sourceid = formfieldvalues['source']
        sourceobj = get_object_or_404(Source, pk=sourceid) if sourceid else None
        formfieldvalues['source'] = sourceobj
        
        print formfieldvalues
        obj = Map(**formfieldvalues)
        obj.save()
        # TODO: find way to refer back to referrer, http_refererer doesnt work...
        return redirect("/viewmap/%s" % obj.pk)

@login_required
def viewmap(request, pk):
    obj = get_object_or_404(Map, pk=pk)
    mapform = MapForm(instance=obj)
    for field in mapform.fields.values():
        field.disabled = True
        field.widget.disabled = True
        field.widget.attrs['readonly'] = 'readonly'
    return render(request, "provchanges/viewmap.html", {'mapform':mapform, 'pk':obj.pk})

@login_required
def editmap(request, pk):
    obj = get_object_or_404(Map, pk=pk)
    if request.method == "GET":
        mapform = MapForm(instance=obj, initial=request.GET.dict())
        return render(request, "provchanges/editmap.html", {'mapform':mapform, 'pk':obj.pk})

    elif request.method == "POST":
        # save submitted info
        fields = [f.name for f in Map._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fields))
        formfieldvalues.update(modified=datetime.datetime.now())
        
        sourceid = formfieldvalues.pop('source')
        sourceobj = get_object_or_404(Source, pk=sourceid) if sourceid else None
        formfieldvalues['source'] = sourceobj
        print formfieldvalues
        for k,v in formfieldvalues.items():
            setattr(obj, k, v)
            
        obj.save()
        return redirect("/viewmap/%s" % obj.pk)

@login_required
def dropmap(request, pk):
    obj = get_object_or_404(Map, pk=pk)
    obj.status = "Withdrawn"
    obj.modified = datetime.datetime.now()
    obj.save()
    return redirect("/viewmap/%s" % obj.pk)




        
##################

def slideshow():
    # from https://codepen.io/anon/pen/RGYPjP
    html = """
            //how many images we have
            $slides: 4;

            // how much we want each slide to show
            $time_per_slide: 4;

            // total time needed for full animation
            $total_animation_time: $time_per_slide * $slides;

            body{
              background:#000;
            }
            .container{
              margin:50px auto;
              width:500px;
              height:300px;
              overflow:hidden;
              border:10px solid;
              border-top-color:#856036;
              border-left-color:#5d4426;
              border-bottom-color:#856036;
              border-right-color:#5d4426;
              position:relative;

            }
            .photo{
              position:absolute;
              animation:round #{$total_animation_time}s infinite;
              opacity:0;
              
            }
            @keyframes round{   
              25%{
                opacity:1;
              }
              40%{
                opacity:0;
              }
            } 

            @for $index from 1 to $slides + 1{
              img:nth-child(#{$index}){
                animation-delay:#{$total_animation_time - $time_per_slide * $index}s
              }
            }
               
            <div class="container">
              <img class='photo'  src="http://farm9.staticflickr.com/8320/8035372009_7075c719d9.jpg" alt="" />
              <img class='photo'  src="http://farm9.staticflickr.com/8517/8562729616_35b1384aa1.jpg" alt="" />
              <img class='photo'  src="http://farm9.staticflickr.com/8465/8113424031_72048dd887.jpg" alt="" />
              <img class='photo'  src="http://farm9.staticflickr.com/8241/8562523343_9bb49b7b7b.jpg" alt="" />

            </div>
            """
    return html

class Grid:
    html = ""
    def add_cell(self, title, content, style="border-style:none", width="30%"):
        self.html += """
                    <div class="gridcell" style="float:left; width:{width}; padding-right:3%">
                            <h4>{title}</h4>
                            <div style="border-style:solid; border-color:black; border-radius:10px; padding:3% 5%; background-size:100% 100%; {style}">
                            {content}
                            </div>
                    </div>
                    """.format(title=title.encode("utf8"), content=content.encode("utf8"), style=style.encode("utf8"), width=width.encode("utf8"))

def registration(request):
    
    if request.method == "POST":
        print "data",request.POST
        fieldnames = [f.name for f in User._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))
        print formfieldvalues
        obj = User.objects.create_user(**formfieldvalues)
        print obj
        obj.save()

        html = redirect("/contribute/countries/")

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
            html = redirect("/contribute/countries/")
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

##guidelines_header = """
##                    <div style="text-align:left">
##
##                        <br><br><br><br>
##                        <b>
##                        All contributors should read the following guidelines, and refer
##                        back to them whenever you face a difficult coding decision. 
##                        </b>
##
##                        <style>
##                            #blackbackground a { color:white }
##                            #blackbackground a:visited { color:white }
##                        </style>
##
##                        <ul id="blackbackground">
##                        <li><a href="/guidelines/understanding/">Understanding Pshapes</a></li>
##                        <li><a href="/guidelines/codingrules/">Coding Rules</a></li>
##                        <li><a href="/guidelines/mapping/">Mapping</a></li>
##                        </ul>
##
##                    </div>
##                    """
##
##def guidelines_understanding(request):
##    bannertitle = "Guidelines - Understanding Pshapes:"
##    
##    bannerleft = """
##                    <div style="text-align:center">
##                        <img width="100%" border="0" src="http://r.hswstatic.com/w_404/gif/reading-topographic-map-quiz-558947465.jpg">
##		    </div>
##    """
##
##    bannerright = guidelines_header
##
##    grids = []
##
##    # SUBPAGE: UNDERSTANDING PSHAPES
##
##    grids.append(dict(title="How the Algorithm Works",
##                      content="""
##                                <p>
##                                Pshapes is primarily just a dataset of province-related <em>changes</em> and not a boundary dataset per se.
##                                However, the data collection effort was developed in conjunction with a computer algorithm that was
##                                designed to use this change information to create a complete historical boundary dataset.
##                                </p>
##
##                                <p>
##                                The algorithm starts by asking for a
##                                complete global dataset of province boundaries reflecting how the situation looks like
##                                on a given (preferably recent) date. This can be any third-party dataset, including the ones listed earlier. 
##                                It then increments through the events listed in the Pshapes change-data, starting with the
##                                most recent and going gradually further back in time. 
##                                </p>
##
##                                <p>
##                                The Pshapes change-events are processed as they are encountedered, and can be boiled down to three basic types.
##                                </p>
##
##                                <ol>
##
##                                <li>
##                                <b>NewInfo</b>
##                                Most changes simply involve changes to a province name or code. These events are handled
##                                by simply noting the start-date of the existing modern province, and then adding a new province
##                                that ends on that same date. Any subsequent changes involving that province will in turn result in
##                                registering its start-date, before again adding the next historical iteration of that province.
##                                <br><br>
##                                </li>
##
##                                <li>
##                                <b>Splits</b>
##                                If on a given date a split event was registered, this means that the current state of our boundary
##                                dataset contains all the resulting breakaway
##                                provinces and that these used to belong to a single large province. To
##                                recreate this older province all we have to do is glue together the geometries of the provinces
##                                that were registered as splitting away (incl. the remnants of the original province in case
##                                the split was incomplete).
##                                <br><br>
##                                </li>
##                                
##                                <li>
##                                <b>Transfers and Mergers</b>
##                                The last type of change include events where a province receives territory from one or
##                                more other provinces. 
##                                If the receiving province was pre-existing then we are talking about a partial transfer of
##                                territory. Since our boundary data represents the larger version of the province after it
##                                received the territory, all that is needed is to cut off the piece that was received (based on a
##                                cookie-cutter polygon that users draw when encountering such events) and glue it
##                                back together to the province that originally gave away the territory.
##                                The same principle applies if the receiving province did not previously exist but instead came
##                                into existence as a result of two or more such transfers.
##                                Finally, transfers can also involve the full transfer of entire provinces that afterwards cease to exist.
##                                These are often known as mergers or annexations, but they are handled in the same way as other transfers
##                                of territories: cut it off and give it back to its previous owner.
##                                <br><br>
##                                </li>
##
##                                </ol>
##
##                                <p>
##                                Multiple complex configuratios of these changes can occur in a single event,
##                                and when processed in this way, the jigzaw puzzle of broken off parts and changing
##                                ownerships will reorganize itself to recreate how the provinces
##                                looked prior to the event. 
##
##                                <p>
##                                Through this process we can reverse geocode our
##                                way back in time for as long as we have a continuous list of changes. 
##                                </p>
##                            """,
##                      width="98%",
##                      ))
##
##    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
##                                                           "bannerleft":bannerleft, "bannerright":bannerright}
##                  )
##
##def guidelines_codingrules(request):
##    bannertitle = "Guidelines - Coding Rules:"
##    
##    bannerleft = """
##                    <div style="text-align:center">
##                        <img width="100%" border="0" src="http://r.hswstatic.com/w_404/gif/reading-topographic-map-quiz-558947465.jpg">
##		    </div>
##    """
##
##    bannerright = guidelines_header
##
##    grids = []
##
##
##    content = """
##                <h4>Disputed Countries/Territories</h4>
##                <p>
##                What defines a country? At all times follow the most internationally recognized country-units and names.
##                For territories under foreign colonial rule, these should be coded as separate from the ruling
##                power. For countries simply achieving independence or countries with only minor changes in their official name,
##                avoid changing the country name. 
##                </p>
##                
##                <h4>Historical Countries</h4>
##                <p>
##                One of the advantages of the Pshapes project is that we should be able to go back in time as far back
##                as we have information. So when encountering historic countries that don't exist anymore, the way to go
##                about this is to register the event as usual, and then change the from-country field.
##                For instance, for each of the ex-Soviet
##                countries all of their provinces must be registered as changing info from the Soviet Union. The new country
##                name as you have written it will appear in the list of countries, so you can keep tracking it further back
##                in time.
##                </p>
##                """
##
##    grids.append(dict(title="Defining Countries",
##                      content=content,
##                      #style="background-color:orange; margins:0 0; padding: 0 0; border-style:none",
##                      width="98%",
##                      ))
##
##    content = """
##                <h4>Admin Levels</h4>
##                <p>
##                In its first run, the Pshapes project is only collecting data on the first-level
##                administrative areas, the highest level in a country. Typically they are given names
##                like "province", "state", "district", or a local language equivalent. 
##
##                Some countries have a special administrative level between the national and 1st level,
##                often referred to as "regions".
##                These tend to be so big that sometimes there are only two of them. 
##                In Pshapes we prefer to ignore these regions and instead focus on the level below. 
##                When in doubt follow a rule that they should be small enough to provide good variation within
##                the country and big enough that it is feasible to get complete information on all of its changes.
##                </p>
##                
##                <h4>Cross-Country Changes</h4>
##                <p>
##                Sometimes you will come across cases where a change involves more than one country name. Territory
##                might be transferred to or change ownership from one country to another. In those cases, register as
##                usual, and then change the from-country field.
##                </p>
##
##                <h4>Minor Transfers</h4>
##                <p>
##                In some countries, some transfers of territory may be listed with the names of level-2 areas, and these
##                should just be listed as partial territorial transfers and drawn roughly by hand. 
##                However, if the change seems very small, or if there are too many of these types of minor changes,
##                it is okay to ignore most of them and only focus on the big changes. 
##                </p>
##                """
##
##    grids.append(dict(title="Coding Rules",
##                      content=content,
##                      #style="background-color:orange; margins:0 0; padding: 0 0; border-style:none",
##                      width="98%",
##                      ))
##
##    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
##                                                           "bannerleft":bannerleft, "bannerright":bannerright}
##                  )
##
##def guidelines_mapping(request):
##    bannertitle = "Guidelines - Mapping:"
##    
##    bannerleft = """
##                    <div style="text-align:center">
##                        <img width="100%" border="0" src="http://r.hswstatic.com/w_404/gif/reading-topographic-map-quiz-558947465.jpg">
##		    </div>
##    """
##
##    bannerright = guidelines_header
##
##    grids = []
##
##    # SUBPAGE: MAPPING CHANGES
##
##    # Map Finder app
##    # NOTE: Map finder brings to screen where also lists websites to find maps, and then the map finder forum...
##    # alt img http://cdn.wallpapersafari.com/7/88/QGsTDo.jpg
##
##    content = """
##            <b>
##            <img width="50%" border="2" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfcsofKnVvMiG0mN7BKmmGlGfM_16ANpxoDMT4MjufR40Ya-ZdfQ">
##
##            <style>
##                #blackbackground a { color:white }
##                #blackbackground a:visited { color:white }
##            </style>
##
##            <p>
##            One of the great things about the Pshapes project is that for the vast majority of province
##            changes we do not need to consult historical maps or use valuable time on geocoding. 
##            </p>
##
##            <p>
##            For some types of changes however there is simply no way around it. In these situations,
##            namely mergers and partial transfers of territory, Pshapes will ask you to draw the spatial extent of a change. 
##            To do this you will need to locate an image file of a historical map and to georeference it at the
##            <a target="_blank" href="http://mapwarper.net/">MapWarper</a> website.
##            Here are some useful sources:
##
##            <ul>
##                <li><a target="_blank" href="http://mapwarper.net/">MapWarper</a></li>
##                <li><a target="_blank" href="http://www.oldmapsonline.org/">OldMapsOnline</a></li>
##                <li><a target="_blank" href="http://www.vidiani.com/tag/administrative-maps/">Vidiani</a></li>
##                <li><a target="_blank" href="http://www.mapsopensource.com">MapsOpenSource.com</a></li>
##                <li><a target="_blank" href="http://www.ezilon.com">Ezilon.com</a></li>
##                <li><a target="_blank" href="https://www.loc.gov/maps/?q=administrative%20divisions">The Library of Congress Map Collection</a></li>
##                <li><a target="_blank" href="https://www.lib.utexas.edu/maps/historical/index.html">The Perry-Castaneda Library Map Collection</a></li>
##                <li><a target="_blank" href="http://alabamamaps.ua.edu/historicalmaps/">Alabama Maps Historical Maps</a></li>
##                <li><a target="_blank" href="http://www.zum.de/whkmla/region/indexa.html">World History at KMLA</a></li>
##                <li><a target="_blank" href="http://www.antiquemapsandprints.com/prints-and-maps-by-country-12-c.asp">Antique Maps and Prints</a></li>
##                <li><a target="_blank" href="http://catalogue.defap-bibliotheque.fr/index.php?lvl=index">La bibliotheque du Defap</a></li>
##                <li><a target="_blank" href="https://books.google.no/books?id=n-xZp-QMKCcC&lpg=PA25&ots=qM9PapNLCF&dq=world%20mapping%20today%20parry&hl=no&pg=PA320#v=onepage&q=world%20mapping%20today%20parry&f=false">"World Mapping Today", by Bob Parry and Chris Perkins</a></li>
##            </ul>
##
##            <em>Note: Make sure the map doesn't have a license that restricts sharing or derivative work.</em>
##
##            </p>
##            </b>
##            """
##
##    grids.append(dict(title="Finding a Map",
##                      content=content,
##                      #style="background-color:orange; margins:0 0; padding: 0 0; border-style:none",
##                      width="98%",
##                      ))
##
##    content = """
##            <b>
##            <img width="50%" src="http://image.slidesharecdn.com/06-clipping-130211003001-phpapp01/95/06-clipping-25-638.jpg?cb=1360542662">
##                <p>
##                Once you have found a map and georeferenced it on MapWarper.org, then it is time
##                to draw to indicate the areas of an existing province that used to belong to an older province. 
##                </p>
##
##                <br>
##                Follow these steps when drawing: 
##                <br>
##                <ol>
##                    <li>
##                    Guided by the map, draw a clipping polygon that encircles the province that gave away territory.
##                    Since we do not know which exact third-party dataset will be used to recreate the final
##                    historical dataset, we need to make sure our clipping polygon is always big enough to include all
##                    parts by drawing with a significant error-margin around the province boundaries.
##                    <br><br>
##                    </li>
##                    <li>
##                    If the giving province only gave away parts of its territory
##                    it's sufficient to just draw around the area that was transferred (e.g. a tiny corner of the province
##                    or a series of islands).
##                    <br><br>
##                    </li>
##                    <li>
##                    Where the giving province shares a border with the
##                    receiving province or any other giving provinces you should follow that border exactly.
##                    <br><br>
##                    </li>
##                    <li>
##                    The clipping polygon will be snapped to any previously drawn giving provinces (shown in gray), so just make
##                    sure it covers every part of that border so that there is no gap in between.
##                    <br><br>
##                    </li>
##                    <li>
##                    Draw multiple polygons if necessary.
##                    <br><br>
##                    </li>
##                </ol>
##                
##            </b>
##            """
##
##    grids.append(dict(title="How to Draw Boundary Changes",
##                      content=content,
##                      #style="background-color:orange; margins:0 0; padding: 0 0; border-style:none",
##                      width="98%",
##                      ))
##
##    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
##                                                           "bannerleft":bannerleft, "bannerright":bannerright}
##                  )




##@login_required
##def community(request):
##    print request, request.user
##    changelist = ProvChange.objects.all()
##    pages = Paginator(changelist, 10)
##
##    page = request.GET.get("page", 1)
##    if page:
##        changelist = pages.page(page)
##    
##    html = render(request, 'provchanges/community.html', {'changelist': changelist})
##    return html
##
##def community(request):
##    changes = ProvChange.objects.all()
##    accepted = ProvChange.objects.filter(status="Accepted")
##    pending = ProvChange.objects.filter(status="Pending")
##    users = User.objects.all()
##    
##    if request.user.is_authenticated():
##        bannertitle = "Welcome to the Pshapes Community Pages"
##        bannerleft = """
##                    <div style="text-align:left">
##                        Here you can check on the progress made and activities of the community, and
##                        help expand the data.
##
##                        <br><br>
##                        <b>Community Stats:</b>
##                            <div style="color:white;">
##                                Total Contributions:
##                                {changes}
##
##                                <br>
##                                Accepted:
##                                {accepted}
##
##                                <br>
##                                Pending:
##                                {pending}
##                                
##                                <br>
##                                Registered Users:
##                                {users}
##                            </div>
##                    </div>
##                            """.format(changes=len(changes), users=len(users),
##                                       accepted=len(accepted), pending=len(pending))
##        bannerright = """
##                    <div style="text-align:left">
##                        <br>
##                        <b>Your most recent notifications:</b>
##                        <br>
##                        <ul>
##                            <li>...</li>
##                            <li>...</li>
##                        </ul>
##                    </div>
##                        """
##        
##    else:
##        bannertitle = "Welcome to the Pshapes Community Pages:"
##        bannerleft = """
##                        <div style="text-align:left">
##                            This is where the Pshapes community can contribute, discuss, and collaborate.
##                            Here you can check on the progress made and activities of the community, and
##                            help expand the data.
##
##                            <br><br>
##                            <b>How Does It Work?</b>
##                            <br>
##                            Users submit contributions, and after a vetting process
##                            the change will be included in the next version of the data available from the website.
##                            You can also browse, quality check, and suggest edits to existing province changes already
##                            submitted by other users.
##
##                            <br><br>
##                            <b>Who is it for?</b>
##                            <br>
##                            Whether you just want to track a recent change in your province, or map out the changes
##                            for an entire country, all contributions count!
##
##                        </div>
##        """
##        bannerright = """
##                        <br><br><br><br>
##                        Help keep track of our changing world.
##                        <br>
##                        <br>
##                        <br>
##                        <a href="/registration" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
##                        Sign Up
##                        </a>
##                        or
##                        <a href="/login" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
##                        Login
##                        </a>
##        """
##    grids = []
##
##    grids.append(dict(title="Recent discussions:",
##                      content="""
##                            ...
##                            """,
##                      ))
##
####    grids.append(dict(title="Submit Change:",
####                      content="""
####                            <a href="/contribute/submitchange" style="color:white;>
####                            <p style="color:black;">
####                            Help expand the data by submitting a new province change.
####                            </p>
####                            </a>
####                            """,
####                      ))
####    grids.append(dict(title="Quality Check:",
####                      content="""
####                            <a href="/contribute/browse" style="color:white;>
####                            <p style="color:black;">
####                            Browse, quality check, or suggest edits to
####                            existing province changes already registered by other users.
####                            </p>
####                            </a>
####                            """,
####                      ))
##    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
##                                                           "bannerleft":bannerleft, "bannerright":bannerright}
##                  )

##def contribute_browse(request):
##    status = request.GET.get("status", "Accepted")
##    changes = ProvChange.objects.filter(status=status).order_by("-added") # the dash reverses the order
##    changestable = model2table(request, title="", objects=changes,
##                              fields=["date","type","fromname","toname","country","user","added","status"])
##    tabstyle = """
##            <style>
##            .curtab {
##                display:table-cell;
##                background-color:orange;
##                color:white;
##                border-radius:10px;
##                padding:10px; 
##                }
##            .tab {
##                display:table-cell;
##                background-color:null;
##                color:black;
##                border-radius:10px;
##                padding:10px;
##                }
##            </style>
##            """
##    
##    tabs = """
##            <div class="{Accepted}"><h4><a href="/contribute/browse?status=Accepted" style="color:inherit">Accepted</a></h4></div>
##            <div class="{Pending}"><h4><a href="/contribute/browse?status=Pending" style="color:inherit">Pending</a></h4></div>
##
##            <br>
##            <br>
##            
##            """.format(Accepted="curtab" if status=="Accepted" else "tab",
##                        Pending="curtab" if status=="Pending" else "tab")
##    content = tabstyle + tabs + changestable
##    
##    grids = []
##    grids.append(dict(title="Browse all province changes:",
##                      content=content,
##                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                      width="99%",
##                      ))
##    
##    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"nomainbanner":True}
##                  )

##def contribute(request):
##    bannertitle = "Contributions at a Glance:"
##
##    from django.db.models import Count
##    changes = ProvChange.objects.all()
##    pending = ProvChange.objects.filter(status="Pending")
##    countrycount = ProvChange.objects.filter(status="Pending").values("fromcountry").distinct().count()
##    users = User.objects.all()
##
##    #<img style="width:70%" src="https://content.linkedin.com/content/dam/blog/en-us/corporate/blog/2011/11/summary.png">
##    bannerleft = """
##                <div>
##                        <div style="text-align:center">
##                            <svg width="100" height="100">
##                              <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />
##                            </svg>
##                        </div>
##		    
##                        <b>
##                        <ul style="text-align:left; list-style-type: none; line-height: 30px;">
##                            <li>
##                            Province changes:
##                            {changes}
##                            </li>
##
##                            <li>
##                            Edits made:
##                            {modifs}
##                            </li>
##
##                            <li>
##                            Countries coded:
##                            {countrycount}
##                            </li>   
##                        </ul>
##                        </b>
##                </div>
##                        """.format(users=len(users),
##                                   changes=len(pending),
##                                   modifs=len(changes)-len(pending),
##                                   countrycount=countrycount,
##                                   )
##
##    #QUOTE
##    #Anyone who has an interest in coding some changes for one or more countries,
##    #should have the ability to do so themselves, regardless of skills or background. 
##
##    bannerright = """
##                    <div style="text-align:left">
##
##                        <br><br>
##                        <h4>Help Collect the Data</h4>
##                        Creating a global dataset of province changes is a tremendous task for any one stakeholder to undertake. 
##                        The Pshapes project is based on the idea that we can collect and maintain province change data more efficiently
##                        and transparently as a community. The idea is that anyone who has an interest in coding some changes for one or more countries,
##                        should have the ability to do so themselves.
##                        Most of the information is already available from our list of online sources, 
##                        making it easy to jump straight into it with little or no background-knowledge. 
##                        In most cases all that is required is filling out some forms. 
##
##                        <br><br>
##                        <a href="/contribute/countries" style="float:left; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
##                        Get Started
##                        </a>
##
##
##                    </div>
##    """
##
##    grids = []
##    
##    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
##                                                           "bannerleft":bannerleft, "bannerright":bannerright}
##                  )



##                                <p>
##                                Are you someone who loves working with geographic and historical data? 
##                                Do you need historical boundaries for a particular project?
##                                Maybe you have a rare historical document or map and want to extend
##                                the historical coverage?
##                                Or perhaps you are a historian or expert on a country or region
##                                and want to quality check what others have already contributed? 
##                                </p>

GUIDE = """
                        <style>
                            #blackbackground a { color:white }
                            #blackbackground a:visited { color:grey }
                        </style>
                        
                        <div id="blackbackground" style="text-align: left;">


                        <b>
                        <a id="instrnext" style="float:right; padding:5px" href="javascript: nextstep()">Next</a>
                        <a id="instrprev" style="float:right; padding:5px" href="javascript: prevstep()">Prev</a>
                        </b>

                        <h3><br></h3>

                        <style>
                        .instrnotsel {
                            font-size: medium;
                        }
                        .instrsel {
                            font-size: xx-large;
                        }
                        </style>

                        <script>
                        function showinstruction(num) {
                            var steps = document.getElementById("instrsteps").children
                            for (var i = 0; i < steps.length; i++) {
                                var step = steps[i];
                                step.style.display = "none";
                            };
                            document.getElementById("instrstepheader").innerHTML = num;
                            document.getElementById("instr"+num).style.display = "block";
                            
                            if (num == 1) {
                                document.getElementById("instrprev").href = "javascript: void(0)";
                            } else if (num == steps.length) {
                                document.getElementById("instrnext").href = "javascript: void(0)";
                            } else {
                                document.getElementById("instrprev").href = "javascript: prevstep()";
                                document.getElementById("instrnext").href = "javascript: nextstep()";
                            };
                        };

                        function nextstep() {
                            var curstep = document.getElementById("instrstepheader").innerHTML;
                            var newstep = parseInt(curstep) + 1;
                            showinstruction(newstep);
                        };

                        function prevstep() {
                            var curstep = document.getElementById("instrstepheader").innerHTML;
                            var newstep = parseInt(curstep) - 1;
                            showinstruction(newstep);
                        };
                        </script>

                        <h1 id="instrstepheader" style="display:none;">1</h1>

                        <div id="instrsteps">
                        
                            <div id="instr1">
                                <h2>Welcome</h2>
                                <p>
                                Do you need historical boundaries for a particular project?<br>
                                Perhaps you are a historian or expert on a country or region
                                and want to quality check what others have already contributed?<br>
                                Or maybe you just love working with geographic and historical data,
                                and want to help out? 
                                </p>
                                <p>
                                Contributing to Pshapes is both easy and fast: just register and
                                contribute as little or as much as possible. You can add changes, quality check,
                                vouch or edit the work of others, raise issues, or discuss difficult cases. 
                                Click "Next" to read more about how to get started. 
                            </div>

                            <div id="instr2">
                                <h2>Sources of Information</h2>
                                <p>
                                There are several resources available detailing the administrative history of the country.
                                Start in the present time and work yourself backwards.
                                Each time you encounter a new date, register the date to the timeline.
                                </p>
                                <p>
                                If the exact date is not known, then just set the date to the earliest
                                possible date (e.g. 1st of the month, or 1st of january of the year).
                                </p>
                                <p>
                                In cases where there is no documented history, the only way is to compare
                                historical maps. In these cases the event of the date should be set to
                                the newest map. 
                                </p>
                                <h4>Recommended Sources:</h4>
                                <p style="font-size:medium; font-style:italic">
                                <ul>
                                    <li>
                                    <a target="_blank" href="http://www.statoids.com">Statoids website</a>
                                    </li>
                                    
                                    <li>
                                    <a target="_blank" href="https://en.wikipedia.org/wiki/Table_of_administrative_divisions_by_country">Wikipedia entries for administrative units</a>
                                    </li>

                                    <li>
                                    <a target="_blank" href="http://www.zum.de/whkmla/">World History at KMLA</a>
                                    </li>

                                    <li>
                                    <a target="_blank" href="http://www.populstat.info/">Populstat website</a>
                                    </li>
                                </ul>
                                </p>
                            </div>

                            <div id="instr3">
                                <h2>Administrative Levels</h2>
                                <p>
                                For each date, look for changes to the the first-level administrative areas,
                                the highest level in a country.
                                </p>
                                <p>
                                Some countries have a special administrative level between the national and
                                1st level, often referred to as "regions". These tend to be so big that sometimes there are only two or three of them.
                                In Pshapes we prefer to ignore these regions and instead focus on the level below. When in doubt follow
                                a rule that they should be small enough to provide good variation within the country and big enough that it
                                is feasible to get complete information on all of its changes.
                                </p>
                                <p>
                                If unsure about the correct level, leave a comment.
                                </p>
                            </div>

                            <div id="instr4">
                                <h2>Adding Events</h2>
                                <p>
                                On any given date, a province may experience one or more of the four basic event types:
                                new information, mergers, transfers, and splits. An event may involve multiple individual
                                changes, such as a province splitting into multiple new provinces. 
                                </p>
                                <p>
                                To identify the province involved in an event, note that
                                provinces are linked together via their name or any of their
                                identifier codes, so try to keep these consistent with existing entries.
                                </p>
                                <p>
                                For events where all provinces in a country experienced the same change, e.g.
                                a country merged entirely into another country,
                                you may set the name to * (star) to avoid having to register each province
                                individually. 
                                </p>
                            </div>

                            <div id="instr5">
                                <h2>Georeferencing Maps</h2>
                                <p>
                                For the vast majority of province changes we do not
                                need to consult historical maps or use valuable time on geocoding.
                                </p>
                                <p>
                                For some types of changes however there is simply no way around it. In these situations, namely mergers and
                                partial transfers of territory, Pshapes will ask you to draw the spatial extent of a change. To do this you will
                                need to find a historical map and georeference it at the <a target="_blank" href="http://mapwarper.net/">MapWarper website</a>.
                                </p>

                                <p>
                                <h4>Recommended Map Sources:</h4>
                                <ul>
                                    <li><a target="_blank" href="http://mapwarper.net/">MapWarper</a></li>
                                    <li><a target="_blank" href="http://www.oldmapsonline.org/">OldMapsOnline</a></li>
                                    <li><a target="_blank" href="http://www.vidiani.com/tag/administrative-maps/">Vidiani</a></li>
                                    <li><a target="_blank" href="http://www.mapsopensource.com">MapsOpenSource.com</a></li>
                                    <li><a target="_blank" href="http://www.ezilon.com">Ezilon.com</a></li>
                                    <li><a target="_blank" href="https://www.loc.gov/maps/?q=administrative%20divisions">The Library of Congress Map Collection</a></li>
                                    <li><a target="_blank" href="https://www.lib.utexas.edu/maps/historical/index.html">The Perry-Castaneda Library Map Collection</a></li>
                                    <li><a target="_blank" href="http://alabamamaps.ua.edu/historicalmaps/">Alabama Maps Historical Maps</a></li>
                                    <li><a target="_blank" href="http://www.zum.de/whkmla/region/indexa.html">World History at KMLA</a></li>
                                    <li><a target="_blank" href="http://www.antiquemapsandprints.com/prints-and-maps-by-country-12-c.asp">Antique Maps and Prints</a></li>
                                    <li><a target="_blank" href="http://catalogue.defap-bibliotheque.fr/index.php?lvl=index">La bibliotheque du Defap</a></li>
                                    <li><a target="_blank" href="https://books.google.no/books?id=n-xZp-QMKCcC&amp;lpg=PA25&amp;ots=qM9PapNLCF&amp;dq=world%20mapping%20today%20parry&amp;hl=no&amp;pg=PA320#v=onepage&amp;q=world%20mapping%20today%20parry&amp;f=false">"World Mapping Today", by Bob Parry and Chris Perkins</a></li>
                                </ul>
                                </p>
                            </div>

                            <div id="instr6">
                                <h2>What to do Include or Exclude</h2>
                                <p>
                                In some cases, transfers of territory may be listed with the names of lower-level areas, and these should just be
                                listed as partial territorial transfers and drawn roughly by hand.
                                </p>
                                <p>
                                However, if the change seems very small,
                                or if there are too many of these types of minor changes, it is okay to ignore most of them and only focus on
                                the big changes.
                                </p>
                            </div>

                            <div id="instr7">
                                <h2>Changes Between Countries</h2>
                                <p>
                                Sometimes you will come across cases where territory might be
                                transferred to or change ownership from one country to another.
                                Especially as you go further back in time you may encounter historical countries that don't exist anymore. 
                                </p>
                                <p>
                                The way to code changes between countries is to
                                register the event as usual, except changing the from-country field.
                                </p>
                                <p>
                                For instance, for each of the ex-Soviet
                                countries all of their provinces must be registered as changing info from the Soviet Union. The new country name
                                as you have written it will appear in the list of countries, so you can keep tracking it further back in time.
                                </p>
                            </div>

                            <div id="instr8">
                                <h2>How To Define a Country</h2>
                                <p>
                                It might not always be clear what constitutes a country. At all times follow what seems to have been the most
                                internationally recognized country-units and names. 
                                </p>
                                <p>
                                For territories under foreign colonial rule, these should be
                                coded as separate from the ruling power. For countries simply achieving independence or countries with only minor
                                changes in their official name, avoid changing the country name.
                                </p>
                            </div>

                            <div id="instr9">
                                <h2>Finishing Up</h2>
                                <p>
                                If you are finished coding a country or believe it's not possible to code further
                                back in time, then indicate this by adding the special "Begin" event.
                                </p>
                                <p>
                                Set this for all provinces (name = *) with the date
                                as the date beyond which we lack information about the administrative units.
                                </p>
                                <p>
                                Begin events are important for reverse geocoding and visualizing provinces,
                                especially for provinces that don't change much. 
                                <p>
                                Setting a Begin event does not not have to be final or definitive. It will always be possible to code a little further back in time, or others may sit on information
                                that you don't have. When the situation changes, you may simply edit your own Begin event, or others
                                may add their own Begin events. 
                                </p>
                            </div>

                        </div>

                        <script>
                        showinstruction(1)
                        </script>
                        
                        </div>
                """


def allcountries(request):
    bannertitle = "Contributions at a Glance:"

    from django.db.models import Count
    changes = ProvChange.objects.all().count()
    pending = ProvChange.objects.filter(status="Pending").count()
    countrycount = ProvChange.objects.filter(status="Pending").values("fromcountry").distinct().count()
    comments = Comment.objects.filter(status="Active").count()
    vouches = Vouch.objects.filter(status="Active").count()
    users = User.objects.all().count()

    #<img style="width:70%" src="https://content.linkedin.com/content/dam/blog/en-us/corporate/blog/2011/11/summary.png">
    #bars = [dict(value=ch) for ch in ProvChange.objects.filter(status="Pending")]
    bars = [dict(value=v, label=v) for v in range(0,100+1,10)] # just for testing
    # TODO: group by year and month, sort by 10 most recent
    curdate = datetime.datetime.now()
##    aggs = ProvChange.objects.\
##                            extra(select={'month': "EXTRACT(month FROM date)"}).\
##                            values('month').\
##                            annotate(count_items=Count('date'))
##    bars = [dict(value=a['count_items'], label=a['month']) for a in aggs]

##    bars = []
##    graphchanges = ProvChange.objects.all()
##    for w in range(10):
##        d2 = curdate - datetime.timedelta(7*w)
##        d1 = curdate - datetime.timedelta(7*(w+1))
##        c = graphchanges.filter(added__gt=d1, added__lte=d2).count()
##        bars.append(dict(value=c, label=""))
##    bars[2]['label'] = d1.strftime("%Y-%m-%d")
##    bars[-1]['label'] = curdate.strftime("%Y-%m-%d")
    contribcharttemplate = """
                        <style>
                        .chart rect {
                          fill: rgb(0,162,232);
                        }

                        .chart text {
                          fill: white;
                          font: 10px sans-serif;
                          text-anchor: end;
                        }
                        </style>

                        <svg class="chart" width="420" height="120">
                        <g transform="translate(0,110) scale(1,-1)">
                            
                            {% for bar in bars %}
                                    <rect x="{% widthratio forloop.counter0 1 10 %}%" y="0%" width="10%" height="{{ bar.value }}%"></rect>
                                    <text transform="scale(1,-1)" x="{% widthratio forloop.counter0 1 10 %}%" y="5%" dy=".35em">{{ bar.label }}</text>
                            {% endfor %}
                            
                        </g>
                        </svg>
                    """
    
    contribchart = Template(contribcharttemplate).render(Context({"request":request, 'bars':bars}))
    bannerleft = """
                <div>
                        <div style="text-align:center">
                            {contribchart}
                        </div>
		    
                        <b>
                        <table>
                        <tr style="vertical-align:text-top">
                            <td>
                            <h1>{countrycount}</h1>
                            Countries coded
                            </td>
                            
                            <td>
                            <h1>{changes}</h1>
                            Changes registered
                            </td>

                            <td>
                            <h1>{modifs}</h1>
                            Edits made
                            </td>

                            <td>
                            <h1>{vouches}</h1>
                            Vouches
                            </td>
                            
                            <td>
                            <h1>{comments}</h1>
                            Comments
                            </td>
                        </tr>
                        </table>
                        </b>
                </div>
                        """.format(users=users,
                                   changes=pending,
                                   modifs=changes-pending,
                                   comments=comments,
                                   vouches=vouches,
                                   countrycount=countrycount,
                                   contribchart=contribchart,
                                   )

    #QUOTE
    #Anyone who has an interest in coding some changes for one or more countries,
    #should have the ability to do so themselves, regardless of skills or background. 

    bannerright = GUIDE
    
    grids = []

    content = """
                    <h1>1</h1>
                    <div style="text-align:left">
                        Choose a country from the list below and begin registering historical changes.
                        After a vetting process the change will be included in the
                        next version of the data available from the website.

                        You can also browse,
                        quality check, suggest edits, and add comments to existing province changes
                        already submitted by other users.

                        <style>
                            #blackbackground a { color:white }
                            #blackbackground a:visited { color:grey }
                        </style>                        
                    </div>
            """

##    grids.append(dict(title="Instructions:",
##                      content=content,
##                      #style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                      width="99%",
##                      ))

    from django.db.models import Count,Max,Min

    # already coded
    fields = ["country","entries","mindate","maxdate"]
    lists = []
    rowdicts = dict() #dict([(countryid,dict(country=countryid,entries=0,mindate="-",maxdate="-")) for countryid,countryname in countries])
    for rowdict in ProvChange.objects.values("fromcountry").exclude(status="NonActive").annotate(entries=Count('pk'),
                                                                                                 mindate=Min("date"),
                                                                                                 maxdate=Max("date")):
        rowdict["country"] = rowdict.pop("fromcountry")
        rowdicts[rowdict["country"]] = rowdict
    for rowdict in ProvChange.objects.values("tocountry").exclude(status="NonActive").annotate(entries=Count('pk'),
                                                                                                 mindate=Min("date"),
                                                                                                 maxdate=Max("date")):
        rowdict["country"] = rowdict.pop("tocountry")
        if rowdict["country"] in rowdicts:
            cur = rowdicts[rowdict["country"]]
            cur["entries"] += rowdict["entries"]
            cur["mindate"] = min(cur["mindate"], rowdict["mindate"]) if cur["mindate"] != "-" else rowdict["mindate"]
            cur["maxdate"] = min(cur["maxdate"], rowdict["maxdate"]) if cur["maxdate"] != "-" else rowdict["maxdate"]
        else:
            rowdicts[rowdict["country"]] = rowdict

    for country in sorted(rowdicts.keys()):
        rowdict = rowdicts[country]
        row = [rowdict[f] for f in fields]
        url = "/contribute/view/%s" % urlquote(rowdict["country"])
        lists.append((url,row))
    
    countriestable = lists2table(request, lists=lists,
                                  fields=["Country","Entries","First Change","Last Change"])
    content = countriestable
    grids.append(dict(title="Continue coding:",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))

    # remaining
    lists = []
    rowdicts = dict([(countryid,dict(country=countryid,entries=0,mindate="-",maxdate="-")) for countryid,countryname in countries
                     if countryid not in rowdicts.keys()])

    for country in sorted(rowdicts.keys()):
        rowdict = rowdicts[country]
        row = [rowdict[f] for f in fields]
        url = "/contribute/view/%s" % urlquote(rowdict["country"])
        lists.append((url,row))
    
    countriestable = lists2table(request, lists=lists,
                                  fields=["Country","Entries","First Change","Last Change"])
    content = countriestable
    grids.append(dict(title="Add a new country:",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )


##def contribute_country(request, country):
##    status = request.GET.get("status", "Accepted")
##    bannertitle = "%s:"%country
##    bannerleft = """
##                    <div style="text-align:left">
##                        [INSERT MAP HERE]
##		    </div>
##    """
##    bannerright = """
##			Maybe some country stats...
##    """
##
##    changes = ProvChange.objects.filter(country=country,status=status).order_by("-added") # the dash reverses the order
##    changestable = model2table(request, title="", objects=changes,
##                              fields=["date","type","fromname","toname","country","user","added","status"])
##
##    tabstyle = """
##            <style>
##            .curtab {
##                display:table-cell;
##                background-color:orange;
##                color:white;
##                border-radius:10px;
##                padding:10px; 
##                }
##            .tab {
##                display:table-cell;
##                background-color:null;
##                color:black;
##                border-radius:10px;
##                padding:10px;
##                }
##            </style>
##            """
##    
##    tabs = """
##            <div class="{Accepted}"><h4><a href="/contribute/countries/{country}?status=Accepted" style="color:inherit">Accepted</a></h4></div>
##            <div class="{Pending}"><h4><a href="/contribute/countries/{country}?status=Pending" style="color:inherit">Pending</a></h4></div>
##
##            <br>
##            <br>
##            
##            """.format(Accepted="curtab" if status=="Accepted" else "tab",
##                        Pending="curtab" if status=="Pending" else "tab",
##                       country=country)
##    content = tabstyle + tabs + changestable
##    
##    grids = []
##    grids.append(dict(title="Browse province changes:",
##                      content=content,
##                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                      width="99%",
##                      ))
##    
##    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
##                                                           "bannerleft":bannerleft, "bannerright":bannerright}
##                  )


##def viewcountry(request, country):
##
##    if "date" in request.GET:
##        # date given, show all events on that date
##        date = request.GET["date"]
##        bannertitle = "{country}, {date}:".format(country=country.encode("utf8"),
##                                                date=datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%b %d, %Y'))
##        bannerleft = """
##                        <div style="text-align:left">
##                            [INSERT MAP HERE]
##                        </div>
##        """
##        bannerright = """
##                        Insert something...
##        """
##        
##        changes = ProvChange.objects.filter(country=country, date=date).order_by("-added") # the dash reverses the order
##        import itertools
##        
##        def typeprov(obj):
##            typ = obj.type
##            if "Transfer" in typ:
##                prov = obj.toname
##                return "Expansion",prov
##            elif typ == "Breakaway":
##                prov = obj.fromname
##                return "Split",prov
##            elif typ == "NewInfo":
##                prov = obj.toname
##                return typ,prov
##        def events():
##            dategroup = list(changes)
##            #splits
##            subkey = lambda o: o.fromname
##            for splitfrom,splitgroup in itertools.groupby(sorted(dategroup,key=subkey), key=subkey):
##                splitgroup = list(splitgroup)
##                splits = [ch for ch in splitgroup if ch.type == "Breakaway"]
##                if splits:
##                    yield (date,("Split",splitfrom)), splits
##            # mergers
##            subkey = lambda o: o.toname
##            for mergeto,mergegroup in itertools.groupby(sorted(dategroup,key=subkey), key=subkey):
##                mergegroup = list(mergegroup)
##                mergers = [ch for ch in mergegroup if "Transfer" in ch.type]
##                if mergers:
##                    yield (date,("Expansion",mergeto)), mergers
##            # newinfos
##            subkey = lambda o: o.fromname
##            for fromname,newgroup in itertools.groupby(sorted(dategroup,key=subkey), key=subkey):
##                newinfos = [ch for ch in newgroup if "NewInfo" == ch.type]
##                if newinfos:
##                    yield (date,("NewInfo",fromname)), newinfos
##
##        events = events()
##        
##    ##    sortkey = lambda o:(o.date,typeprov(o))
##    ##    events = itertools.groupby(sorted(changes,key=sortkey), key=sortkey)
##        
##        def getlinkrow(date,prov,typ,items):
##            items = list(items)
##            firstitem = items[0]
##            if typ == "NewInfo":
##                fields = ["country","source","date","fromname","fromtype","fromhasc","fromiso","fromfips","fromcapital"]
##                params = urlencode(dict([(field,getattr(firstitem,field)) for field in fields]))
##                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(country), prov=urlquote(prov)) + params + '&type="NewInfo"'
##            elif typ == "Split":
##                fields = ["country","source","date","fromname","fromtype","fromhasc","fromiso","fromfips","fromcapital"]
##                params = urlencode(dict([(field,getattr(firstitem,field)) for field in fields]))
##                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(country), prov=urlquote(prov)) + params + '&type="Split"'
##            elif typ == "Expansion":
##                fields = ["country","source","date","toname","totype","tohasc","toiso","tofips","tocapital"]
##                params = urlencode(dict([(field,getattr(firstitem,field)) for field in fields]))
##                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(country), prov=urlquote(prov)) + params + '&type="Expansion"'
##            return link,(prov,typ)
##        events = [getlinkrow(date,prov,typ,items) for (date,(typ,prov)),items in events]
##        eventstable = lists2table(request, events, ["Province", "EventType"])
##
##        content = eventstable
##        
##        grids = []
##        grids.append(dict(title='Events: <a href="/contribute/add/{country}?date={date}">Add new</a>'.format(country=urlquote(country), date=urlquote(date)),
##                          content=content,
##                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                          width="99%",
##                          ))
##        
##        return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
##                                                               "bannerleft":bannerleft, "bannerright":bannerright}
##                      )
##
##    else:
##        bannertitle = "Timeline for %s" % country.encode("utf8")
##        bannerleft = """
##                        <div style="text-align:left">
##                            [INSERT MAP HERE]
##                        </div>
##        """
##        bannerright = """
##                        <div style="background-color:rgb(248,234,150); outline: black solid thick;">
##                        <p style="font-size:large; font-weight:bold">Note:</p>
##                        <p style="font-size:medium; font-style:italic">
##                        There are several types of sources you can use:
##                        <ul>
##                            <li>
##                            <a target="_blank" href="http://www.statoids.com">The Statoids website</a> traces historical province changes
##                            in great detail, and should be the first place to look.
##                            </li>
##
##                            <li>
##                            The <a target="_blank" href="https://en.wikipedia.org/wiki/Table_of_administrative_divisions_by_country">Wikipedia entries for administrative units</a>
##                            can sometimes also be a useful reference.
##                            </li>
##
##                            <li>
##                            You can also use offline sources such as a book or an article.
##                            </li>
##                        </ul>
##                        </p>
##                        </div>
##        """
##
##
##        dates = [d["date"].isoformat() for d in ProvChange.objects.filter(country=country).order_by("date").values('date').distinct()]
##        print dates
##
##        def getlinkrow(date):
##            link = "/contribute/view/{country}/?".format(country=urlquote(country)) + "date=" + date
##            return link, (date,)
##
##        daterows = [getlinkrow(date) for date in dates]
##        datestable = lists2table(request, daterows, ["Date"])
##
##        content = datestable
##        
##        grids = []
##        grids.append(dict(title='Dates: <a href="/contribute/add/%s">Add new</a>' % urlquote(country),
##                          content=content,
##                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                          width="99%",
##                          ))
##        
##        return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
##                                                               "bannerleft":bannerleft, "bannerright":bannerright}
##                      )

def viewcountry(request, country):

    def getdateeventstable(date):
        changes = (ProvChange.objects.filter(fromcountry=country, date=date).exclude(status="NonActive") | ProvChange.objects.filter(tocountry=country, date=date).exclude(status="NonActive")).order_by("-added") # the dash reverses the order
        import itertools
        
        def typeprov(obj):
            typ = obj.type
            if typ == "FullTransfer":
                prov = obj.toname
                return prov,"Merge",obj.fromcountry,obj.tocountry
            elif typ == "PartTransfer":
                prov = obj.toname
                return prov,"Transfer",obj.fromcountry,obj.tocountry
            elif typ == "Breakaway":
                prov = obj.fromname
                return prov,"Split",obj.fromcountry,obj.tocountry
            elif typ == "NewInfo":
                prov = obj.fromname
                return prov,typ,obj.fromcountry,obj.tocountry
            elif typ == "Begin":
                prov = obj.toname
                return prov,typ,obj.fromcountry,obj.tocountry
        def events():
            dategroup = list(changes)
            subkey = typeprov
            for typprov,subevents in itertools.groupby(sorted(dategroup,key=subkey), key=subkey):
                yield (date,typprov),subevents
                
##            #splits
##            subkey = lambda o: o.fromname
##            for splitfrom,splitgroup in itertools.groupby(sorted(dategroup,key=subkey), key=subkey):
##                splitgroup = list(splitgroup)
##                splits = [ch for ch in splitgroup if ch.type == "Breakaway"]
##                if splits:
##                    yield (date,("Split",splitfrom)), splits
##            # mergers
##            subkey = lambda o: o.toname
##            for mergeto,mergegroup in itertools.groupby(sorted(dategroup,key=subkey), key=subkey):
##                mergegroup = list(mergegroup)
##                mergers = [ch for ch in mergegroup if ch.type == "FullTransfer"]
##                if mergers:
##                    yield (date,("Merge",mergeto)), mergers
##            # transfers
##            subkey = lambda o: o.fromname
##            for transfrom,transgroup in itertools.groupby(sorted(dategroup,key=subkey), key=subkey):
##                transgroup = list(transgroup)
##                transfers = [ch for ch in transgroup if ch.type == "PartTransfer"]
##                if transfers:
##                    yield (date,("Transfer",transfrom)), transfers
##            # newinfos
##            subkey = lambda o: o.fromname
##            for fromname,newgroup in itertools.groupby(sorted(dategroup,key=subkey), key=subkey):
##                newinfos = [ch for ch in newgroup if "NewInfo" == ch.type]
##                if newinfos:
##                    yield (date,("NewInfo",fromname)), newinfos

        events = events()
        
        def getlinkrow(date,prov,typ,fromcountry,tocountry,items):
            items = list(items)
            firstitem = items[0]
            # link should point to country that was different, if any
            if fromcountry and fromcountry == country:
                linkcountry = fromcountry
            elif tocountry and tocountry == country:
                linkcountry = tocountry
            else:
                linkcountry = country
                
            if typ == "NewInfo":
                fields = ["fromcountry","tocountry","source","sources","mapsources","date","fromname","fromalterns","fromtype","fromhasc","fromiso","fromfips","fromcapital","fromcapitalname"]
                params = dict([(field,getattr(firstitem,field)) for field in fields])
                params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
                params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
                params = urlencode(params)
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(linkcountry), prov=urlquote(prov)) + params + '&type="NewInfo"'
                prov = markcountrychange(country, firstitem.fromname, [firstitem.fromcountry,firstitem.tocountry])
            elif typ == "Split":
                fields = ["fromcountry","tocountry","source","sources","mapsources","date","fromname","fromalterns","fromtype","fromhasc","fromiso","fromfips","fromcapital","fromcapitalname"]
                params = dict([(field,getattr(firstitem,field)) for field in fields])
                params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
                params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
                params = urlencode(params)
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(linkcountry), prov=urlquote(prov)) + params + '&type="Split"'
                prov = markcountrychange(country, firstitem.fromname, [firstitem.fromcountry,firstitem.tocountry])
            elif typ == "Merge":
                fields = ["fromcountry","tocountry","source","sources","mapsources","date","toname","toalterns","totype","tohasc","toiso","tofips","tocapital","tocapitalname"]
                params = dict([(field,getattr(firstitem,field)) for field in fields])
                params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
                params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
                params = urlencode(params)
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(linkcountry), prov=urlquote(prov)) + params + '&type="Merge"'
                prov = markcountrychange(country, firstitem.toname, [firstitem.fromcountry,firstitem.tocountry])
            elif typ == "Transfer":
                fields = ["fromcountry","tocountry","source","sources","mapsources","date","toname","toalterns","totype","tohasc","toiso","tofips","tocapital","tocapitalname"]
                params = dict([(field,getattr(firstitem,field)) for field in fields])
                params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
                params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
                params = urlencode(params)
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(linkcountry), prov=urlquote(prov)) + params + '&type="Transfer"'
                prov = markcountrychange(country, firstitem.toname, [firstitem.fromcountry,firstitem.tocountry])
            elif typ == "Begin":
                fields = ["fromcountry","tocountry","source","sources","mapsources","date","toname","toalterns","totype","tohasc","toiso","tofips","tocapital","tocapitalname"]
                params = dict([(field,getattr(firstitem,field)) for field in fields])
                params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
                params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
                params = urlencode(params)
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(linkcountry), prov=urlquote(prov)) + params + '&type="Begin"'
                prov = markcountrychange(country, firstitem.toname, [firstitem.fromcountry,firstitem.tocountry])

            changeids = [c.changeid for c in items]
            vouches=len(list(Vouch.objects.filter(changeid__in=changeids, status='Active')))
            if vouches:
                vouchitem = '''
                            <div style="display:inline; border-radius:10px; ">
                            <a style="color:black; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
                            <img src="https://d30y9cdsu7xlg0.cloudfront.net/png/110875-200.png" height=30px/>
                            </div>
                            '''.format(vouches=vouches)
            else:
                vouchitem = '<a style="color:black; font-family:inherit; font-size:inherit; font-weight:bold;">0</a>'
            return link,(prov,typ,vouchitem)
        events = [getlinkrow(date,prov,typ,fromcountry,tocountry,items) for (date,(prov,typ,fromcountry,tocountry)),items in events]
        eventstable = lists2table(request, events, ["Province", "EventType", "Vouches"])

        content = eventstable
        
        return content

    if "date" in request.GET:
        # date given, show all events on that date
        date = request.GET["date"]
        top = """
                        <a href="/contribute/view/{country}" style="float:left; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                        Back to {countrytext}
                        </a>
                        """.format(country=urlquote(country), countrytext=country.encode("utf8"))
        left = """
                        <h3 style="clear:both">{country} events for {date}:</h3>
                        <div style="">
                            <img style="width:200px;" src="http://www.freeiconspng.com/uploads/clock-event-history-schedule-time-icon--19.png">
                        </div>
        """.format(country=country.encode("utf8"), date=datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%b %d, %Y'))
        right = """
                        Insert something...
        """

        custombanner = """

                        {top}
                        
                        <table width="99%" style="clear:both; padding:0px; margin:0px">
                        <tr>
                        
                        <td style="width:48%; padding:1%; text-align:center; padding:0px; margin:0px; vertical-align:top">
                        {left}
                        </td>
                        
                        <td style="width:48%; padding:1%; padding:0px; margin:0px; vertical-align:top; text-align:center">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """.format(top=top, left=left, right=right)
    
        grids = []
        content = getdateeventstable(date)
        grids.append(dict(title='Events: <a href="/contribute/add/{country}?date={date}">Add new</a>'.format(country=urlquote(country), date=urlquote(date)),
                          content=content,
                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                          width="99%",
                          ))
        
        return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"custombanner":custombanner}
                      )

    else:
        bannertitle = "" #"Timeline for %s" % country.encode("utf8")
        top = """
                        <a href="/contribute/countries/" style="float:left; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Back to World
			</a>
			"""

        # GRIDS
        grids = []

        # dates            
        dates = [d["date"].isoformat() for d in (ProvChange.objects.filter(fromcountry=country).exclude(status="NonActive") | ProvChange.objects.filter(tocountry=country).exclude(status="NonActive")).order_by("date").values('date').distinct()]
        print dates

    ##    def getlinkrow(date):
    ##        link = "/contribute/view/{country}/?".format(country=urlquote(country)) + "date=" + date
    ##        return link, (date,)

    ##    daterows = [getlinkrow(date) for date in dates]
    ##    datestable = lists2table(request, daterows, ["Date"])

    ##    content = datestable

        content = '''<hr>
                    <h3 id="timeline">
                        <img src="https://image.flaticon.com/icons/svg/55/55191.svg" height="40px">
                        Timeline:
                        <a style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:underline; margin:10px;" href="/contribute/add/{country}">New Date</a>
                    </h3>'''.format(country=urlquote(country))
        
        for date in dates:
            table = getdateeventstable(date)
            html = """
                    <div style="margin-left:2%">
                    <h4>
                        {date}
                    </h4>
                    {table}
                    <br><div width="100%" style="text-align:center"><a href="/contribute/add/{country}?date={date}" style="text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                    </div>
                    """.format(date=date, table=table.encode('utf8'), country=urlquote(country))
            content += html
            
        grids.append(dict(title="",
                          content=content,
                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                          width="95%",
                          ))

        # sources
        color = "rgb(60,60,60)"

        sources = list(get_country_sources(country))

##        content = '''<hr>
##                     <h3>
##                         Sources:
##                         <a style="background-color:{color}; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:underline; margin:10px;" href="/addsource/">New Source</a>
##                    </h3>
##                    '''.format(color=color)
##        
##        for source in sources:
##            griditem = """
##                    <a href="/viewsource/{pk}/" style="text-decoration:none; color:inherit;">
##                        <div class="griditem" style="float:left; width:200px; margin:10px">
##                            <div class="gridheader" style="background-color:{color}; padding-top:10px">
##                                <img src="http://www.pvhc.net/img28/hgicvxtrvbwmfpuozczo.png" height="40px">
##                                <h4 style="display:inline-block">{title}</h4>
##                            </div>
##                            
##                            <div class="gridcontent">
##                                <p>{citation}</p>
##                            </div>
##                        </div>
##                    </a>
##                        """.format(color=color, title=source.title, citation=source.citation, pk=source.pk)
##            html = """
##                    <div style="margin-left:2%">
##                    {griditem}
##                    </div>
##                    """.format(griditem=griditem)
##            content += html

        fields = ['title', 'citation']
        lists = []
        for source in sources:
            link = '/viewsource/{pk}/'.format(pk=source.pk)
            row = [source.title, source.citation]
            lists.append((link,row))

        table = lists2table(request, lists, fields, 'sourcetable', color)

        content = '''<br><br>
                    <hr>
                     <h3 id="sources">
                         <img src="http://www.pvhc.net/img28/hgicvxtrvbwmfpuozczo.png" height="40px">
                         Sources:
                    </h3>
                    <div style="margin-left:2%">
                        {table}
                        <br><div width="100%" style="text-align:center"><a href="/addsource/?country={country}" style="text-align:center; background-color:{color}; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                    </div>
                    '''.format(table=table.encode('utf8'), color=color, country=urlquote(country))
            
        grids.append(dict(title="",
                          content=content,
                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                          width="95%",
                          ))

        # maps
        color = 'rgb(58,177,73)'

        maps = list(get_country_maps(country))
        
##        for mapp in maps:
##            #http://sampleserver1.arcgisonline.com/ArcGIS/services/Specialty/ESRI_StatesCitiesRivers_USA/MapServer/WMSServer?version=1.3.0&request=GetMap&CRS=CRS:84&bbox=-178.217598,18.924782,-66.969271,71.406235&width=760&height=360&layers=0&styles=default&format=image/png
##            #https://mapwarper.net/maps/wms/19956
##            griditem = """
##                    <a href="/viewmap/{pk}/" style="text-decoration:none; color:inherit;">
##                        <div class="griditem" style="float:left; width:200px; margin:10px">
##                            <div class="gridheader" style="background-color:{color}; padding-top:10px">
##                                <img src="http://www.pvhc.net/img28/hgicvxtrvbwmfpuozczo.png" height="40px">
##                                <h4 style="display:inline-block">{year}</h4>
##                            </div>
##                            
##                            <div class="gridcontent">
##                                <img width="100%" src="http://sampleserver1.arcgisonline.com/ArcGIS/services/Specialty/ESRI_StatesCitiesRivers_USA/MapServer/WMSServer?version=1.3.0&request=GetMap&CRS=CRS:84&bbox=-178.217598,18.924782,-66.969271,71.406235&width=760&height=360&layers=0&styles=default&format=image/png">
##                                <p>{title}</p>
##                            </div>
##                        </div>
##                    </a>
##                        """.format(color=color, year=mapp.year, title=mapp.title, note=mapp.note, wms=mapp.wms, pk=mapp.pk)
##            html = """
##                    <div style="margin-left:2%">
##                    {griditem}
##                    </div>
##                    """.format(country=urlquote(country), griditem=griditem)
##            content += html

        fields = ['', 'year', 'title', 'url']
        lists = []
        for mapp in maps:
            wms = mapp.wms #"https://mapwarper.net/maps/wms/26754" #"https://mapwarper.net/maps/wms/19956"
            if wms:
                wmslink = WMS_Helper(wms).image_url(height=50)
                imglink = '<a href="/viewmap/{pk}/"><img height="50px" src="{wmslink}"></a>'.format(pk=mapp.pk, wmslink=wmslink)
            else:
                wmslink = "http://icons.iconarchive.com/icons/icons8/android/512/Maps-Map-Marker-icon.png"
                imglink = '<a href="/viewmap/{pk}/"><img height="50px" src="{wmslink}" style="opacity:0.1"></a>'.format(pk=mapp.pk, wmslink=wmslink)
            row = [imglink, mapp.year, mapp.title, mapp.url]
            lists.append((None,row))

        table = lists2table(request, lists, fields, 'maptable', color)

        content = '''<br><br>
                    <hr>
                     <h3 id="maps">
                         <img src="http://icons.iconarchive.com/icons/icons8/android/512/Maps-Map-Marker-icon.png" height="40px">
                         Maps:
                    </h3>
                    <div style="margin-left:2%">
                        {table}
                        <br><div width="100%" style="text-align:center"><a href="/addmap/?country={country}" style="text-align:center; background-color:{color}; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>
                    </div>
                    '''.format(table=table.encode('utf8'), color=color, country=urlquote(country))
            
        grids.append(dict(title="",
                          content=content,
                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                          width="95%",
                          ))

        # comments
        allcomments = Comment.objects.filter(country=country, changeid=None, status="Active")
        content = '<br><br><hr><h3 id="comments"><img src="https://png.icons8.com/metro/540/comments.png" style="padding-right:5px" height="40px">Questions & Comments:</h3>'
        content += '<div style="margin-left:2%%"> %s </div>' % comments2html(request, allcomments, country, None, 'rgb(27,138,204)')
        grids.append(dict(title="",
                          content=content,
                          style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                          width="99%",
                          ))

##                        <div style="text-align:center; margin-left:30%">
##
##                            <div style="background-color:orange; width:50%; border-radius:5px; text-align:left; padding:5px; margin:5px">
##                                <a href="#timeline" style="text-decoration:none; color:inherit">
##                                <img src="https://image.flaticon.com/icons/svg/55/55191.svg" height="40px">
##                                <h3 style="display:inline">Timeline</h3>
##                                </a>
##                            </div>
##
##                            <div style="background-color:rgb(122,122,122); width:50%; border-radius:5px; text-align:left; padding:5px; margin:5px">
##                                <a href="#sources" style="text-decoration:none; color:inherit">
##                                <img src="http://www.pvhc.net/img28/hgicvxtrvbwmfpuozczo.png" height="40px">
##                                <h3 style="display:inline">Sources</h3>
##                                </a>
##                            </div>
##
##                            <div style="background-color:rgb(58,177,73); width:50%; border-radius:5px; text-align:left; padding:5px; margin:5px">
##                                <a href="#maps" style="text-decoration:none; color:inherit">
##                                <img src="http://icons.iconarchive.com/icons/icons8/android/512/Maps-Map-Marker-icon.png" height="40px">
##                                <h3 style="display:inline">Maps</h3>
##                                </a>
##                            </div>
##
##                            <div style="background-color:rgb(27,138,204); width:50%; border-radius:5px; text-align:left; padding:5px; margin:5px">
##                                <a href="#comments" style="text-decoration:none; color:inherit">
##                                <img src="https://png.icons8.com/metro/540/comments.png" style="padding-right:5px" height="40px">
##                                <h3 style="display:inline">Comments</h3>
##                                </a>
##                            </div>
##                            
##                        </div>

        mapdata = ProvShape.objects.filter(country=country)
        if mapdata:
            latest_date = mapdata.latest('end')
            countrymap = """
                <script src="http://openlayers.org/api/2.13/OpenLayers.js"></script>

                    <div style="width:90%%; height:40vh; margins:auto; border-radius:10px; background-color:rgb(0,162,232);" id="map">
                    </div>
                
                <script defer="defer">
                var map = new OpenLayers.Map('map', {allOverlays: true,
                                                    //resolutions: [0.5,0.6,0.7,0.8,0.9,1],
                                                    controls: [],
                                                    });
                </script>

                <script>
                // empty country layer
                var style = new OpenLayers.Style({fillColor:"rgb(200,200,200)", strokeWidth:0.2, strokeColor:'white'},
                                                );
                var countryLayer = new OpenLayers.Layer.Vector("Provinces", {styleMap:style});
                map.addLayers([countryLayer]);
                
                // empty province layer
                var style = new OpenLayers.Style({fillColor:"rgb(122,122,122)", strokeWidth:0.1, strokeColor:'white'},
                                                );
                var provLayer = new OpenLayers.Layer.Vector("Provinces", {styleMap:style});
                map.addLayers([provLayer]);

                rendercountries = function(data) {
                        var geojson_format = new OpenLayers.Format.GeoJSON();
                        var geoj_str = JSON.stringify(data);
                        countries = geojson_format.read(geoj_str, "FeatureCollection");
                        
                        feats = [];
                        for (feat of countries) {
                                feats.push(feat);
                        };
                        countryLayer.addFeatures(feats);
                };

                $.getJSON('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json', {}, rendercountries);

                renderprovs = function(data) {
                        var geojson_format = new OpenLayers.Format.GeoJSON();
                        var geoj_str = JSON.stringify(data);
                        allProvs = geojson_format.read(geoj_str, "FeatureCollection");
                        
                        dateFeats = [];
                        for (feat of allProvs) {
                                dateFeats.push(feat);
                        };
                        provLayer.addFeatures(dateFeats);
                        map.zoomToExtent(provLayer.getDataExtent());
                        map.updateSize();
                };

                var latest = '%s'.split('-');
                $.getJSON('/api', {simplify:0.05, year:latest[0], month:latest[1], day:latest[2], country:'%s'}, renderprovs);
                
                </script>
                """ % (latest_date.end, country.encode("utf8"))
            
            left = """	
                            <h3 style="clear:both">{countrytext}</h3>
                            
                            <div style="text-align:center; margin-left:5%">

                            {countrymap}

                            </div>

                            <br>
                            <a href="/explore/?country={countrytext}" style="text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">
                            Explore in Map View
                            </a>
                            
                            <br><br><br>
            """.format(countrytext=country.encode("utf8"), countrymap=countrymap)
            
        else:
            left = """	
                            <h3 style="clear:both">{countrytext}</h3>
                            
                            <div style="text-align:center; margin-left:5%">
                            <br>

                            <p>The historical boundaries for this country have not yet been reconstructed.
                            Just start adding events on the timeline below, and once they have been reviewed
                            and accepted by an administrator, you will see your changes visualized on a map here.</p>

                            </div>
            """.format(countrytext=country.encode("utf8"))


        right = """<br>
                        <div style="text-align:center; margin-left:5%">

                            <div style="background-color:orange; width:95%; border-radius:5px; text-align:left; padding:5px; margin:5px">
                                <a href="#timeline" style="text-decoration:none; color:inherit">
                                <img src="https://image.flaticon.com/icons/svg/55/55191.svg" height="40px">
                                <h3 style="display:inline">Timeline ({daterange})</h3>
                                </a>
                            </div>

                            <div style="background-color:rgb(122,122,122); width:95%; border-radius:5px; text-align:left; padding:5px; margin:5px">
                                <a href="#sources" style="text-decoration:none; color:inherit">
                                <img src="http://www.pvhc.net/img28/hgicvxtrvbwmfpuozczo.png" height="40px">
                                <h3 style="display:inline">Sources ({sources})</h3>
                                </a>
                            </div>

                            <div style="background-color:rgb(58,177,73); width:95%; border-radius:5px; text-align:left; padding:5px; margin:5px">
                                <a href="#maps" style="text-decoration:none; color:inherit">
                                <img src="http://icons.iconarchive.com/icons/icons8/android/512/Maps-Map-Marker-icon.png" height="40px">
                                <h3 style="display:inline">Maps ({maps})</h3>
                                </a>
                            </div>

                            <div style="background-color:rgb(27,138,204); width:95%; border-radius:5px; text-align:left; padding:5px; margin:5px">
                                <a href="#comments" style="text-decoration:none; color:inherit">
                                <img src="https://png.icons8.com/metro/540/comments.png" style="padding-right:5px" height="40px">
                                <h3 style="display:inline">Comments ({comments})</h3>
                                </a>
                            </div>
                            
                        </div>

                <br><br>
                
                """.format(countrytext=country.encode("utf8"),
                           daterange='%s - %s' % (dates[0].split('-')[0],dates[-1].split('-')[0]) if dates else '-',
                           sources=len(sources),
                           maps=len(maps),
                           comments=allcomments.count(),
                           )

##        bottom = """	
##                        <div style="margin-left:20%; margin-bottom:80px">
##
##                            <div style="float:left; background-color:orange; border-radius:5px; text-align:left; padding:5px; margin:5px">
##                                <a href="#timeline" style="text-decoration:none; color:inherit">
##                                <img src="https://image.flaticon.com/icons/svg/55/55191.svg" height="40px">
##                                <h3 style="display:inline">Timeline</h3>
##                                </a>
##                            </div>
##
##                            <div style="float:left; background-color:rgb(122,122,122); border-radius:5px; text-align:left; padding:5px; margin:5px">
##                                <a href="#sources" style="text-decoration:none; color:inherit">
##                                <img src="http://www.pvhc.net/img28/hgicvxtrvbwmfpuozczo.png" height="40px">
##                                <h3 style="display:inline">Sources</h3>
##                                </a>
##                            </div>
##
##                            <div style="float:left; background-color:rgb(58,177,73); border-radius:5px; text-align:left; padding:5px; margin:5px">
##                                <a href="#maps" style="text-decoration:none; color:inherit">
##                                <img src="http://icons.iconarchive.com/icons/icons8/android/512/Maps-Map-Marker-icon.png" height="40px">
##                                <h3 style="display:inline">Maps</h3>
##                                </a>
##                            </div>
##
##                            <div style="float:left; background-color:rgb(27,138,204); border-radius:5px; text-align:left; padding:5px; margin:5px">
##                                <a href="#comments" style="text-decoration:none; color:inherit">
##                                <img src="https://png.icons8.com/metro/540/comments.png" style="padding-right:5px" height="40px">
##                                <h3 style="display:inline">Comments</h3>
##                                </a>
##                            </div>
##                            
##                        </div>
##        """.format(countrytext=country.encode("utf8"), country=urlquote(country))

        custombanner = """

                        {top}
                        
                        <table width="99%" style="clear:both; padding:0px; margin:0px">
                        <tr>
                        
                        <td style="width:48%; padding:1%; text-align:center; padding:0px; margin:0px; vertical-align:top">
                        {left}
                        </td>
                        
                        <td style="width:48%; padding:1%; padding:0px; margin:0px; vertical-align:text-top;">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """.format(top=top, left=left, right=right)
        
        return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"custombanner":custombanner}
                      )


def editcountry(request):
    pass

def addcountry(request):
    pass


def viewprov(request, country, province):
    if all((k in request.GET for k in "date type".split())):
        # view event, ensure enough params
        return viewevent(request, country, province)

    else:
        raise Exception("You must set at least the date and type GET params to view an event")

def editprov(request):
    pass

def addprov(request, country, province=None):
    if len(request.GET) == 0:
        # add date
        return adddate(request, country)

    if len(request.GET) == 1 and "date" in request.GET:
        # add event, ensure enough params
        return addevent(request, country)

    else:
        # add individual change (preferably to existing event), ensure enough params are provided
        return addchange(request, country, province)

@login_required
def adddate(request, country):
    func = AddDateWizard.as_view(country=country)
    return func(request)

def markcountrychange(country, provtext, provcountries):
    if not isinstance(provcountries,list):
        provcountries = [provcountries]
    for provcountry in provcountries:
        if provcountry and provcountry != country:
            provtext += " (%s)" % provcountry
            break
    return provtext

def viewevent(request, country, province):
    # TODO: add "edit-event" button in main banner
    # and "add-change" button down by the table
    assert all((param in request.GET for param in "date type".split()))
    #country = request.GET["country"].strip('"').strip("'").strip()
    y,m,d = map(int,request.GET["date"].strip('"').strip("'").strip().split("-"))
    date = datetime.date(year=y,month=m,day=d)
    prov = province #request.GET["prov"].strip('"').strip("'").strip()
    typ = request.GET["type"].strip('"').strip("'").strip()

##    if typ == "Split":
##        bannertitle = "{provtext} province split into new provinces on {date}".format(provtext=prov.encode("utf8"), date=date.strftime('%b %d, %Y'))
##    elif typ == "Expansion":
##        bannertitle = "{provtext} province received territory from existing provinces on {date}".format(provtext=prov.encode("utf8"), date=date.strftime('%b %d, %Y'))
##    elif typ == "NewInfo":
##        bannertitle = "{provtext} province changed some of its information on {date}".format(provtext=prov.encode("utf8"), date=date.strftime('%b %d, %Y'))
##    else:
##        raise Exception()
    
    #bannertitle = '<a href="/contribute/view/{country}" style="color:inherit">{countrytext}</a>, {provtext}:'.format(country=urlquote(country),countrytext=country.encode("utf8"),provtext=prov.encode("utf8"))
    bannertitle = ""
    grids = []
    
    print "TYPE",repr(typ)
    if typ == "NewInfo":
        fields = ["toname","type","status"]
        #changes = ProvChange.objects.filter(country=country,date=date,type="NewInfo",fromname=prov)
        if 'tocountry' in request.GET:
            # existing event
            changes = ProvChange.objects.filter(fromcountry=request.GET['fromcountry'], tocountry=request.GET['tocountry'], date=date, type="NewInfo", fromname=prov, bestversion=True).exclude(status="NonActive")
        else:
            # new event, so tocountry doesnt exist yet
            changes = ProvChange.objects.filter(fromcountry=request.GET['fromcountry'], date=date, type="NewInfo", fromname=prov, bestversion=True).exclude(status="NonActive")
        change = next((c for c in changes.order_by("-added")), None)

        if change:
            oldinfo = '<li style="list-style:none">'+markcountrychange(country, change.fromname, change.fromcountry).encode("utf8")+"<br><br></li>"            
            if change.fromalterns != change.toalterns: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Altnerate names: '+change.fromalterns.encode("utf8")+"</li>"
            if change.fromiso != change.toiso: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; ISO: '+change.fromiso.encode("utf8")+"</li>"
            if change.fromfips != change.tofips: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; FIPS: '+change.fromfips.encode("utf8")+"</li>"
            if change.fromhasc != change.tohasc: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; HASC: '+change.fromhasc.encode("utf8")+"</li>"
            if change.fromcapitalname != change.tocapitalname: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital: '+change.fromcapitalname.encode("utf8")+"</li>"
            if change.fromcapital != change.tocapital: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital moved: '+change.fromcapital.encode("utf8")+"</li>"
            if change.fromtype != change.totype: oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Type: '+change.fromtype.encode("utf8")+"</li>"
            top = """
                            <a href="/contribute/view/{country}" style="float:left; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                            Back to {countrytext}
                            </a>
                            """.format(country=urlquote(country), countrytext=country.encode("utf8"))
            left = """
                            <div style="clear:both; text-align: left">
                            <h2 style="float:left">{oldinfo}</h2>
                            </div>
            """.format(oldinfo=oldinfo)

            mid = """
                    <h2><em>Changed info to:</em></h2>
                    """
        
            newinfo = '''<li style="font-size:smaller; list-style:none"> {provtext}<a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>

                        <div style="display:inline; border-radius:10px; ">
                        <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
                        <img src="https://d30y9cdsu7xlg0.cloudfront.net/png/110875-200.png" height=30px style="filter:invert(100%)"/>
                        </div>
				
                        <br><br></li>'''.format(pk=change.pk, provtext=markcountrychange(country, change.toname, change.tocountry).encode("utf8"), vouches=len(list(Vouch.objects.filter(changeid=change.changeid, status='Active'))))
            if change.fromalterns != change.toalterns: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Alternate names: '+change.toalterns.encode("utf8")+"</li>"
            if change.fromiso != change.toiso: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; ISO: '+change.toiso.encode("utf8")+"</li>"
            if change.fromfips != change.tofips: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; FIPS: '+change.tofips.encode("utf8")+"</li>"
            if change.fromhasc != change.tohasc: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; HASC: '+change.tohasc.encode("utf8")+"</li>"
            if change.fromcapitalname != change.tocapitalname: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital: '+change.tocapitalname.encode("utf8")+"</li>"
            if change.fromcapital != change.tocapital: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital moved: '+change.tocapital.encode("utf8")+"</li>"
            if change.fromtype != change.totype: newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Type: '+change.totype.encode("utf8")+"</li>"
            right = """
                            <style>
                                #blackbackground a {{ color:white }}
                                #blackbackground a:visited {{ color:grey }}
                            </style>
                            
                            <div id="blackbackground">
                            <h2>{newinfo}</h2>
                            </div>  
            """.format(newinfo=newinfo)
            custombanner = """

                            {top}

                            <style>
                            td {{vertical-align:top}}
                            </style>
                            
                            <table width="99%" style="clear:both">
                            <tr>
                            
                            <td style="width:31%; padding:1%">
                            {left}
                            </td>

                            <td style="width:31%; padding:1%">
                            {mid}
                            </td>
                            
                            <td style="width:31%; padding:1%">
                            {right}
                            </td>

                            </tr>
                            </table>
                            """.format(top=top, left=left, mid=mid, right=right)


##            pendingedits = ProvChange.objects.filter(changeid=change.changeid, status="Pending").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
##            if pendingedits:
##                pendingeditstable = model2table(request, title="New Edits:", objects=pendingedits,
##                                          fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])
##
##                grids.append(dict(title="Pending Edits",
##                                  content=pendingeditstable,
##                                  style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                                  width="99%",
##                                  ))
##
##            oldversions = ProvChange.objects.filter(changeid=change.changeid, status="NonActive").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
##            if oldversions:
##                oldversionstable = model2table(request, title="Revision History:", objects=oldversions,
##                                          fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])
##
##                grids.append(dict(title="Revision History",
##                                  content=oldversionstable,
##                                  style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                                  width="99%",
##                                  ))

        else:
            # newinfo event just added, so no change objects yet
            oldinfo = '<li style="list-style:none">'+markcountrychange(country, request.GET["fromname"], request.GET["fromcountry"]).encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Alternate names: '+request.GET["fromalterns"].encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; ISO: '+request.GET["fromiso"].encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; FIPS: '+request.GET["fromfips"].encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; HASC: '+request.GET["fromhasc"].encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital: '+request.GET["fromcapitalname"].encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital moved: '+request.GET["fromcapital"].encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Type: '+request.GET["fromtype"].encode("utf8")+"</li>"
            top = """
                            <a href="/contribute/view/{country}" style="float:left; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                            Back to {countrytext}
                            </a>
                            """.format(country=urlquote(country), countrytext=country.encode("utf8"))
            left = """
                            <div style="clear:both; text-align: left">
                            <h2 style="float:left">{oldinfo}</h2>
                            </div>
            """.format(oldinfo=oldinfo)
            mid = """
                    <h2><em>Changed info to:</em></h2>
                    """

            butstyle = 'text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;'
            plusbutstyle = 'text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:none; margin:5px;'

            setinfobutton = '<li style="list-style:none">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + '<a style="{plusbutstyle}" href="/contribute/add/{country}/{province}?{params}">&nbsp;Set info&nbsp;</a>'.format(country=urlquote(country), province=urlquote(prov), params=request.GET.urlencode(), plusbutstyle=plusbutstyle) + "</li>"
            right = """
                            <style>
                                #blackbackground a {{ color:white }}
                                #blackbackground a:visited {{ color:grey }}
                            </style>
                            
                            <div id="blackbackground">
                            <h2>{setinfobutton}</h2>
                            </div>  
            """.format(setinfobutton=setinfobutton)
            custombanner = """

                            {top}

                            <style>
                            td {{vertical-align:top}}
                            </style>
                            
                            <table width="99%" style="clear:both">
                            <tr>
                            
                            <td style="width:31%; padding:1%">
                            {left}
                            </td>

                            <td style="width:31%; padding:1%">
                            {mid}
                            </td>
                            
                            <td style="width:31%; padding:1%">
                            {right}
                            </td>

                            </tr>
                            </table>
                            """.format(top=top, left=left, mid=mid, right=right)
        
    elif typ == "Split":
        fields = ["toname","type","status"]
        if 'tocountry' in request.GET:
            # existing event
            changes = ProvChange.objects.filter(fromcountry=request.GET['fromcountry'],tocountry=request.GET['tocountry'], date=date,type="Breakaway",fromname=prov).exclude(status="NonActive")
        else:
            # new event, so cant know the tocountry yet
            changes = ProvChange.objects.filter(fromcountry=request.GET['fromcountry'],date=date,type="Breakaway",fromname=prov).exclude(status="NonActive")
        changes = changes.order_by("-added") # the dash reverses the order

        GET = request.GET.copy()
        GET["type"] = "NewInfo"
        newinfobut = '<a href="/contribute/view/{country}/{province}?{params}" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">Info</a>'.format(country=urlquote(country), province=urlquote(prov), params=GET.urlencode())

        top = """
                        <a href="/contribute/view/{country}" style="float:left; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Back to {countrytext}
			</a>
			""".format(country=urlquote(country), countrytext=country.encode("utf8"))
        
        left = """
                        <div style="clear:both; text-align: left">
                        <h2 style="float:left">{provtext} {newinfobut}</h2>
                        </div>
        """.format(newinfobut=newinfobut, provtext=markcountrychange(country, changes[0].fromname, changes[0].fromcountry).encode("utf8") if changes else prov.encode("utf8"))

        mid = """
                <h2><em>Split into:</em></h2>
                """
        
        butstyle = 'text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;'
        plusbutstyle = 'text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:none; margin:5px;'
        
        splitlist = "".join(('''<li style="padding:10px 0px; list-style:none">&rarr; {provtext} <a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>

				<div style="display:inline; border-radius:10px; ">
				<a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
				<img src="https://d30y9cdsu7xlg0.cloudfront.net/png/110875-200.png" height=30px style="filter:invert(100%)"/>
				</div>
				
                                </li>'''.format(pk=change.pk, provtext=markcountrychange(country, change.toname, change.tocountry).encode("utf8"), vouches=len(list(Vouch.objects.filter(changeid=change.changeid, status='Active'))))
                                 for change in changes))
        splitlist += '<li style="padding:10px 0px; list-style:none">' + '&nbsp;&nbsp;&nbsp;<a style="{plusbutstyle}" href="/contribute/add/{country}/{province}?{params}">&nbsp;Add New&nbsp;</a>'.format(country=urlquote(country), province=urlquote(prov), params=request.GET.urlencode(), plusbutstyle=plusbutstyle) + "</li>"
        right = """
                        <style>
                            #blackbackground a {{ color:white }}
                            #blackbackground a:visited {{ color:grey }}
                        </style>
                        
                        <div id="blackbackground">
                        <h2>{splitlist}</h2>
                        </div>  
        """.format(splitlist=splitlist)

        custombanner = """

                        {top}

                        <style>
                        td {{vertical-align:top}}
                        </style>
                        
                        <table width="99%" style="clear:both">
                        <tr>
                        
                        <td style="width:31%; padding:1%">
                        {left}
                        </td>

                        <td style="width:31%; padding:1%">
                        {mid}
                        </td>
                        
                        <td style="width:31%; padding:1%">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """.format(top=top, left=left, mid=mid, right=right)

    elif typ == "Merge":
        fields = ["fromname","type","status"]
        if 'fromcountry' in request.GET:
            # existing event
            changes = ProvChange.objects.filter(tocountry=request.GET['tocountry'],fromcountry=request.GET['fromcountry'],date=date,type="FullTransfer",toname=prov).exclude(status="NonActive")
        else:
            # new event, so fromcountry doesnt exist yet
            changes = ProvChange.objects.filter(tocountry=request.GET['tocountry'],date=date,type="FullTransfer",toname=prov).exclude(status="NonActive")
        changes = changes.order_by("-added") # the dash reverses the order

        butstyle = 'text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;'
        plusbutstyle = 'text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:none; margin:5px;'

        givelist = "".join(('''<li style="padding:10px 0px; list-style:none">{provtext} <a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>

                            <div style="display:inline; border-radius:10px; ">
                            <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
                            <img src="https://d30y9cdsu7xlg0.cloudfront.net/png/110875-200.png" height=30px style="filter:invert(100%)"/>
                            </div>

                            &rarr;</li>'''.format(pk=change.pk, provtext=markcountrychange(country, change.fromname, change.fromcountry).encode("utf8"), vouches=len(list(Vouch.objects.filter(changeid=change.changeid, status='Active')))) for change in changes))
        givelist += '<li style="padding:10px 0px; list-style:none">' + '<a href="/contribute/add/{country}/{province}?{params}" style="{plusbutstyle}">&nbsp;Add New&nbsp;</a>'.format(country=urlquote(country), province=urlquote(prov), params=request.GET.urlencode(), plusbutstyle=plusbutstyle) + "</li>"
        top = """
                        <a href="/contribute/view/{country}" style="float:left; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Back to {countrytext}
			</a>
			""".format(country=urlquote(country), countrytext=country.encode("utf8"))
        left = """			
                        <style>
                            #blackbackground a {{ color:white }}
                            #blackbackground a:visited {{ color:grey }}
                        </style>
                        
                        <div style="clear:both; text-align:left">
                        <h2 id="blackbackground" style="float:left">{givelist}</h2>
                        </div>  
        """.format(givelist=givelist)
        mid = """
                <h2><em>Merged into:</em></h2>
                """
        right = """
                        <div>
                        <h2>{provtext}</h2>
                        </div>
        """.format(provtext=markcountrychange(country, changes[0].toname, changes[0].tocountry).encode("utf8") if changes else prov.encode("utf8"))
        custombanner = """

                        {top}

                        <style>
                        td {{vertical-align:top}}
                        </style>
                        
                        <table width="99%" style="clear:both">
                        <tr>
                        
                        <td style="width:31%; padding:1%">
                        {left}
                        </td>

                        <td style="width:31%; padding:1%">
                        {mid}
                        </td>
                        
                        <td style="width:31%; padding:1%">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """.format(top=top, left=left, mid=mid, right=right)

    elif typ == "Transfer":
        fields = ["toname","type","status"]
        if 'fromcountry' in request.GET:
            # existing event
            changes = ProvChange.objects.filter(tocountry=request.GET['tocountry'],fromcountry=request.GET['fromcountry'],date=date,type="PartTransfer",toname=prov).exclude(status="NonActive")
        else:
            # new event, so fromcountry doesnt exist yet
            changes = ProvChange.objects.filter(tocountry=request.GET['tocountry'],date=date,type="PartTransfer",toname=prov).exclude(status="NonActive")
        changes = changes.order_by("-added") # the dash reverses the order

        butstyle = 'text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;'
        plusbutstyle = 'text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:none; margin:5px;'

        givelist = "".join(('''<li style="padding:10px 0px; list-style:none">{provtext} <a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>

                            <div style="display:inline; border-radius:10px; ">
                            <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
                            <img src="https://d30y9cdsu7xlg0.cloudfront.net/png/110875-200.png" height=30px style="filter:invert(100%)"/>
                            </div>

                            &rarr;</li>'''.format(pk=change.pk, provtext=markcountrychange(country, change.fromname, change.fromcountry).encode("utf8"), vouches=len(list(Vouch.objects.filter(changeid=change.changeid, status='Active')))) for change in changes))
        givelist += '<li style="padding:10px 0px; list-style:none">' + '<a href="/contribute/add/{country}/{province}?{params}" style="{plusbutstyle}">&nbsp;Add New&nbsp;</a>'.format(country=urlquote(country), province=urlquote(prov), params=request.GET.urlencode(), plusbutstyle=plusbutstyle) + "</li>"
        top = """
                        <a href="/contribute/view/{country}" style="float:left; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Back to {countrytext}
			</a>
			""".format(country=urlquote(country), countrytext=country.encode("utf8"))
        left = """			
                        <style>
                            #blackbackground a {{ color:white }}
                            #blackbackground a:visited {{ color:grey }}
                        </style>
                        
                        <div style="clear:both; text-align:left">
                        <h2 id="blackbackground" style="float:left">{givelist}</h2>
                        </div>  
        """.format(givelist=givelist)
        mid = """
                <h2><em>Transferred territory to:</em></h2>
                """
        right = """
                        <div>
                        <h2>{provtext}</h2>
                        </div>
        """.format(provtext=markcountrychange(country, changes[0].toname, changes[0].tocountry).encode("utf8") if changes else prov.encode("utf8"))
        custombanner = """

                        {top}

                        <style>
                        td {{vertical-align:top}}
                        </style>
                        
                        <table width="99%" style="clear:both">
                        <tr>
                        
                        <td style="width:31%; padding:1%">
                        {left}
                        </td>

                        <td style="width:31%; padding:1%">
                        {mid}
                        </td>
                        
                        <td style="width:31%; padding:1%">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """.format(top=top, left=left, mid=mid, right=right)

    elif typ == "Begin":
        fields = ["toname","type","status"]
        #changes = ProvChange.objects.filter(country=country,date=date,type="NewInfo",fromname=prov)
        if 'fromcountry' in request.GET:
            # existing event
            changes = ProvChange.objects.filter(tocountry=request.GET['tocountry'], fromcountry=request.GET['fromcountry'], date=date, type="Begin", toname=prov, bestversion=True).exclude(status="NonActive")
        else:
            # new event, so fromcountry doesnt exist yet
            changes = ProvChange.objects.filter(tocountry=request.GET['tocountry'], date=date, type="Begin", toname=prov, bestversion=True).exclude(status="NonActive")
        change = next((c for c in changes.order_by("-added")), None)

        if change:
            top = """
                            <a href="/contribute/view/{country}" style="float:left; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                            Back to {countrytext}
                            </a>
                            """.format(country=urlquote(country), countrytext=country.encode("utf8"))
            left = """
                            <div style="clear:both; text-align: left">
                            
                            </div>
            """

            mid = """
                    <h2><em>Province is created:</em></h2>
                    """
        
            newinfo = '''<li style="font-size:smaller; list-style:none"> {provtext}<a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a>

                        <div style="display:inline; border-radius:10px; ">
                        <a style="color:white; font-family:inherit; font-size:inherit; font-weight:bold;">{vouches}</a>
                        <img src="https://d30y9cdsu7xlg0.cloudfront.net/png/110875-200.png" height=30px style="filter:invert(100%)"/>
                        </div>

                        <br><br></li>'''.format(pk=change.pk, provtext=markcountrychange(country, change.toname, change.tocountry).encode("utf8"), vouches=len(list(Vouch.objects.filter(changeid=change.changeid, status='Active'))))
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Alternate names: '+change.toalterns.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; ISO: '+change.toiso.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; FIPS: '+change.tofips.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; HASC: '+change.tohasc.encode("utf8")+"</li>"
            right = """
                            <style>
                                #blackbackground a {{ color:white }}
                                #blackbackground a:visited {{ color:grey }}
                            </style>
                            
                            <div id="blackbackground">
                            <h2>{newinfo}</h2>
                            </div>  
            """.format(newinfo=newinfo)
            custombanner = """

                            {top}

                            <style>
                            td {{vertical-align:top}}
                            </style>
                            
                            <table width="99%" style="clear:both">
                            <tr>
                            
                            <td style="width:31%; padding:1%">
                            {left}
                            </td>

                            <td style="width:31%; padding:1%">
                            {mid}
                            </td>
                            
                            <td style="width:31%; padding:1%">
                            {right}
                            </td>

                            </tr>
                            </table>
                            """.format(top=top, left=left, mid=mid, right=right)


##            pendingedits = ProvChange.objects.filter(changeid=change.changeid, status="Pending").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
##            pendingeditstable = model2table(request, title="New Edits:", objects=pendingedits,
##                                      fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])
##
##            grids.append(dict(title="Pending Edits",
##                              content=pendingeditstable,
##                              style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                              width="99%",
##                              ))
##
##            oldversions = ProvChange.objects.filter(changeid=change.changeid, status="NonActive").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
##            oldversionstable = model2table(request, title="Revision History:", objects=oldversions,
##                                      fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])
##
##            grids.append(dict(title="Revision History",
##                              content=oldversionstable,
##                              style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                              width="99%",
##                              ))

        else:
            # begin event just added, so no change objects yet
            top = """
                            <a href="/contribute/view/{country}" style="float:left; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                            Back to {countrytext}
                            </a>
                            """.format(country=urlquote(country), countrytext=country.encode("utf8"))
            left = """
                            <div style="clear:both; text-align: left">
                            
                            </div>
            """

            mid = """
                    <h2><em>Province is created:</em></h2>
                    """

            toname = request.GET['toname']
            tocountry = request.GET['tocountry']
            toalterns = request.GET.get('toaltern', '')
            toiso = request.GET.get('toiso', '')
            tofips = request.GET.get('tofips', '')
            tohasc = request.GET.get('tohasc', '')
        
            newinfo = '''<li style="font-size:smaller; list-style:none"> {provtext}<a href="/contribute/add/{country}/{province}?{params}" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">Confirm</a>

                        <br><br></li>'''.format(provtext=markcountrychange(country, toname, tocountry).encode("utf8"),
                                                country=urlquote(country), province=urlquote(province), params=request.GET.urlencode())
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Alternate names: '+toalterns.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; ISO: '+toiso.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; FIPS: '+tofips.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; HASC: '+tohasc.encode("utf8")+"</li>"
            right = """
                            <style>
                                #blackbackground a {{ color:white }}
                                #blackbackground a:visited {{ color:grey }}
                            </style>
                            
                            <div id="blackbackground">
                            <h2>{newinfo}</h2>
                            </div>  
            """.format(newinfo=newinfo)
            custombanner = """

                            {top}

                            <style>
                            td {{vertical-align:top}}
                            </style>
                            
                            <table width="99%" style="clear:both">
                            <tr>
                            
                            <td style="width:31%; padding:1%">
                            {left}
                            </td>

                            <td style="width:31%; padding:1%">
                            {mid}
                            </td>
                            
                            <td style="width:31%; padding:1%">
                            {right}
                            </td>

                            </tr>
                            </table>
                            """.format(top=top, left=left, mid=mid, right=right)









            
##            fieldnames = [f.name for f in ProvChange._meta.get_fields()]
##            formfieldvalues = dict(((k,v) for form in form_list for k,v in form.cleaned_data.items() if k in fieldnames))
##            formfieldvalues["user"] = self.request.user.username
##            formfieldvalues["added"] = datetime.datetime.now()
##            formfieldvalues["bestversion"] = True
##            print formfieldvalues
##
##            eventvalues = dict(((k,v) for k,v in self.request.GET.items()))
##            print eventvalues
##
##            objvalues = dict(eventvalues)
##            objvalues.update(formfieldvalues)
##
##            # copy toinfo to frominfo
##            for fl in 'country name alterns iso fips hasc'.split():
##                objvalues['from'+fl] = objvalues.get('to'+fl)
##            
##            print 'final objvalues',objvalues
##            obj = ProvChange.objects.create(**objvalues)
##            obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions/edits
##            print obj
##            
##            obj.save()
##
##            prov = data["toname"]
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids, "custombanner":custombanner}
                  )


@login_required
def editevent(request):
    # wizard with one screen for editing prov info
    pass

@login_required
def addevent(request, country):
    # wizard that lets you add the type of event
    # then from or to prov info, and maybe source (or maybe source should get listbox to choose from previous)
    # then requires inputting at least one breakaway for splitevents (self is added automatically), and at least one for expansion events, and only one for newinfo
    # after first change added, goto viewevent screen to potentially add more...
    func = AddEventWizard.as_view(country=country)
    return func(request)
    

@login_required
def addchange(request, country, province):
    if request.GET["type"].lower().strip('"') == "split":
        func = AddSplitChangeWizard.as_view(country=country, province=province)
        print 888,func
    elif request.GET["type"].lower().strip('"') == "merge":
        func = AddMergeChangeWizard.as_view(country=country, province=province)
    elif request.GET["type"].lower().strip('"') == "transfer":
        func = AddTransferChangeWizard.as_view(country=country, province=province)
    elif request.GET["type"].lower().strip('"') == "newinfo":
        func = AddNewInfoChangeWizard.as_view(country=country, province=province)
    elif request.GET["type"].lower().strip('"') == "begin":
        # special handling, begin events dont require any further info
        # so just add immediately and redirect to same page
        objvalues = dict([(k,v) for k,v in request.GET.items()])
        objvalues["user"] = request.user.username
        objvalues["added"] = datetime.datetime.now()
        objvalues["bestversion"] = True
        print objvalues

        # copy toinfo to frominfo
        for fl in 'country name alterns iso fips hasc'.split():
            objvalues['from'+fl] = objvalues.get('to'+fl)

        sources = [get_object_or_404(Source, pk=int(pk)) for pk in objvalues.pop('sources').split(',') if pk]
        mapsources = [get_object_or_404(Map, pk=int(pk)) for pk in objvalues.pop('mapsources').split(',') if pk]
        print objvalues
        
        print 'final objvalues',objvalues
        obj = ProvChange.objects.create(**objvalues)
        obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions/edits
        print obj
        
        obj.save()
        for s in sources:
            obj.sources.add(s)
        for m in mapsources:
            obj.mapsources.add(m)
        obj.save()

        fields = ["tocountry","date","source","sources","mapsources","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]
        params = dict([(field,getattr(obj,field)) for field in fields])
        params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
        params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
        params = urlencode(params)
        eventlink = "/contribute/view/{country}/{prov}/?type=Begin&".format(country=urlquote(country), prov=urlquote(province)) + params

        return redirect(eventlink)
    
    return func(request)

##    if request.method == "POST":
##        print "data",request.POST
##        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
##        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))
##        formfieldvalues["user"] = request.user.username
##        formfieldvalues["added"] = datetime.date.today()
##        formfieldvalues["bestversion"] = True
##        print formfieldvalues
##        obj = ProvChange.objects.create(**formfieldvalues)
##        obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions
##        print obj
##        obj.save()
##
##        # hmmmm # need to make get request to editchange to just return basic html of the get
##
##        html = redirect("/provchanges/%s/view/" % obj.pk)
##
##    elif request.method == "GET":
##        args = {'typechange': TypeChangeForm(),
##                'generalchange': GeneralChangeForm(),
##                'fromchange': FromChangeForm(),
##                'geochange': GeoChangeForm(),
##                'tochange': ToChangeForm(),}
##        html = render(request, 'provchanges/submitchange.html', args)
##        
##    return html

def model2table(request, title, objects, fields):
    html = """
		<table class="modeltable"> 
		
			<style>
			table.modeltable {
				border-collapse: collapse;
				width: 100%;
			}

			th.modeltable, td.modeltable {
				text-align: left;
				padding: 8px;
			}

			tr.modeltable:nth-child(even){background-color: #f2f2f2}

			tr.modeltable:nth-child(odd){background-color: white}

			th.modeltable {
				background-color: orange;
				color: white;
			}
			</style>
		
			<tr class="modeltable">
				<th class="modeltable"> 
				</th>

				{% for field in fields %}
                                    <th class="modeltable">
                                        <b>{{ field }}</b>
                                    </th>
                                {% endfor %}
                                    
			</tr>
			</a>

                        {% if changelist %}
			
                            {% for pk,changerow in changelist %}
                                    <tr class="modeltable">
                                            <td class="modeltable">
                                                <a href="{% url 'viewchange' pk=pk %}">View</a>
                                            </td>
                                            
                                            {% for value in changerow %}
                                                <td class="modeltable">{{ value }}</td>
                                            {% endfor %}
                                            
                                    </tr>
                            {% endfor %}

                        {% else %}

                            <tr class="modeltable">
                            <td class="modeltable"></td>
                            {% for _ in fields %}
                                <td class="modeltable"> - </td>
                            {% endfor %}
                            </tr>

                        {% endif %}
                            
		</table>
                """
    changelist = [(change.pk, [getattr(change,field) for field in fields]) for change in objects]
    rendered = Template(html).render(Context({"request":request, "fields":fields, "changelist":changelist, "title":title}))
    return rendered


def lists2table(request, lists, fields, classname="listtable", color='orange'):
    html = """
		<table class="{{ classname }}"> 
		
			<style>
			table.{{ classname }} {
				border-collapse: collapse;
				width: 100%;
			}

			th.{{ classname }}, td.{{ classname }} {
				text-align: left;
				padding: 8px;
			}

			tr.{{ classname }}:nth-child(even){background-color: #f2f2f2}

			tr.{{ classname }}:nth-child(odd){background-color: white}

			th.{{ classname }} {
				background-color: {{ color }};
				color: white;
			}
			</style>
		
			<tr class="{{ classname }}">
				<th class="{{ classname }}"> 
				</th>

				{% for field in fields %}
                                    <th class="{{ classname }}">
                                        <b>{{ field }}</b>
                                    </th>
                                {% endfor %}
                                    
			</tr>
			</a>
			
			{% for url,row in lists %}
				<tr class="{{ classname }}">
					<td class="{{ classname }}">
					{% if url %}
                                            <a href="{{ url }}">View</a>
                                        {% endif %}
					</td>
					
                                        {% for value in row %}
                                            <td class="{{ classname }}">{{ value | safe}}</td>
                                        {% endfor %}
					
				</tr>
			{% endfor %}
		</table>
                """
    rendered = Template(html).render(Context({"request":request, "fields":fields, "lists":lists, "classname":classname, "color":color}))
    return rendered

def withdrawchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)
    if request.user.username == change.user or request.user.is_staff():
        change.status = "NonActive"
        change.save()

    return redirect("/provchange/{pk}/view/".format(pk=pk) )

def resubmitchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)
    if request.user.username == change.user or request.user.is_staff():
        change.status = "Pending"
        change.save()

    return redirect("/provchange/{pk}/view/".format(pk=pk) )

def comments2html(request, allcomments, country, changeid=None, commentheadercolor="orange"):
    topics = []
    for c in allcomments.distinct('title'):
        title = c.title
        print title
        comments = allcomments.filter(title=title).order_by("added") # the dash reverses the order
        fields = ["added","user","text","withdraw"]
        rows = []
        for c in comments:
            rowdict = dict([(f,getattr(c, f, "")) for f in fields])
            rowdict['pk'] = c.pk
            rowdict['added'] = rowdict['added'].strftime('%Y-%M-%d %H:%M')
            rows.append(rowdict)
        addreplyobj = Comment(user=request.user.username, country=country, changeid=changeid,
                                added=datetime.datetime.now(), title=title)
        replyform = ReplyForm(instance=addreplyobj).as_p()
        topics.append((title,rows,replyform))

    print topics

    # new comm    
    addcommentobj = Comment(user=request.user.username, country=country, changeid=changeid,
                            added=datetime.datetime.now())
    new_comment = CommentForm(instance=addcommentobj).as_p()
    
    # template
    templ = """
			{% if topics %}
                            {% for title,comments,replyform in topics %}
                                <div style="font-size:small; padding-left:10px; padding-right:10px;" >
                                    <div style="float:left; padding:0px; width:90%">
                                        <h3 style="background-color:{{ commentheadercolor }}; color:white; padding:5px; border-radius:5px;">{{ title }}</h3>
                                        <p style="float:right;">
                                            {{ comments.0.added }}
                                            {% if request.user.username == comments.0.user %}
                                                <a href="/dropcomment/{{ comments.0.pk }}">
                                                    <img style="padding-left:10px" src="https://d30y9cdsu7xlg0.cloudfront.net/png/3058-200.png" height=14px/>
                                                </a>
                                            {% endif %}
                                        </p>
                                        <h4>
                                        {{ comments.0.user }}
                                        </h4>
                                        <p style="float:left">{{ comments.0.text }}</p>
                                    </div>

                                    {% for comment in comments|slice:"1:" %}
                                    <div style="padding-left:65px; padding-right:10px;" >
                                        <div style="float:left; padding:0px; width:90%">
                                            <p style="float:right">
                                                {{ comments.0.added }}
                                                {% if request.user.username == comment.user %}
                                                    <a href="/dropcomment/{{ comment.pk }}">
                                                        <img style="padding-left:10px" src="https://d30y9cdsu7xlg0.cloudfront.net/png/3058-200.png" height=14px/>
                                                    </a>
                                                {% endif %}
                                            </p>
                                            <h4>{{ comment.user }}</h4>
                                            <p style="float:left">{{ comment.text }}</p>
                                        </div>
                                    </div>
                                    {% endfor %}

                                    <div style="margin-left:40px">
                                            <h4 onClick="var replyform = document.getElementById('replyform{{ forloop.counter0 }}'); replyform.style.display = replyform.style.display === 'none' ? '' : 'none';" style="text-decoration:underline; clear:both; margin-left:80px; padding:10px">Reply</h4>
                                            <form id="replyform{{ forloop.counter0 }}" style="display:none; padding-left:80px" action="/addcomment/" method="post">
                                            {% csrf_token %}
                                            {{ replyform }}
                                            <input type="submit" value="Reply" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:7px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:3px;">
                                            </form>
                                    </div>
                                    
                                </div>
                            {% endfor %}
			{% else %}
				There are currently no comments.
			{% endif %}

			<h4 style="clear:both; margin-left:20px">New Topic:</h4>
			<div style="margin-left:60px">
				<form action="/addcomment/" method="post">
				{% csrf_token %}
				{{ new_comment }}
	                	<input type="submit" value="Comment" style="text-align:center; background-color:{{ commentheadercolor }}; color:white; border-radius:10px; padding:7px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:3px;">
				</form>
		</div>
		"""
    rendered = Template(templ).render(RequestContext(request, {'topics':topics, 'new_comment':new_comment, 'commentheadercolor':commentheadercolor}))
    return rendered

def viewchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)

    if change.type in "NewInfo Breakaway":
        conflicting = ProvChange.objects.filter(status__in="Active Pending".split(), fromcountry=change.fromcountry, tocountry=change.tocountry, date=change.date, type=change.type, fromname=change.fromname, toname=change.toname, bestversion=True).exclude(pk=change.pk)
        conflictingfields = ["date","type","fromname","fromcountry","toname","tocountry","user","added","status"]
    elif change.type in "PartTransfer FullTransfer Begin":
        # UNSURE: should we not match on same date here, bc begin should only happen once, so any duplicates on different dates are conflicting?
        # on other hand one should be able to say begin for specific provinces, so not necessarily true...
        conflicting = ProvChange.objects.filter(status__in="Active Pending".split(), fromcountry=change.fromcountry, tocountry=change.tocountry, date=change.date, type=change.type, fromname=change.fromname, toname=change.toname, bestversion=True).exclude(pk=change.pk)
        conflictingfields = ["date","type","fromname","fromcountry","toname","tocountry","user","added","status"]

    notes = []
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
        notes.append(note)
    if conflicting:
        # custom table
        html = """
                    <table class="conftable"> 
                    
                            <style>
                            table.conftable {
                                    border-collapse: collapse;
                                    width: 100%;
                            }

                            th.conftable, td.conftable {
                                    text-align: left;
                                    padding: 8px;
                            }

                            tr.conftable:nth-child(even){background-color: none}

                            tr.conftable:nth-child(odd){background-color: none}

                            th.conftable {
                                    background-color: black;
                                    color: white;
                            }
                            </style>
                    
                            <tr class="conftable">
                                    <th class="conftable"> 
                                    </th>

                                    {% for field in fields %}
                                        <th class="conftable">
                                            <b>{{ field }}</b>
                                        </th>
                                    {% endfor %}
                                        
                            </tr>
                            </a>

                            {% if changelist %}
                            
                                {% for pk,changerow in changelist %}
                                        <tr class="conftable">
                                                <td class="conftable">
                                                    <a href="{% url 'viewchange' pk=pk %}">View</a>
                                                </td>
                                                
                                                {% for value in changerow %}
                                                    <td class="conftable">{{ value }}</td>
                                                {% endfor %}
                                                
                                        </tr>
                                {% endfor %}

                            {% else %}

                                <tr class="conftable">
                                <td class="conftable"></td>
                                {% for _ in fields %}
                                    <td class="conftable"> - </td>
                                {% endfor %}
                                </tr>

                            {% endif %}
                                
                    </table>
                    """
        changelist = [(c.pk, [getattr(c,field) for field in conflictingfields]) for c in conflicting]
        conflictingtable = Template(html).render(Context({"request":request, "fields":conflictingfields, "changelist":changelist}))

        
        note = """
                <div style="background-color:rgb(248,234,150); outline: black solid thick; padding:1%%; font-family: comic sans ms">
                <p style="font-size:large; font-weight:bold">Note:</p>
                <p style="font-size:medium; font-style:italic">
                There seems to be conflicting versions of this change:
                </p>
                    %s
                </div>
                <br>
                """ % conflictingtable
        notes.append(note)

    if change.type == "Breakaway":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["fromcountry","tocountry","date","source","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Split&".format(country=urlquote(change.fromcountry), prov=urlquote(change.fromname)) + params
    elif change.type == "FullTransfer":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["tocountry","fromcountry","date","source","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Merge&".format(country=urlquote(change.tocountry), prov=urlquote(change.toname)) + params
    elif change.type == "PartTransfer":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["tocountry","fromcountry","date","source","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Transfer&".format(country=urlquote(change.tocountry), prov=urlquote(change.toname)) + params
    elif change.type == "NewInfo":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["fromcountry","tocountry","date","source","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=NewInfo&".format(country=urlquote(change.fromcountry), prov=urlquote(change.fromname)) + params
    elif change.type == "Begin":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["tocountry","fromcountry","date","source","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Begin&".format(country=urlquote(change.tocountry), prov=urlquote(change.toname)) + params
    print 99999,change.type, change
    print 1111,eventlink

    pendingedits = ProvChange.objects.filter(changeid=change.changeid, status="Pending").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
    pendingeditstable = model2table(request, title="New Edits:", objects=pendingedits,
                              fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])

    oldversions = ProvChange.objects.filter(changeid=change.changeid, status="NonActive").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
    oldversionstable = model2table(request, title="Revision History:", objects=oldversions,
                              fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])

    vouches = list(Vouch.objects.filter(changeid=change.changeid, status='Active'))
    canvouch = request.user.username != change.user
    hasvouched = bool(vouches)

    args = {'pk': pk,
            'notes': notes,
            'canvouch': canvouch,
            'hasvouched': hasvouched,
            'vouches': vouches,
            'eventlink': eventlink,
            'metachange': MetaChangeForm(instance=change),
            'typechange': TypeChangeForm(instance=change),
            'generalchange': GeneralChangeForm(instance=change),
##            'histomap': HistoMapForm(instance=change),
##            'georef': GeorefForm(instance=change),
            'fromchange': FromChangeForm(instance=change),
            'geochange': GeoChangeForm(instance=change, country=change.tocountry, province=change.toname, date=change.date),
            'tochange': ToChangeForm(instance=change),
            "pendingeditstable": pendingeditstable,
            "oldversionstable": oldversionstable,
            }
    
    for key,val in args.items():
        if hasattr(val,"fields"):
            for field in val.fields.values():
                field.widget.attrs['readonly'] = "readonly"

    # comments by topic
    allcomments = Comment.objects.filter(changeid=change.changeid, status="Active")
##    topics = []
##    for c in allcomments.distinct('title'):
##        title = c.title
##        print title
##        comments = allcomments.filter(title=title).order_by("added") # the dash reverses the order
##        fields = ["added","user","text","withdraw"]
##        rows = []
##        for c in comments:
##            rowdict = dict([(f,getattr(c, f, "")) for f in fields])
##            rowdict['added'] = rowdict['added'].strftime('%Y-%M-%d %H:%M')
##            if rowdict['user'] == request.user.username:
##                rowdict['withdraw'] = '''
##                                <div style="display:inline; border-radius:10px; ">
##                                <a href="/dropcomment/{pk}">
##                                <img src="https://d30y9cdsu7xlg0.cloudfront.net/png/3058-200.png" height=30px/>
##                                </a>
##                                </div>
##                                    '''.format(pk=c.pk)
##            rows.append(rowdict)
##        addreplyobj = Comment(user=request.user.username, country=change.fromcountry, changeid=change.changeid,
##                                added=datetime.datetime.now(), title=title)
##        replyform = ReplyForm(instance=addreplyobj).as_p()
##        topics.append((title,rows,replyform))
##
##    print topics

    #topics = [(title,comm) for title,comm in sorted(topics.items(), key=lambda t,c: c[0]['added'])]
    args['topics'] = comments2html(request, allcomments, change.fromcountry, change.changeid, "rgb(27,138,204)")

    # try to emulate https://cloud.netlifyusercontent.com/assets/344dbf88-fdf9-42bb-adb4-46f01eedd629/b549e4a7-f9d9-4f64-b597-21c7d8f2a166/facebook-comments.png
    # user icon: "https://cdn4.iconfinder.com/data/icons/gray-user-management/512/rounded-512.png"


    

    

    # count of all comm
    comments = allcomments.count()
    args['comments'] = comments
                
    html = render(request, 'provchanges/viewchange.html', args)
        
    return html

@login_required
def editchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)

    if request.method == "POST":
        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))

        # post requests are different, so multivalue entries must be gotten as list
        formfieldvalues["sources"] = request.POST.getlist('sources')
        formfieldvalues["mapsources"] = request.POST.getlist('mapsources')
        
        formfieldvalues["user"] = request.user.username
        formfieldvalues["added"] = datetime.datetime.now()
        formfieldvalues["status"] = "Pending"

        if request.user.username == change.user:
            for c in ProvChange.objects.filter(changeid=change.changeid):
                # all previous versions by same user become nonactive and nonbestversion
                c.bestversion = False
                c.status = "NonActive"
                c.save()
            formfieldvalues["bestversion"] = True

        sources = [get_object_or_404(Source, pk=int(pk)) for pk in formfieldvalues.pop('sources') if pk]
        mapsources = [get_object_or_404(Map, pk=int(pk)) for pk in formfieldvalues.pop('mapsources') if pk]

        formfieldvalues['transfer_map'] = get_object_or_404(Map, pk=int(formfieldvalues['transfer_map'])) if formfieldvalues.get('transfer_map') else None
        
        print formfieldvalues
        print sources, mapsources

        for k,v in formfieldvalues.items():
            setattr(change, k, v)

        geoform = GeoChangeForm(instance=change, data=formfieldvalues, country=change.tocountry, province=change.toname, date=change.date)
        geoform.is_valid()
        change.transfer_geom = geoform.clean()["transfer_geom"]
        change.pk = None # nulling the pk will add a modified copy of the instance
                    
        change.save()
        for s in sources:
            change.sources.add(s)
        for m in mapsources:
            change.mapsources.add(m)
        change.save()

        html = redirect("/provchange/%s/view/" % change.pk)
        
    elif request.method == "GET":
        args = {'pk': pk,
                'typechange': TypeChangeForm(instance=change),
                'generalchange': GeneralChangeForm(instance=change),
                'fromchange': FromChangeForm(instance=change),
##                'histomap': HistoMapForm(instance=change),
##                'georef': GeorefForm(instance=change),
                'geochange': GeoChangeForm(instance=change, country=change.tocountry, province=change.toname, date=change.date),
                'tochange': ToChangeForm(instance=change),}
        html = render(request, 'provchanges/editchange.html', args)
        
    return html






# Date...

class CustomDateWidget(forms.TextInput):

    ### WARNING: id_1-date is hacky for now, may not always work...
    
    def render(self, name, value, attrs = None):
        output = super(CustomDateWidget, self).render(name, value, attrs)
        output += """
<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/smoothness/jquery-ui.css">
<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>

<script>
$('#id_0-date').datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: "yy-mm-dd",
    defaultDate: "2014-12-31",
    yearRange: '1946:2014',
    showOn: "both",
    buttonImage: 'http://jqueryui.com/resources/demos/datepicker/images/calendar.gif',
    buttonImageOnly: true,
});
$(".ui-datepicker-trigger").css("margin-bottom","-3px");
</script>
"""
        return output

    


# Auth forms

from .models import User

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
        fields = ["first_name","last_name","email","affiliation"]

@login_required
def account_edit(request):
    userobj = User.objects.get(username=request.user)
    form = UserInfoForm(instance=userobj)
    if request.POST:
        userobj.first_name = request.POST["first_name"]
        userobj.last_name = request.POST["last_name"]
        userobj.email_name = request.POST["email"]
        userobj.affiliation = request.POST["affiliation"]
        print userobj.first_name
        userobj.save()
        return redirect("/account/")
    else:
        ##form.fields["email"].widget.attrs['readonly'] = "readonly"
        return render(request, 'provchanges/accountedit.html', {"user":request.user, "userinfoform":form}
                      )

class UploadFileForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UploadFileForm, self).__init__(*args, **kwargs)

    def as_p(self):
        templ = """
                    <form method="post" action="/update/" enctype="multipart/form-data">
                        {% csrf_token %}
                        <table>
                        {{ form }}
                        </table>
                        <br>
                        <input type="submit" value="Update Boundary Data" onClick="alert('The website boundary data will now be updated, this may take a while.');" style="font-weight:bold; background-color:rgb(7,118,183); color:white; border-radius:5px; padding:5px">
                        </input>
                    </form>
                """
        rendered = Template(templ).render(RequestContext(self.request, {'form':self}))
        return rendered

@login_required
def account(request):
    userobj = User.objects.get(username=request.user)
    userform = UserInfoForm(instance=userobj)

    changes = ProvChange.objects.filter(user=request.user.username).order_by("-added")   # the dash reverses the order
    pending = ProvChange.objects.filter(user=request.user.username, status="Pending")
    comments = Comment.objects.filter(user=request.user.username, status="Active").order_by("-added") # the dash reverses the order
    
    grids = []
    bannertitle = "User Settings for '%s'" % request.user
    
##    if edit:
##        bannerleft = """
##                    <form action="/account/edit/" method="post">
##                    
##                    <div style="text-align:center">
##                            {userinfoform}
##                    </div>
##                    
##                    <div style="text-align:center">
##                        <input type="submit" value="Submit" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; float:right; margin:10px;">
##                    </div>
##                    <br>
##
##                    </form>
##                    """.format(userinfoform=userform.as_p())
##    else:
    
    for field in userform.fields.values():
        field.widget.attrs['readonly'] = "readonly"
        field.widget.attrs["style"] = 'background-color:black; color:white'
    bannerleft = """
                <table style="text-align:right; padding-left:20%; padding-bottom:3%;">
                    {userinfoform}
                </table>
                
                <div style="text-align:center">
                    <a href="/account/edit" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                        Edit
                    </a>                    
                </div>
                <br>
                """.format(userinfoform=userform.as_table(),
                           )

##    for field in userform.fields.values():
##        field.widget.attrs['readonly'] = "readonly"
##        field.widget.attrs["style"] = 'background-color:black'
##    bannertitle = "User Settings for '%s'" % request.user
##    bannerleft = """
##                <div style="text-align:center">
##                    {userinfoform}
##                </div>
##                <br>
##                """.format(userinfoform=userform.as_p())

    if request.user.is_staff:
        uploadform = UploadFileForm(request=request).as_p()
        bannerright = """
                        {uploadform}
                        
                        <br><br>
                        <a href="/logout" style="background-color:orange; color:white; border-radius:5px; padding:5px">
                            <b>Logout</b>
                        </a>
                        """.format(uploadform=uploadform)
    else:
        bannerright = """
                        <br><br>
                        <a href="/logout" style="background-color:orange; color:white; border-radius:5px; padding:5px">
                            <b>Logout</b>
                        </a>
                        """

    custombanner = """
                    <h2>{bannertitle}</h2>
                    
                        <table width="99%" style="clear:both; padding:0px; margin:0px">
                        <tr>

                        <td style="width:20%; padding:1%; text-align:center; padding:0px; margin:0px; vertical-align:middle">
                            <img width="80%" src="https://cdn4.iconfinder.com/data/icons/gray-user-management/512/rounded-512.png">
                        </td>
                        
                        <td style="width:60%; padding:1%; text-align:center; padding:0px; margin:0px; vertical-align:middle">
                        {left}
                        </td>
                        
                        <td style="width:20%; padding:1%; padding:0px; margin:0px; vertical-align:top; text-align:center">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """.format(left=bannerleft, right=bannerright, bannertitle=bannertitle)

    # stats
##    qstats = """
##                    <b>
##                    <table style="font-size:small">
##                    <tr style="vertical-align:text-top">
##                        <td>
##                        <h2>{changes}</h2>
##                        Total Contributions
##                        </td>
##                        <td>
##                        <h2>{modifs}</h2>
##                        Edits Made
##                        </td>
##                        <td>
##                        <h2>{comments}</h2>
##                        Comments
##                        </td>
##                    </tr>
##                    </table>
##                    </b>
##            """.format(changes=changes.count(),
##                       modifs=changes.count() - pending.count(),
##                       comments=comments.count())
##    grids.append(dict(title="Overview:",
##                      content=qstats,
##                      style="padding:0; margins:0",#background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                      width="100%",
##                      ))    

    # user contribs
    rendered = model2table(request, '', changes[:50], ['user','added','fromcountry','fromname','type','status'])

    grids.append(dict(title="Your Contributions (last 50 only):", #most recent, 1-%s of %s):" % (min(changes.count(),50), changes.count()),
                      content=rendered,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="100%",
                      ))

    # comments
    fields = ["added","country","title","text","withdraw"]
    lists = []
    for c in comments[:10]:
        rowdict = dict([(f,getattr(c, f, "")) for f in fields])
        rowdict['added'] = rowdict['added'].strftime('%Y-%M-%d %H:%M')
        if c.user == request.user.username:
            rowdict['withdraw'] = '''
                            <div style="display:inline; border-radius:10px; ">
                            <a href="/dropcomment/{pk}">
                            <img src="https://d30y9cdsu7xlg0.cloudfront.net/png/3058-200.png" height=20px/>
                            </a>
                            </div>
                                '''.format(pk=c.pk)
        row = [rowdict[f] for f in fields]
        lists.append(("",row))
    content = lists2table(request, lists=lists,
                                        fields=["Added","Country","Title","Comment",""])

    grids.append(dict(title="Your Comments (last 10 only):", #most recent, 1-%s of %s):" % (min(comments.count(),10), comments.count()),
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="93%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "custombanner":custombanner}
                  )












# Event forms

##class GridSelectMultipleWidget(forms.CheckboxSelectMultiple):
##
##    def render(self, name, value, attrs=None):
##        choices = [(value,decor) for value,decor in self.choices]
##        html = """
##            <div style="width:98%;" class="gridselectmultiple">
##            {% for value,decor in choices %}
##                <div style="float:left; width:25%">
##                    <input type="checkbox" value="{{ value }}" name="{{ name }}" style="float:left">
##                    <div style="float:left">{{ decor|safe }}</div>
##                </div>
##            {% endfor %}
##            </div>
##
##            <div style="clear:both;"></div>
##            """
##        rendered = Template(html).render(Context({"choices":choices, 'name':name, 'value':value}))
##        return rendered
##
##class GridSelectOneWidget(forms.RadioSelect):
##
##    def render(self, name, value, attrs=None):
##        choices = [(value,decor) for value,decor in self.choices]
##        html = """
##            <div style="width:98%;" class="gridselectone">
##            {% for value,decor in choices %}
##                <div style="float:left; width:25%">
##                    <input type="radio" value="{{ value }}" name="{{ name }}" style="float:left">
##                    <div style="float:left">{{ decor|safe }}</div>
##                </div>
##            {% endfor %}
##            </div>
##
##            <div style="clear:both;"></div>
##            """
##        rendered = Template(html).render(Context({"choices":choices, 'name':name, 'value':value}))
##        return rendered

class ListTextWidget(forms.TextInput):
    # from http://stackoverflow.com/questions/24783275/django-form-with-choices-but-also-with-freetext-option
    def __init__(self, data_list, name, *args, **kwargs):
        super(ListTextWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list':'list__%s' % self._name})

    def render(self, name, value, attrs=None):
        text_html = super(ListTextWidget, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return (text_html + data_list)

class SourceEventForm(forms.ModelForm):

    icon = "https://cdn0.iconfinder.com/data/icons/huge-black-icons/512/Info.png"
    step_title = "Source of Information"
    step_descr = """
                   Where are you getting the information from? 
                
                   """

    class Meta:
        model = ProvChange
        fields = ['source', 'sources', 'mapsources']
##        widgets = dict(sources=forms.CheckboxSelectMultiple(renderer=SelectMultipleOrCreate),
##                       mapsources=forms.CheckboxSelectMultiple(renderer=SelectMultipleOrCreate))

    def __init__(self, *args, **kwargs):
        super(SourceEventForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            country = kwargs["initial"]["fromcountry"]
        elif 'instance' in kwargs:
            country = kwargs["instance"].fromcountry
        else:
            raise Exception('Either initial or instance must be set')
        self.country = country

        # new
        sources = get_country_sources(country)
        self.suggested_sources = sorted([(s.pk, "{title} - {citation}".format(title=s.title.encode('utf8'), citation=s.citation.encode('utf8'))) for s in sources])
        #self.fields["sources"].widget = GridSelectMultipleWidget(choices=[(s.pk, SourceForm(instance=s).as_griditem()) for s in sources])
        #self.fields["sources"].widget = forms.CheckboxSelectMultiple(choices=[(s.pk, "{title} - {citation}".format(title=s.title.encode('utf8'), citation=s.citation.encode('utf8'))) for s in sources])
        
        maps = get_country_maps(country)
        self.suggested_mapsources = sorted([(m.pk, "{title} ({yr})".format(yr=m.year, title=m.title.encode('utf8'))) for m in maps])
        #self.fields["mapsources"].widget = GridSelectMultipleWidget(choices=[(m.pk, MapForm(instance=m).as_griditem()) for m in maps])
        #self.fields["mapsources"].widget = forms.CheckboxSelectMultiple(choices=[(m.pk, "{yr} - {title}".format(yr=m.year, title=m.title.encode('utf8'))) for m in maps])

        # old, to be phased out
        sources = [r.source for r in (ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)).annotate(count=Count('source')).order_by('-count')]
        if sources:
            mostcommon = sources[0]
            sources = sorted(set(sources))
            #self.fields["source"].widget = ListTextWidget(data_list=sources, name="sources", attrs=dict(type="text",size=120,autocomplete="on"))
            self.fields["source"].widget = forms.Textarea(attrs=dict(style='width:90%; font:inherit'))
            self.fields['source'].initial = mostcommon

    def clean(self):
        # store the sources and mapsources objects as pks
        cleaned_data = super(SourceEventForm, self).clean()
        cleaned_data['sources'] = ','.join([str(s.pk) for s in cleaned_data['sources']])
        cleaned_data['mapsources'] = ','.join([str(m.pk) for m in cleaned_data['mapsources']])
        return cleaned_data

    def as_p(self):
        html = """
                    <div style="margin-left:2%">

                        <p>Select all sources that were used to code this change.
                        This includes information that was inferred by visually comparing maps.
                        </p>
                        
                        <p>                        
                        If you have not already done so, go ahead and <a href="/addsource/?country={{ country }}">register the source(s) for this country now.</a> 
                        </p>

                        <div style="">
                        {{ form.source.label_tag }}
                        {{ form.source }}
                        </div>

                        <p>
					<div style="width:45%; margin-left:20px; display:inline-block"><em>Suggested Sources:</em>
                                            <table style="margin-left:20px">
                                            {% for id,lab in form.suggested_sources %}
                                                <tr>
                                                <td style="width:60px; vertical-align:top"><img height="20px" src="http://www.pvhc.net/img28/hgicvxtrvbwmfpuozczo.png"><div style="display:inline-block; vertical-align:top">{{ id }}</div></td>
                                                <td style="padding-left:5px; vertical-align:top"><a target="_blank" href="/viewsource/{{ id }}/">{{ lab }}</a></td>
                                                </tr>
                                            {% endfor %}
                                            </table>
					</div>
					<div style="width:45%; display:inline-block"><em>Suggested Maps:</em>
                                            <table style="margin-left:20px">
                                            {% for id,lab in form.suggested_mapsources %}
                                                <tr>
                                                <td style="width:60px; vertical-align:top"><img height="20px" src="http://icons.iconarchive.com/icons/icons8/android/512/Maps-Map-Marker-icon.png"><div style="display:inline-block; vertical-align:top">{{ id }}</div></td>
                                                <td style="padding-left:5px; vertical-align:top"><a target="_blank" href="/viewsource/{{ id }}/">{{ lab }}</a></td>
                                                </tr>
                                            {% endfor %}
                                            </table>
					</div>
			</p>
                    </div>
                    """
        
        rendered = Template(html).render(Context({"form":self, 'country':urlquote(self.country)}))
        return rendered
        
from django.forms.widgets import RadioFieldRenderer

EVENTTYPEINFO = {"NewInfo": {"label": "NewInfo",
                         "short": "A change was made to a province's name, codes, or capital.",
                          "descr": """
                                    
                                    """,
                          "img": '<img style="width:100px" src="/static/webnewinfo.png"/>',
                          },
              "Split": {"label": "Split",
                               "short": "A province split into multiple new ones or lost territory to one or more breakaway regions.",
                              "descr": """
                                        
                                        """,
                              "img": '<img style="width:100px" src="/static/websplit.png"/>',
                              },
             "Merge": {"label": "Merge",
                              "short": "One or more provinces merged entirely into another province.",
                              "descr": """
                                        
                                        """,
                              "img": '<img style="width:100px" src="/static/webmerge.png"/>',
                              },
             "Transfer": {"label": "Transfer",
                              "short": "One or more provinces gave parts of their territories to another province.",
                              "descr": """
                                        
                                        """,
                              "img": '<img style="width:100px" src="/static/webtransfer.png"/>',
                              },
             "Begin": {"label": "Begin",
                              "short": "Marks the earliest known record for this province.",
                              "descr": """
                                        
                                        """,
                              "img": '<img style="width:100px" src="/static/webbegin.png"/>',
                              },
               }

class TypeEventRenderer(RadioFieldRenderer):

    def render(self):
        choices = [(w,EVENTTYPEINFO[w.choice_label]) for w in self]
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

class TypeEventForm(forms.Form):

    icon = "https://cdn1.iconfinder.com/data/icons/ui-glynh-04-of-5/100/UI_Glyph_07-07-512.png"
    step_title = "Type of Change"
    step_descr = """
                    What type of event was it? 
                   """
    type = forms.ChoiceField(choices=[("NewInfo","NewInfo"),("Split","Split"),("Merge","Merge"),("Transfer","Transfer"),("Begin","Begin")], widget=forms.RadioSelect(renderer=TypeEventRenderer))

##    class Meta:
##        widgets = {"type": forms.RadioSelect(renderer=TypeEventRenderer) }

class FromEventForm(forms.ModelForm):

    icon = "/static/fromicon.png"
    step_title = "From Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'fromcountry fromname fromalterns fromiso fromfips fromhasc fromcapitalname fromcapital fromtype'.split()

    def __init__(self, *args, **kwargs):
        self.step_descr = kwargs.pop("step_descr", "")
        super(FromEventForm, self).__init__(*args, **kwargs)
        countrylist = set((r.fromcountry for r in ProvChange.objects.distinct("fromcountry"))) | set((r.tocountry for r in ProvChange.objects.distinct("tocountry")))
        countrylist.update((c[0] for c in countries))
        countrylist = sorted(countrylist)
        self.fields["fromcountry"].widget = ListTextWidget(data_list=countrylist, name="fromcountrylist")
        
        country = kwargs["initial"]["fromcountry"]
        provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
        provlist = set((r.fromname for r in provs.distinct("fromname"))) | set((r.toname for r in provs.distinct("toname")))
        provlist = sorted(provlist)
        self.fields["fromname"].widget = ListTextWidget(data_list=provlist, name="fromprovlist")

class ToEventForm(forms.ModelForm):

    icon = "/static/toicon.png"
    step_title = "To Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'tocountry toname toalterns toiso tofips tohasc tocapitalname tocapital totype'.split()

    def __init__(self, *args, **kwargs):
        self.step_descr = kwargs.pop("step_descr", "")
        super(ToEventForm, self).__init__(*args, **kwargs)
        countrylist = set((r.fromcountry for r in ProvChange.objects.distinct("fromcountry"))) | set((r.tocountry for r in ProvChange.objects.distinct("tocountry")))
        countrylist.update((c[0] for c in countries))
        countrylist = sorted(countrylist)
        self.fields["tocountry"].widget = ListTextWidget(data_list=countrylist, name="tocountrylist")
        
        country = kwargs["initial"]["tocountry"]
        provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
        provlist = set((r.fromname for r in provs.distinct("fromname"))) | set((r.toname for r in provs.distinct("toname")))
        provlist = sorted(provlist)
        self.fields["toname"].widget = ListTextWidget(data_list=provlist, name="toprovlist")

class DateForm(forms.Form):

    step_title = "Date"
    step_descr = """
                    On what date did the changes occur? 
                   """
    year = forms.ChoiceField(choices=[(yr,yr) for yr in range(1800, 2016+1)], initial=1950)
    month = forms.ChoiceField(choices=[(mn,mn) for mn in range(1, 12+1)])
    day = forms.ChoiceField(choices=[(dy,dy) for dy in range(1, 31+1)])

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs.update({'style' : 'font-size: x-large'})
        self.fields['month'].widget.attrs.update({'style' : 'font-size: x-large'})
        self.fields['day'].widget.attrs.update({'style' : 'font-size: x-large'})


class AddDateWizard(SessionWizardView):
    form_list = [   DateForm,
                      ]

    country = None

    def __iter__(self):
        for step in self.get_form_list():
            yield self.get_form(step=step)
 
    def get_context_data(self, form, **kwargs):
        context = super(AddDateWizard, self).get_context_data(form=form, **kwargs)
        context.update({'wizard_subclass': self})
        return context

    def get_template_names(self):
        return ["provchanges/adddate.html"]

    def done(self, form_list, form_dict, **kwargs):
        # NOT YET DONE...
        print "DONE!", form_list, form_dict, kwargs

        data = form_list[0].cleaned_data
        data = dict(((k,int(v)) for k,v in data.items()))
        date = datetime.date(**data)
        country = self.country

        url = "/contribute/add/{country}?date={date}".format(country=urlquote(country), date=urlquote(date))
        html = redirect(url)

        return html

class AddEventWizard(SessionWizardView):
    form_list = [   SourceEventForm,
                     TypeEventForm,
                      FromEventForm,
                      ToEventForm,
                      ]

    # NOTE: MUST BE EITHER EXPANSION OR SPLIT OR NEWINFO EVENT, WITH GET PARAMS FOR ALL CONSTANT EVENTINFO
    condition_dict = {"0": lambda wiz: True,
                      "1": lambda wiz: True,
                      "2": lambda wiz: wiz.get_cleaned_data_for_step("1")["type"] in ("Split","NewInfo") if wiz.get_cleaned_data_for_step("1") else False,
                      "3": lambda wiz: wiz.get_cleaned_data_for_step("1")["type"] in ("Merge","Transfer","Begin") if wiz.get_cleaned_data_for_step("1") else False,
                      }

    country = None

    def __iter__(self):
        for step in self.get_form_list():
            yield self.get_form(step=step)

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step in "23": # from or to form
            typ = self.get_cleaned_data_for_step("1").get("type")
            if typ == "Split":
                kwargs["step_descr"] = "Please identify the province that split?"
            elif typ == "NewInfo":
                kwargs["step_descr"] = "Please identify the province that changed information? Only the parts that have changed will be registered. "
            elif typ == "Transfer":
                kwargs["step_descr"] = "Please identify the province that gained territory after all the transfers?"
            elif typ == "Merge":
                kwargs["step_descr"] = "Please identify the province that gained territory after all the mergers?"
            elif typ == "Begin":
                kwargs["step_descr"] = "Please identify the province for which this is the earliest known record?"

        return kwargs

    def get_form_initial(self, step=None):
        data = dict()
        if step == "0":
            data["fromcountry"] = self.country
        elif step == "2":
            data["fromcountry"] = self.country
        elif step == "3":
            data["tocountry"] = self.country
        return data

    def get_context_data(self, form, **kwargs):
        context = super(AddEventWizard, self).get_context_data(form=form, **kwargs)
        context.update({'wizard_subclass': self})
        return context

    def get_template_names(self):
        return ["provchanges/addevent.html"]

    def done(self, form_list, form_dict, **kwargs):
        # NOT YET DONE...
        print "DONE!", form_list, form_dict, kwargs
        
        data = dict(((k,v) for form in form_list for k,v in form.cleaned_data.items()))
        data["date"] = self.request.GET["date"]
        print "DATA",data
        country = self.country
        
        if data["type"] == "Merge":
            prov = data["toname"]
        elif data["type"] == "Split":
            prov = data["fromname"]
        elif data["type"] == "Transfer":
            prov = data["toname"]
        elif data["type"] == "NewInfo":
            prov = data["fromname"]
        elif data["type"] == "Begin":
            prov = data["toname"]
        # if transfer, have to set the 3 geom vals and save to session
        # then, in addtransferchange, get the 3 geom vals from session, and set to the submit data
        # ...
            
        keys = data.keys() #["date","source","type"]
        params = urlencode( [(key,data[key]) for key in keys] ) #+ [("fromcountry",country),("tocountry",country)] )
        print params
        url = "/contribute/view/{country}/{prov}?".format(country=urlquote(country), prov=urlquote(prov)) + params
        html = redirect(url)

        return html





























# Change forms

class MetaChangeForm(forms.ModelForm):

    icon = "https://cdn4.iconfinder.com/data/icons/gray-user-management/512/rounded-512.png"

    class Meta:
        model = ProvChange
        fields = ['user','added','status']

##class SourceForm(forms.ModelForm):
##
##    step_title = "Source"
##    step_descr = """
##                    Find a documented third-party sources to base your submission on.
##                    <a href="http://www.statoids.com">The Statoids website</a> traces historical province changes
##                    in great detail, and should be the first place to look. Go to the primary divisions page for a country of
##                    choice and insert the url into the field below.
##                   """
##
##    class Meta:
##        model = ProvChange
##        fields = ['source']

from django.forms.widgets import RadioFieldRenderer

TYPEINFO = {"NewInfo": {"label": "NewInfo",
                         "short": "A change was made to a province's name, codes, or capital.",
                          "descr": """
                                    Most province changes are as simple as changes in their basic information. In addition, provinces splitting up, 
                                    merging together, or experiencing other major territorial changes are often accompanied by changes
                                    to their name and codes as well. 
                                    """,
                          "img": '<img style="width:100px" src="/static/webnewinfo.png"/>',
                          },
              "PartTransfer": {"label": "PartTransfer",
                               "short": "Part of a province's territory was transferred to another province.",
                              "descr": """
                                        The transferred territory can be
                                        given to an existing province or serve as part of the foundation for an entirely new province.
                                        (Requires a map showing the province outline prior to the transfer of territory)
                                        """,
                              "img": '<img style="width:100px" src="/static/webtransfer.png"/>',
                              },
             "FullTransfer": {"label": "FullTransfer",
                              "short": "An entire province ceased to exist and became part of another province.",
                              "descr": """
                                        For instance, if multiple existing provinces merged together
                                        you would register multiple 'fulltransfer' changes. The transferred territory can be
                                        given to an existing province or serve as part of the foundation for an entirely new province.
                                        (Requires a map showing the now defunct province) 
                                        """,
                              "img": '<img style="width:100px" src="/static/webmerge.png"/>',
                              },
              "Breakaway": {"label": "Breakaway",
                            "short": "A new province was created by breaking away from an existing province.",
                              "descr": """
                                        For instance, if a province split into multiple new provinces
                                        you would register multiple 'breakaway' changes, one for each.
                                        """,
                              "img": '<img style="width:100px" src="/static/websplit.png"/>',
                              },
             "Begin": {"label": "Begin",
                              "short": "Marks the earliest known record for this province.",
                              "descr": """
                                        Typically used for entire country to say more information is needed
                                        beyond this point. 
                                        """,
                              "img": '<img style="width:100px" src="/static/webbegin.png"/>',
                              },
               }

class TypeChangeRenderer(RadioFieldRenderer):

    def render(self):
        choices = [(w,TYPEINFO[w.choice_label]) for w in self if "-" not in w.choice_label]
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

class MergeTypeChangeRenderer(RadioFieldRenderer):

    def render(self):
        choices = [(w,TYPEINFO[w.choice_label]) for w in self if w.choice_label == "FullTransfer"]
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

class TransferTypeChangeRenderer(RadioFieldRenderer):

    def render(self):
        choices = [(w,TYPEINFO[w.choice_label]) for w in self if w.choice_label == "PartTransfer"]
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

class SplitTypeChangeRenderer(RadioFieldRenderer):

    def render(self):
        choices = [(w,TYPEINFO[w.choice_label]) for w in self if w.choice_label in ["Breakaway"]]
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

    icon = "https://cdn1.iconfinder.com/data/icons/ui-glynh-04-of-5/100/UI_Glyph_07-07-512.png"
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=TypeChangeRenderer) }
        

class MergeTypeChangeForm(forms.ModelForm):
    icon = "https://cdn1.iconfinder.com/data/icons/ui-glynh-04-of-5/100/UI_Glyph_07-07-512.png"
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=MergeTypeChangeRenderer) }

class TransferTypeChangeForm(forms.ModelForm):
    icon = "https://cdn1.iconfinder.com/data/icons/ui-glynh-04-of-5/100/UI_Glyph_07-07-512.png"
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=TransferTypeChangeRenderer) }

class SplitTypeChangeForm(forms.ModelForm):
    icon = "https://cdn1.iconfinder.com/data/icons/ui-glynh-04-of-5/100/UI_Glyph_07-07-512.png"
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=SplitTypeChangeRenderer) }

class GeneralChangeForm(SourceEventForm):

    # USED TO SHOW INDIVIDUAL CHANGES
    # THE DESCRIPTIONS DONT ACTUALLY SHOW, SO SHOULD BE REMOVED
    # ...

    icon = "https://cdn0.iconfinder.com/data/icons/huge-black-icons/512/Info.png"
    step_title = "Basic Information"
    step_descr = """
                    Welcome to the step-by-step wizard for submitting historical
                    changes to the "primary" or "level-1" sub-administrative units of countries.
                    For what country and at what date did the province change? 
                    <br><br>

                    <div style="background-color:rgb(248,234,150); outline: black solid thick; font-family: comic sans ms">
                    <p style="font-size:large; font-weight:bold">Note:</p>
                    <p style="font-size:medium; font-style:italic">
                    There are several types of sources you can use:
                    <ul>
                        <li>
                        <a target="_blank" href="http://www.statoids.com">The Statoids website</a> traces historical province changes
                        in great detail, and should be the first place to look.
                        </li>

                        <li>
                        The <a target="_blank" href="https://en.wikipedia.org/wiki/Table_of_administrative_divisions_by_country">Wikipedia entries for administrative units</a>
                        can sometimes also be a useful reference.
                        </li>

                        <li>
                        You can also use offline sources such as a book or an article.
                        </li>
                    </ul>
                    </p>
                    </div>

                    <div style="background-color:rgb(248,234,150); outline: black solid thick; font-family: comic sans ms">
                    <p style="font-size:large; font-weight:bold">Note:</p>
                    <p style="font-size:medium; font-style:italic">
                    It can be a good idea to start by looking at
                    <a target="_blank" href="/contribute">this list of countries and changes already submitted by other users</a>
                    to avoid double-registering. 
                    </p>
                    </div>
                   """

    class Meta:
        model = ProvChange
        fields = ['date', 'source', 'sources', 'mapsources']
        widgets = {"date": CustomDateWidget()}

    def as_p(self):
        html = """
                    <div style="margin-left:2%">

                        <p>
                        {{ form.date.label_tag }}
                        {{ form.date }}
                        </p>

                        <div style="">
                        {{ form.source.label_tag }}
                        {{ form.source }}
                        </div>

                        <p>
					<div style="margin-left:20px; width:45%; display:inline-block"><em>Suggested Sources:</em>
                                            <table style="margin-left:20px">
                                            {% for id,lab in form.suggested_sources %}
                                                <tr>
                                                <td style="width:60px; vertical-align:top"><img height="20px" src="http://www.pvhc.net/img28/hgicvxtrvbwmfpuozczo.png"><div style="display:inline-block; vertical-align:top">{{ id }}</div></td>
                                                <td style="padding-left:5px; vertical-align:top"><a target="_blank" href="/viewsource/{{ id }}/">{{ lab }}</a></td>
                                                </tr>
                                            {% endfor %}
                                            </table>
					</div>
					<div style="width:45%; display:inline-block"><em>Suggested Maps:</em>
                                            <table style="margin-left:20px">
                                            {% for id,lab in form.suggested_mapsources %}
                                                <tr>
                                                <td style="width:60px; vertical-align:top"><img height="20px" src="http://icons.iconarchive.com/icons/icons8/android/512/Maps-Map-Marker-icon.png"><div style="display:inline-block; vertical-align:top">{{ id }}</div></td>
                                                <td style="padding-left:5px; vertical-align:top"><a target="_blank" href="/viewsource/{{ id }}/">{{ lab }}</a></td>
                                                </tr>
                                            {% endfor %}
                                            </table>
					</div>
			</p>
					
                    </div>
                    """
        
        rendered = Template(html).render(Context({"form":self, 'country':urlquote(self.country)}))
        return rendered

    def get_source_formatted(self):
        import re
        val = self['source'].value()
        
        def repl(matchobj):
            id = matchobj.group(2)
            return '<a target="_blank" href="/viewmap/{id}/"><img height="15px" src="http://icons.iconarchive.com/icons/icons8/android/512/Maps-Map-Marker-icon.png">{id}</a>'.format(id=id)
        val,n = re.subn('#(map)([1-9]*)', repl, val)
        def repl(matchobj):
            id = matchobj.group(2)
            return '<a target="_blank" href="/viewsource/{id}/"><img height="15px" src="http://www.pvhc.net/img28/hgicvxtrvbwmfpuozczo.png">{id}</a>'.format(id=id)
        val,n = re.subn('#(source)([1-9]*)', repl, val)
        return val

class FromChangeForm(forms.ModelForm):

    icon = "/static/fromicon.png"
    step_title = "From Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'fromcountry fromname fromalterns fromiso fromfips fromhasc fromcapitalname fromcapital fromtype'.split()

    def __init__(self, *args, **kwargs):
        self.step_descr = kwargs.pop("step_descr", "")
        super(FromChangeForm, self).__init__(*args, **kwargs)
        countrylist = set((r.fromcountry for r in ProvChange.objects.distinct("fromcountry"))) | set((r.tocountry for r in ProvChange.objects.distinct("tocountry")))
        countrylist.update((c[0] for c in countries))
        countrylist = sorted(countrylist)
        self.fields["fromcountry"].widget = ListTextWidget(data_list=countrylist, name="fromcountrylist")

        if "initial" in kwargs:
            country = kwargs["initial"]["fromcountry"]
            provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
            provlist = set((r.fromname for r in provs.distinct("fromname"))) | set((r.toname for r in provs.distinct("toname")))
            provlist = sorted(provlist)
            self.fields["fromname"].widget = ListTextWidget(data_list=provlist, name="fromprovlist")

class ToChangeForm(forms.ModelForm):

    icon = "/static/toicon.png"
    step_title = "To Province"
    step_descr = ""

    class Meta:
        model = ProvChange
        fields = 'tocountry toname toalterns toiso tofips tohasc tocapitalname tocapital totype'.split()

    def __init__(self, *args, **kwargs):
        self.step_descr = kwargs.pop("step_descr", "")
        super(ToChangeForm, self).__init__(*args, **kwargs)
        countrylist = set((r.fromcountry for r in ProvChange.objects.distinct("fromcountry"))) | set((r.tocountry for r in ProvChange.objects.distinct("tocountry")))
        countrylist.update((c[0] for c in countries))
        countrylist = sorted(countrylist)
        self.fields["tocountry"].widget = ListTextWidget(data_list=countrylist, name="tocountrylist")

        if "initial" in kwargs:
            country = kwargs["initial"]["tocountry"]
            provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
            provlist = set((r.fromname for r in provs.distinct("fromname"))) | set((r.toname for r in provs.distinct("toname")))
            provlist = sorted(provlist)
            self.fields["toname"].widget = ListTextWidget(data_list=provlist, name="toprovlist")





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

    #class Media:
        #extend = False
        #js = ("OpenLayers.js",)
    
    def render(self, name, value, attrs=None):
        #print self.Media.js, self.Media.
        output = super(CustomOLWidget, self).render(name, value, attrs=attrs)
        output += """
<script>
var jsmap = %s;
var selectedFeature;
var selectControl;

function syncwms() {
    var wmsurl = document.getElementById('id_transfer_source').value;
    if (wmsurl.trim() != "") {
        var wmsurl = wmsurl.split("?")[0] + "?service=wms&format=image/png"; // trim away junk wms params and ensure uses transparency
        
        var layerlist = jsmap.map.getLayersByName('Historical Map');
        
        if (layerlist.length >= 1) 
            {
            // replace existing
            jsmap.map.removeLayer(layerlist[0]);
            };
            
        customwms = new OpenLayers.Layer.WMS("Historical Map", wmsurl, {layers: 'basic'} );
        customwms.isBaseLayer = false;
        jsmap.map.addLayer(customwms);
        jsmap.map.setLayerIndex(customwms, 1);

        // zoom to country bbox somehow
        //jsmap.map.zoomToExtent(customwms.getDataExtent());
    };
};

function setExistingClipFeatures(geoj) {
    var geojson_format = new OpenLayers.Format.GeoJSON();
    var features = geojson_format.read(geoj, "FeatureCollection");
    
    //vectors.addFeatures requires an array, thus
    if(features.constructor != Array) {
        features = [features];
    }
    existingClipLayer = jsmap.map.getLayersByName('Existing Clip Polygons')[0];
    existingClipLayer.addFeatures(features);
};

function onPopupClose(evt) {
    selectControl.unselect(selectedFeature);
};

function onFeatureSelect(feature) {
    selectedFeature = feature;
    popup = new OpenLayers.Popup.FramedCloud("featinfo", 
                             feature.geometry.getBounds().getCenterLonLat(),
                             null,
                             "<div style='font-size:.8em'>Feature: " + feature.id +"<br>Area: " + feature.geometry.getArea()+"</div>",
                             null, true, onPopupClose);
    feature.popup = popup;
    jsmap.map.addPopup(popup);
    return true;
};

function onFeatureUnselect(feature) {
    jsmap.map.removePopup(feature.popup);
    feature.popup.destroy();
    feature.popup = null;
};

function setupmap() {
    // layer switcher
    jsmap.map.addControl(new OpenLayers.Control.LayerSwitcher({'div':OpenLayers.Util.getElement('layerswitcher')}));
    jsmap.map.addControl(new OpenLayers.Control.MousePosition());

    // wms
    syncwms();

    // existing clips
    var existingClipLayer = new OpenLayers.Layer.Vector("Existing Clip Polygons", {style:{fillColor:"gray", fillOpacity:0.3}});
    jsmap.map.addLayers([existingClipLayer]);

    // enable popup for clips (currently only works if disabling the transfer_geom layer)
    //selectControl = new OpenLayers.Control.SelectFeature(existingClipLayer, {onSelect: onFeatureSelect, onUnselect: onFeatureUnselect});
    //jsmap.map.addControl(selectControl);
    //selectControl.activate();
};

setupmap();

</script>
""" % self.attrs["jsmapname"]
        
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


##class HistoMapForm(forms.ModelForm):
##
##    step_title = "Historical Map"
##    step_descr = """
##                    Find a historical map from before the change. 
##                   """
##
##    class Meta:
##        model = ProvChange
##        fields = ["transfer_reference"]
##        widgets = {"transfer_reference": forms.Textarea(attrs=dict(cols=90,rows=5)) }
##
##    def as_p(self):
##        html = """
##                        The map should show the giving province as it was prior to the change.
##                        Here are some useful places to start:
##
##                        <ul>
##                            <li><a href="http://mapwarper.net/">MapWarper</a></li>
##                            <li><a href="http://www.oldmapsonline.org/">OldMapsOnline</a></li>
##                            <li><a href="https://www.loc.gov/maps/?q=administrative%20divisions">The Library of Congress Map Collection</a></li>
##                            <li><a href="https://www.lib.utexas.edu/maps/historical/index.html">The Perry-Castaneda Library Map Collection</a></li>
##                            <li><a href="http://alabamamaps.ua.edu/historicalmaps/">Alabama Maps Historical Maps</a></li>
##                            <li><a href="http://www.zum.de/whkmla/region/indexa.html">World History at KMLA</a></li>
##                            <li><a href="http://www.antiquemapsandprints.com/prints-and-maps-by-country-12-c.asp">Antique Maps and Prints</a></li>
##                            <li><a href="http://catalogue.defap-bibliotheque.fr/index.php?lvl=index">La bibliotheque du Defap</a></li>
##                        </ul>
##
##                        In the field below identify and reference the source, author, and year of the
##                        map in as much detail as possible.
##
##                        <div style="padding:20px"><b>Map Reference: </b>{{ form.transfer_reference }}</div>
##
##                            <div style="background-color:rgb(248,234,150); outline: black solid thick; font-family: comic sans ms">
##                            <p style="font-size:large; font-weight:bold">Note:</p>
##                            <p style="font-size:medium; font-style:italic">
##                            Note: In accordance with the open-source
##                            nature of the Pshapes project, the map source must be free to share and use without any license restrictions.
##                            Submissions that are based on copyrighted map sources will not be used in the final data. 
##                            </p>
##                            </div>
##                """
##        rendered = Template(html).render(Context({"form":self}))
##        return rendered
##
##
##class GeorefForm(forms.ModelForm):
##
##    step_title = "Georeference"
##    step_descr = """
##                    Georeference the historical map image. 
##                   """
##
##    class Meta:
##        model = ProvChange
##        fields = ["transfer_source"]
##        widgets = {"transfer_source": forms.TextInput(attrs={'size': 90}) }
##
##    def clean(self):
##        data = super(GeorefForm, self).clean()
##        if data:
##            if "mapwarper.net" in data['transfer_source']:
##                pass
##            else:
##                mapwarpid = data['transfer_source']
##                data['transfer_source'] = "http://mapwarper.net/maps/wms/%s" % mapwarpid
##        return data
##        
##    def as_p(self):
##        html = """
##                        Georeferencing is as easy as matching a handful of control points on your historical map image with the equivalent
##                        locations on a real-world map.
##                        For this you must <a href="http://mapwarper.net/">create an account or login to the MapWarper project website</a>.
##
##                        <br><br>
##                        <iframe width="100%" height="300px" src="http://mapwarper.net/"></iframe>
##                        <br>
##
##                        Once finished with georeferencing, simply insert the MapWarper ID of your georeferenced map
##                        (a short number near the top of the MapWarper page)
##                        into the field below. 
##
##                        <div style="padding:20px"><b>MapWarper Map ID: </b>{{ form.transfer_source }}</div>
##                """
##        rendered = Template(html).render(Context({"form":self}))
##        return rendered

geoinstruct = """
                <ol>
                    <li>
                    Guided by the map, draw a clipping polygon that <em>encircles</em> the province that gave away territory.
                    <br>
                    That is, do not follow the borders exactly, but rather draw with a significant error-margin around the province boundaries.
                    <br>
                    This makes it easier to draw and will avoid common topological and integration problems in border dataset,
                    since there are bound to be minor inaccuracies in the historical maps and their georeferencing. 
                    <br><br>
                    </li>
                    <li>
                    Only if the giving province shares a border with the
                    receiving province or any other giving provinces, should you follow those parts of the border exactly.
                    (To avoid gaps between the clipping polygon and any previously drawn giving provinces, shown in gray, 
                    just make sure they overlap.)
                    <br><br>
                    </li>
                    <li>
                    If the giving province only gave away parts of its territory
                    it's sufficient to just draw around the area that was transferred (e.g. a tiny corner of the province
                    or a series of islands).
                    <br><br>
                    </li>
                    <li>
                    Draw multiple polygons if necessary.
                    <br><br>
                    </li>
                </ol>
                
            </b>
            """

class GeoChangeForm(forms.ModelForm):

    icon = "https://cdn4.iconfinder.com/data/icons/eldorado-education/40/291382-geography_globe-512.png"
    step_title = "Territory"
    step_descr = """
                    What did the giving province look like before giving away territory?
                   """

    class Meta:
        model = ProvChange
        fields = ["transfer_reference", "transfer_source", "transfer_map", "transfer_geom"]
        widgets = {"transfer_geom": CustomOLWidget(attrs={"id":"geodjango_transfer_geom"}),
                    "transfer_source": ListTextWidget([], name="sources", attrs={'size': 90, "id":"id_transfer_source"}),
                    "transfer_reference": ListTextWidget([], name="references", attrs={'size': 90, "id":"id_transfer_reference"}),
                   }
        
    def __init__(self, *args, **kwargs):
        self.inst = kwargs.get("instance")
        print "INST",self.inst
        self.country = kwargs.pop("country")
        self.province = kwargs.pop("province")
        self.date = kwargs.pop("date")
        print "kwargs",kwargs
        super(GeoChangeForm, self).__init__(*args, **kwargs)
        print 999, self.fields["transfer_geom"].widget

        # find other relates provs
        country = self.country
        province = self.province
        date = self.date
        otherfeats = ProvChange.objects.filter(fromcountry=country, toname=province, date=date).exclude(status="NonActive") | ProvChange.objects.filter(tocountry=country, toname=province, date=date).exclude(status="NonActive")
        if self.inst:
            otherfeats = otherfeats.exclude(pk=self.inst.pk)
        otherfeats = self.otherfeats = [f for f in otherfeats if f.transfer_geom] # only those with geoms

        print kwargs
        if "initial" in kwargs:
            country = kwargs["initial"]["country"]
            provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
            sources = sorted((r.transfer_source for r in provs.distinct("transfer_source")))
            references = sorted((r.transfer_reference for r in provs.distinct("transfer_reference")))
            self.fields['transfer_source'].widget._list = sources
            self.fields['transfer_reference'].widget._list = references

        maps = get_country_maps(country)
        choices = [(m.pk, "{yr} - {title}".format(yr=m.year, title=m.title.encode('utf8'))) for m in maps]
        self.fields['transfer_map'].widget = forms.Select(choices=[('','')]+choices, attrs=dict(style='width:70%'))

        # make wms auto add/update on sourceurl input
        #self.fields['transfer_geom'].widget = EditableLayerField().widget
        print 888,kwargs
        jsmapname = "geodjango_transfer_geom" if kwargs.get("instance") else "geodjango_3_transfer_geom"
        self.fields['transfer_source'].widget.attrs.update({
##            "onload": "setupmap();",
##            'oninput': "".join(["alert(OpenLayers.objectName);","var wmsurl = document.getElementById('id_transfer_source').value;",
##                                "alert(wmsurl);",
##                                """var customwms = new OpenLayers.Layer.WMS("Custom WMS", wmsurl, {layers: 'basic'} );""",
##                                #"""customwms.isBaseLayer = false;""",
##                                "alert(customwms.objectName);",
##                                """geodjango_transfer_geom.map.addLayer(customwms);""",
##                                ])
            "oninput": "syncwms();",
            })
        self.fields["transfer_geom"].widget.attrs["jsmapname"] = jsmapname
        
    def as_p(self):
        html = """
                        Before you begin:
                        <br><br>
                        To define the territory that changed you need a historical map that shows the giving province as it was prior to the change.
                        If you have not already done so, go ahead and <a href="/addmap/?country={{ country }}">register the map for this country now.</a> 

                        <h4>OLD (to be phased out)!</h4>
                        <div style="padding:20px">WMS Map Link: {{ form.transfer_source }}</div>

                        <div style="padding:20px">Map Description: {{ form.transfer_reference }}</div>

                        <h4>NEW!</h4>
                        <div style="padding:20px">Map Overlay: {{ form.transfer_map }}</div>

                        <br>

                        <div>{{ form.transfer_geom }}</div>

                        <div style="clear:both">
                        <br>
                        Instructions:
                        <br>
                        {{ geoinstruct | safe }}

                        </div>
                        
                    """
        # add features
        import json
        geoj = {"type":"FeatureCollection",
                "features": [dict(type="Feature", properties=dict(fromname=f.fromname), geometry=json.loads(f.transfer_geom.json))
                             for f in self.otherfeats]}
        geoj_str = json.dumps(geoj).replace("'", "\\'") # if the any property names include a single apo, escape it so doesnt cancel the string quotes
        print geoj_str
        html += """<script>
                setExistingClipFeatures('{geoj}')
                </script>
                """.format(geoj=geoj_str)
        
        rendered = Template(html).render(Context({"form":self, 'geoinstruct':geoinstruct, 'country':urlquote(self.country)}))
        return rendered

    def as_simple(self):
        html = """
                        <p>OLD (to be phased out)!</p>
                        <div style="padding:20px">WMS Map Link: {{ form.transfer_source }}</div>
                        <div style="padding:20px">Map Description: {{ form.transfer_reference }}</div>

                        <p>NEW!</p>
                        <div style="padding:20px">Map Overlay: {{ form.transfer_map }}</div>

                        <br>

                        <div>{{ form.transfer_geom }}</div>

                        <div style="clear:both">
                        <br>
                        Instructions:
                        <br>
                        {{ geoinstruct | safe }}
                        
                        </div>
                        
                    """
        # add features
        import json
        geoj = {"type":"FeatureCollection",
                "features": [dict(type="Feature", properties=dict(fromname=f.fromname), geometry=json.loads(f.transfer_geom.json))
                             for f in self.otherfeats]}
        geoj_str = json.dumps(geoj).replace("'", "\\'") # if the any property names include a single apo, escape it so doesnt cancel the string quotes
        print geoj_str
        html += """<script>
                setExistingClipFeatures('{geoj}')
                </script>
                """.format(geoj=geoj_str)
        
        rendered = Template(html).render(Context({"form":self, 'geoinstruct':geoinstruct}))
        return rendered

    def clean(self):
        cleaned_data = super(GeoChangeForm, self).clean()
        if cleaned_data and cleaned_data.get('transfer_map'):
            cleaned_data['transfer_map'] = get_object_or_404(Map, pk=int(cleaned_data['transfer_map'].pk))
        if cleaned_data and self.otherfeats:
            othergeoms = reduce(lambda res,val: res.union(val), (f.transfer_geom for f in self.otherfeats))
            diff = cleaned_data["transfer_geom"].difference(othergeoms)
            if diff.geom_type != "MultiPolygon":
                from django.contrib.gis.geos import MultiPolygon
                diff = MultiPolygon(diff)
            cleaned_data["transfer_geom"] = diff
        return cleaned_data





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


























##class SubmitChangeWizard(SessionWizardView):
##    form_list = [   GeneralChangeForm,
##                     TypeChangeForm,
##                      FromChangeForm,
##                     HistoMapForm,
##                     GeorefForm,
##                      GeoChangeForm,
##                      ToChangeForm,
##                      ]
##    def _geomode(wiz):
##        typeformdata = wiz.get_cleaned_data_for_step("1") or {"type":"NewInfo"}
##        return "Transfer" in typeformdata["type"]
##    
##    condition_dict = {"3": _geomode,
##                      "4": _geomode,
##                      "5": _geomode,}
##        
####    def __init__(self, *args, **kwargs):
####        self.form_list = [TypeChangeForm,
####                      GeneralChangeForm,
####                      FromChangeForm,
####                      GeoChangeForm,
####                      ToChangeForm,
####                      ]
####        SessionWizardView.__init__(self, *args, **kwargs)
##
####    def get_form_list(self):
####        return [SourceForm,
####                     TypeChangeForm,
####                      GeneralChangeForm,
####                      FromChangeForm,
####                     HistoMapForm,
####                     GeorefForm,
####                      GeoChangeForm,
####                      ToChangeForm,
####                      ]
##
##    def __iter__(self):
##        for step in self.get_form_list():
##            yield self.get_form(step=step)
## 
##    def get_context_data(self, form, **kwargs):
##        context = super(SubmitChangeWizard, self).get_context_data(form=form, **kwargs)
##        context.update({'wizard_subclass': self})
##        return context
##
##    def get_form(self, step=None, data=None, files=None):
##        form = super(SubmitChangeWizard, self).get_form(step, data, files)
##        print step,repr(form)
##        if isinstance(form, GeoChangeForm):
##            # ADD CUSTOM WMS
##            typeformdata = self.get_cleaned_data_for_step("1") or {"type":"NewInfo"}
##            if "Transfer" in typeformdata["type"]:
##                wmsdata = self.get_cleaned_data_for_step("4") or {}
##                wms = wmsdata.get("transfer_source")
##                if wms:
##                    wms = wms.split("?")[0]+"?service=wms&format=image/png" # trim away junk wms params and ensure uses transparency
##                    form.fields['transfer_geom'].widget.wms = wms
##        return form
##
####    def get_form(self, step=None, data=None, files=None):
####        # SKIP GEOFORM IF NOT NEEDED
####        form = super(SubmitChangeWizard, self).get_form(step, data, files)
####        print step,repr(form)
####        if isinstance(form, HistoMapForm):
####            typeformdata = self.get_cleaned_data_for_step("1") or {"type":"NewInfo"}
####            if not "Transfer" in typeformdata["type"]:
####                # skip til after geoform
####                self.step = bytes(int(step)+3)
####                form = super(SubmitChangeWizard, self).get_form(self.step, data, files)
####        elif isinstance(form, GeoChangeForm):
####            typeformdata = self.get_cleaned_data_for_step("1") or {"type":"NewInfo"}
####            if "Transfer" in typeformdata["type"]:
####                wmsdata = self.get_cleaned_data_for_step("5") or {}
####                wms = wmsdata.get("transfer_source")
####                if wms:
####                    wms = wms.split("?")[0]+"?service=wms&format=image/png" # trim away junk wms params and ensure uses transparency
####                    form.fields['transfer_geom'].widget.wms = wms
####        return form
##        
##    def get_template_names(self):
##        return ["provchanges/submitchange.html"]
##
##    def done(self, form_list, form_dict, **kwargs):
##        # NOT YET DONE...
##        print "DONE!", form_list, form_dict, kwargs
##        
##        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
##        formfieldvalues = dict(((k,v) for form in form_list for k,v in form.cleaned_data.items() if k in fieldnames))
##        formfieldvalues["user"] = self.request.user.username
##        formfieldvalues["added"] = datetime.date.today()
##        formfieldvalues["bestversion"] = True
##        print formfieldvalues
##
##        obj = ProvChange.objects.create(**formfieldvalues)
##        obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions
##        print obj
##        
##        obj.save()
##        html = redirect("/provchange/%s/view/" % obj.pk)
##
##        return html

class AddChangeWizard(SessionWizardView):

##    form_list = [   GeneralChangeForm,
##                     TypeChangeForm,
##                      FromChangeForm,
##                    ToChangeForm,
##                     HistoMapForm,
##                     GeorefForm,
##                      GeoChangeForm,
##                      ]
##    
##    def _geomode(wiz):
##        typeformdata = wiz.get_cleaned_data_for_step("1") or {"type":"NewInfo"}
##        print wiz.get_cleaned_data_for_step("1")
##        return "Transfer" in typeformdata["type"]
##    
##    condition_dict = {"0": lambda wiz: False,
##                      "1": lambda wiz: True,
##                      "2": lambda wiz: wiz.request.GET["type"].lower() == "expansion",
##                      "3": lambda wiz: wiz.request.GET["type"].lower() == "split",
##                      "4": _geomode,
##                      "5": _geomode,
##                      "6": _geomode,}
##
##    country = None
##    province = None

    def __iter__(self):
        for step in self.get_form_list():
            yield self.get_form(step=step)
 
    def get_context_data(self, form, **kwargs):
        context = super(AddChangeWizard, self).get_context_data(form=form, **kwargs)
        context.update({'wizard_subclass': self})
        return context

##    def get_form(self, step=None, data=None, files=None):
##        print "HELLOOOO", self.request.GET, repr(self.request.GET["type"].lower())
##        data = data or {}
##        print data
##        data = dict([(key,data.getlist(key)[0] if isinstance(data.getlist(key),list) else data.getlist(key)) for key in data.keys()])
##        print data
##        typ = self.request.GET["type"].lower().strip('"')
##        
##        if typ == "expansion":
##            for k,v in [("0-country","country"),
##                        ("0-date","date"),
##                        ("0-source","source"),
##                        ("3-toname","toname")
##                        ]:
##                if k not in data:
##                    data[k] = self.request.GET[v]
##            print "DATA",data
##
##        elif typ == "split":
##            for k,v in [("0-country","country"),
##                        ("0-date","date"),
##                        ("0-source","source"),
##                        ("2-fromname","fromname")
##                        ]:
##                if k not in data:
##                    data[k] = self.request.GET[v]
##            print "DATA",data
##        
##        if step == "1":
##            # NOT WOORKING !!!!
##            print 77777,repr(typ),typ=="split"
##            form = super(AddChangeWizard, self).get_form(step, data=data, files=files)  
##            if typ == "expansion":
##                form._meta.widgets = {"type": forms.RadioSelect(renderer=ExpansionTypeChangeRenderer) }
##                #form = ExpansionTypeChangeForm(data=data, files=files)
##            elif typ == "split":
##                form._meta.widgets = {"type": forms.RadioSelect(renderer=SplitTypeChangeRenderer) }
##                #form = SplitTypeChangeForm(data=data, files=files)
##            else:
##                fsfdsfdsfdsf
##        else:
##            form = super(AddChangeWizard, self).get_form(step, data=data, files=files)        
##        print step,repr(form)
##        print "FORMDATA",form.data
##        
##        if isinstance(form, GeoChangeForm):
##            # ADD CUSTOM WMS
##            typeformdata = self.get_cleaned_data_for_step("1") or {"type":"NewInfo"}
##            if "Transfer" in typeformdata["type"]:
##                wmsdata = self.get_cleaned_data_for_step("4") or {}
##                wms = wmsdata.get("transfer_source")
##                if wms:
##                    wms = wms.split("?")[0]+"?service=wms&format=image/png" # trim away junk wms params and ensure uses transparency
##                    form.fields['transfer_geom'].widget.wms = wms
##        return form

##    def get_form_instance(self, step):
##        params = dict([(k,v) for k,v in self.request.GET.items()])
##        # THIS IS WHERE I AMMMMM
##        print "INST PARAMS",params
##        inst = ProvChange(**params)
##        return inst

    def get_template_names(self):
        return ["provchanges/addchange.html"]

    def done(self, form_list, form_dict, **kwargs):
        # NOT YET DONE...
        print "DONE!", form_list, form_dict, kwargs
        
        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
        formfieldvalues = dict(((k,v) for form in form_list for k,v in form.cleaned_data.items() if k in fieldnames))
        formfieldvalues["user"] = self.request.user.username
        formfieldvalues["added"] = datetime.datetime.now()
        formfieldvalues["bestversion"] = True
        print formfieldvalues

        eventvalues = dict(((k,v) for k,v in self.request.GET.items()))
        print eventvalues

        if eventvalues["type"].strip('"') == "Merge" and formfieldvalues["type"].strip('"') == "NewInfo":
            # all tos become froms when newinfo for merge event
            # ACTUALLY: shouldnt happen anymore
            raise Exception()
            #trans = dict([(k.replace("to","from"),v) for k,v in eventvalues.items() if k.startswith("to")])
            #eventvalues = dict([(k,v) for k,v in eventvalues.items() if not k.startswith("to")])
            #eventvalues.update(trans)

        objvalues = dict(eventvalues)
        objvalues.update(formfieldvalues)
        sources = [get_object_or_404(Source, pk=int(pk)) for pk in objvalues.pop('sources').split(',') if pk]
        mapsources = [get_object_or_404(Map, pk=int(pk)) for pk in objvalues.pop('mapsources').split(',') if pk]
        print objvalues
        
        obj = ProvChange.objects.create(**objvalues)
        obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions
        print obj
        
        obj.save()
        for s in sources:
            obj.sources.add(s)
        for m in mapsources:
            obj.mapsources.add(m)
        obj.save()
        
        html = self.done_redirect(obj)

        return html


class AddNewInfoChangeWizard(AddChangeWizard):

    form_list = [   
                    ToChangeForm,
                      ]

    country = None
    province = None
    
##    def get_form(self, step=None, data=None, files=None):
##        print "HELLOOOO", self.request.GET, repr(self.request.GET["type"].lower())
##        if data:
##            print data
##            data = dict([(key,data.getlist(key)[0] if isinstance(data.getlist(key),list) else data.getlist(key)) for key in data.keys()])
##        else:
##            data = {}
##        print data
##
##        form = super(AddNewInfoChangeWizard, self).get_form(step, data=data, files=files)        
##
##        return form

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == "0": # from or to form
            kwargs["step_descr"] = "Fill in the province information after the change. Only the parts that have changed will be registered." 
        return kwargs

    def get_form_initial(self, step=None):
        data = dict()
        if step == "0":
            data["tocountry"] = self.request.GET["fromcountry"]
            data["toname"] = self.request.GET["fromname"]
            data["toalterns"] = self.request.GET["fromalterns"]
            data["toiso"] = self.request.GET["fromiso"]
            data["tofips"] = self.request.GET["fromfips"]
            data["tohasc"] = self.request.GET["fromhasc"]
            data["totype"] = self.request.GET["fromtype"]
            data["tocapital"] = self.request.GET["fromcapital"]
            data["tocapitalname"] = self.request.GET["fromcapitalname"]
        return data  

    def done_redirect(self, obj):
        fields = ["fromcountry","date","source","sources","mapsources","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]
        params = dict([(field,getattr(obj,field)) for field in fields])
        params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
        params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
        params = urlencode(params)
        eventlink = "/contribute/view/{country}/{prov}/?type=NewInfo&".format(country=urlquote(self.country), prov=urlquote(obj.fromname)) + params
        html = redirect(eventlink)
        return html

class AddSplitChangeWizard(AddChangeWizard):

    form_list = [   SplitTypeChangeForm,
                    ToChangeForm,
                      ]

    country = None
    province = None
    
##    def get_form(self, step=None, data=None, files=None):
##        print "HELLOOOO", self.request.GET, repr(self.request.GET["type"].lower())
##        if data:
##            print data
##            data = dict([(key,data.getlist(key)[0] if isinstance(data.getlist(key),list) else data.getlist(key)) for key in data.keys()])
##        else:
##            data = {}
##        print data
##
##        form = super(AddSplitChangeWizard, self).get_form(step, data=data, files=files)        
##
##        return form

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == "1": # from or to form
            kwargs["step_descr"] = "Please identify the province that broke away?"
        return kwargs

    def get_form_initial(self, step=None):
        data = dict()
        if step == "1":
            data["tocountry"] = self.country
        return data  

    def done_redirect(self, obj):
        fields = ["fromcountry","date","source","sources","mapsources","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]
        params = dict([(field,getattr(obj,field)) for field in fields])
        params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
        params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
        params = urlencode(params)
        eventlink = "/contribute/view/{country}/{prov}/?type=Split&".format(country=urlquote(self.country), prov=urlquote(obj.fromname)) + params
        html = redirect(eventlink)
        return html
    
class AddMergeChangeWizard(AddChangeWizard):

    form_list = [   MergeTypeChangeForm,
                    FromChangeForm,
                    ToChangeForm,
##                     HistoMapForm,
##                     GeorefForm,
                      GeoChangeForm,
                      ]
    
    def _geomode(wiz):
        typeformdata = wiz.get_cleaned_data_for_step("0") or {"type":"NewInfo"}
        print wiz.get_cleaned_data_for_step("0")
        return typeformdata["type"] == "FullTransfer"

    condition_dict = {"0": lambda wiz: True,
                      "1": lambda wiz: True,
                      "2": lambda wiz: False,
                      "3": _geomode,}

    country = None
    province = None

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == "1": # from or to form
            kwargs["step_descr"] = "Please identify the province that merged and ceased to exist?"
        elif step == "3":
            kwargs["country"] = self.country
            kwargs["province"] = self.province
            kwargs["date"] = self.request.GET["date"]
        return kwargs

    def get_form_initial(self, step=None):
        data = dict()
        if step == "1":
            data["fromcountry"] = self.country
        elif step == "3":
            data["country"] = self.country
        return data
    
    def done_redirect(self, obj):
        fields = ["tocountry","date","source","sources","mapsources","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]
        params = dict([(field,getattr(obj,field)) for field in fields])
        params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
        params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
        params = urlencode(params)
        eventlink = "/contribute/view/{country}/{prov}/?type=Merge&".format(country=urlquote(self.country), prov=urlquote(obj.toname)) + params
        html = redirect(eventlink)
        return html

    
class AddTransferChangeWizard(AddChangeWizard):

    form_list = [   TransferTypeChangeForm,
                    FromChangeForm,
                    ToChangeForm,
                      GeoChangeForm,
                      ]
    
    def _geomode(wiz):
        typeformdata = wiz.get_cleaned_data_for_step("0") or {"type":"NewInfo"}
        print wiz.get_cleaned_data_for_step("0")
        return typeformdata["type"] == "PartTransfer"

    condition_dict = {"0": lambda wiz: True,
                      "1": lambda wiz: True,
                      "2": lambda wiz: False,
                      "3": _geomode,}

    country = None
    province = None

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == "1": # from or to form
            kwargs["step_descr"] = "Please identify the province that transferred territory?"
        elif step == "3":
            kwargs["country"] = self.country
            kwargs["province"] = self.province
            kwargs["date"] = self.request.GET["date"]
        return kwargs

    def get_form_initial(self, step=None):
        data = dict()
        if step == "1":
            data["fromcountry"] = self.country
        elif step == "3":
            data["country"] = self.country
        return data  
    
    def done_redirect(self, obj):
        fields = ["tocountry","date","source","sources","mapsources","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]
        params = dict([(field,getattr(obj,field)) for field in fields])
        params['sources'] = ','.join([str(s.pk) for s in params['sources'].all()])
        params['mapsources'] = ','.join([str(m.pk) for m in params['mapsources'].all()])
        params = urlencode(params)
        eventlink = "/contribute/view/{country}/{prov}/?type=Transfer&".format(country=urlquote(self.country), prov=urlquote(obj.toname)) + params
        html = redirect(eventlink)
        return html
    
##class SubmitChangeWizard(SessionWizardView):
##    form_list = [   GeneralChangeForm,
##                     TypeChangeForm,
##                      FromChangeForm,
##                    ToChangeForm,
##                     HistoMapForm,
##                     GeorefForm,
##                      GeoChangeForm,
##                      ]
##
##    # NOTE: MUST BE EITHER EXPANSION OR SPLIT OR NEWINFO EVENT, WITH GET PARAMS FOR ALL CONSTANT EVENTINFO
##    
##    def _geomode(wiz):
##        typeformdata = wiz.get_cleaned_data_for_step("1") or {"type":"NewInfo"}
##        print wiz.get_cleaned_data_for_step("1")
##        return "Transfer" in typeformdata["type"]
##    
##    condition_dict = {"0": lambda wiz: False,
##                      "1": lambda wiz: wiz.request.GET["eventtype"] != "newinfo", # for newinfo events, no point in setting type
##                      "2": lambda wiz: wiz.request.GET["eventtype"] in ("expansion","newinfo"),
##                      "3": lambda wiz: wiz.request.GET["eventtype"] in ("split","newinfo"),
##                      "4": _geomode,
##                      "5": _geomode,
##                      "6": _geomode,}
##
##    def __iter__(self):
##        for step in self.get_form_list():
##            yield self.get_form(step=step)
## 
##    def get_context_data(self, form, **kwargs):
##        context = super(SubmitChangeWizard, self).get_context_data(form=form, **kwargs)
##        context.update({'wizard_subclass': self})
##        return context
##
##    def get_form(self, step=None, data=None, files=None):
##        data = data or {}
##        print data
##        data = dict([(key,data.getlist(key)[0] if isinstance(data.getlist(key),list) else data.getlist(key)) for key in data.keys()])
##        print data
##        
##        if self.request.GET["eventtype"] == "expansion":
##            for k,v in [("0-country","country"),
##                        ("0-date","date"),
##                        ("0-source","source"),
##                        ("3-toprov","toprov")
##                        ]:
##                if k not in data:
##                    data[k] = self.request.GET[v]
##            print "DATA",data
##
##        elif self.request.GET["eventtype"] == "split":
##            for k,v in [("0-country","country"),
##                        ("0-date","date"),
##                        ("0-source","source"),
##                        ("2-toprov","fromprov")
##                        ]:
##                if k not in data:
##                    data[k] = self.request.GET[v]
##            print "DATA",data
##        
##        if step == "1":
##            # NOT WOORKING !!!!
##            print 77777,self.request.GET["eventtype"]
##            if self.request.GET["eventtype"] == "expansion":
##                form = ExpansionTypeChangeForm(data=data, files=files)
##            elif self.request.GET["eventtype"] == "split":
##                form = SplitTypeChangeForm(data=data, files=files)
##            else:
##                form = TypeChangeForm(data=data, files=files)
##        else:
##            form = super(SubmitChangeWizard, self).get_form(step, data=data, files=files)        
##        print step,repr(form)
##        print "FORMDATA",form.data
##        
##        if isinstance(form, GeoChangeForm):
##            # ADD CUSTOM WMS
##            typeformdata = self.get_cleaned_data_for_step("1") or {"type":"NewInfo"}
##            if "Transfer" in typeformdata["type"]:
##                wmsdata = self.get_cleaned_data_for_step("4") or {}
##                wms = wmsdata.get("transfer_source")
##                if wms:
##                    wms = wms.split("?")[0]+"?service=wms&format=image/png" # trim away junk wms params and ensure uses transparency
##                    form.fields['transfer_geom'].widget.wms = wms
##        return form
##
##    def get_template_names(self):
##        return ["provchanges/submitchange.html"]
##
##    def done(self, form_list, form_dict, **kwargs):
##        # NOT YET DONE...
##        print "DONE!", form_list, form_dict, kwargs
##        
##        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
##        formfieldvalues = dict(((k,v) for form in form_list for k,v in form.cleaned_data.items() if k in fieldnames))
##        formfieldvalues["user"] = self.request.user.username
##        formfieldvalues["added"] = datetime.date.today()
##        formfieldvalues["bestversion"] = True
##        print formfieldvalues
##
##        obj = ProvChange.objects.create(**formfieldvalues)
##        obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions
##        print obj
##        
##        obj.save()
##        html = redirect("/provchange/%s/view/" % obj.pk)
##
##        return html

##class SubmitExpansionChangeWizard(SessionWizardView):
##    form_list = [   GeneralChangeForm,
##                    FromChangeForm,
##                     HistoMapForm,
##                     GeorefForm,
##                      GeoChangeForm
##                      ]
##    def _geomode(wiz):
##        typeformdata = wiz.get_cleaned_data_for_step("1") or {"type":"NewInfo"}
##        return "Transfer" in typeformdata["type"]
##    
##    condition_dict = {"2": _geomode,
##                      "3": _geomode,
##                      "4": _geomode,}
##    
##    def __iter__(self):
##        for step in self.get_form_list():
##            yield self.get_form(step=step)
## 
##    def get_context_data(self, form, **kwargs):
##        context = super(SubmitExpansionChangeWizard, self).get_context_data(form=form, **kwargs)
##        context.update({'wizard_subclass': self})
##        return context
##
##    def get_form(self, step=None, data=None, files=None):
##        form = super(SubmitChangeWizard, self).get_form(step, data, files)
##        print step,repr(form)
##        if isinstance(form, GeoChangeForm):
##            # ADD CUSTOM WMS
##            typeformdata = self.get_cleaned_data_for_step("0") or {"type":"NewInfo"}
##            if "Transfer" in typeformdata["type"]:
##                wmsdata = self.get_cleaned_data_for_step("3") or {}
##                wms = wmsdata.get("transfer_source")
##                if wms:
##                    wms = wms.split("?")[0]+"?service=wms&format=image/png" # trim away junk wms params and ensure uses transparency
##                    form.fields['transfer_geom'].widget.wms = wms
##        return form
##    
##    def get_template_names(self):
##        return ["provchanges/submitchange.html"]
##
##    def done(self, form_list, form_dict, **kwargs):
##        # NOT YET DONE...
##        print "DONE!", form_list, form_dict, kwargs
##        
##        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
##        formfieldvalues = dict(((k,v) for form in form_list for k,v in form.cleaned_data.items() if k in fieldnames))
##        formfieldvalues["user"] = self.request.user.username
##        formfieldvalues["added"] = datetime.date.today()
##        formfieldvalues["bestversion"] = True
##        print formfieldvalues
##
##        obj = ProvChange.objects.create(**formfieldvalues)
##        obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions
##        print obj
##        
##        obj.save()
##        html = redirect("/provchange/%s/view/" % obj.pk)
##
##        return html
##
##class SubmitSplitChangeWizard(SessionWizardView):
##    form_list = [   GeneralChangeForm,
##                    ToChangeForm,]
##      
##    def __iter__(self):
##        for step in self.get_form_list():
##            yield self.get_form(step=step)
## 
##    def get_context_data(self, form, **kwargs):
##        context = super(SubmitChangeWizard, self).get_context_data(form=form, **kwargs)
##        context.update({'wizard_subclass': self})
##        return context
##
##    def get_form(self, step=None, data=None, files=None):
##        form = super(SubmitSplitChangeWizard, self).get_form(step, data, files)
##        print step,repr(form)
##        if isinstance(form, GeoChangeForm):
##            # ADD CUSTOM WMS
##            typeformdata = self.get_cleaned_data_for_step("0") or {"type":"NewInfo"}
##            if "Transfer" in typeformdata["type"]:
##                wmsdata = self.get_cleaned_data_for_step("3") or {}
##                wms = wmsdata.get("transfer_source")
##                if wms:
##                    wms = wms.split("?")[0]+"?service=wms&format=image/png" # trim away junk wms params and ensure uses transparency
##                    form.fields['transfer_geom'].widget.wms = wms
##        return form
##
##    def get_template_names(self):
##        return ["provchanges/submitchange.html"]
##
##    def done(self, form_list, form_dict, **kwargs):
##        # NOT YET DONE...
##        print "DONE!", form_list, form_dict, kwargs
##        
##        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
##        formfieldvalues = dict(((k,v) for form in form_list for k,v in form.cleaned_data.items() if k in fieldnames))
##        formfieldvalues["user"] = self.request.user.username
##        formfieldvalues["added"] = datetime.date.today()
##        formfieldvalues["bestversion"] = True
##        print formfieldvalues
##
##        obj = ProvChange.objects.create(**formfieldvalues)
##        obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions
##        print obj
##        
##        obj.save()
##        html = redirect("/provchange/%s/view/" % obj.pk)
##
##        return html



