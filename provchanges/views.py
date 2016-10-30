from django.shortcuts import render, get_object_or_404, redirect
from django.template import Template,Context
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import admin

from django.utils.http import urlquote, urlencode

from django.core.paginator import Paginator

from rest_framework import response
from rest_framework.decorators import api_view

from formtools.wizard.views import SessionWizardView

from .models import ProvChange

from django.db.models import Count

import datetime


# Create your views here.

countries = [(u'Afghanistan', u'Afghanistan'), (u'\xc5land Islands', u'\xc5land Islands'), (u'Albania', u'Albania'), (u'Algeria', u'Algeria'), (u'American Samoa', u'American Samoa'), (u'Andorra', u'Andorra'), (u'Angola', u'Angola'), (u'Anguilla', u'Anguilla'), (u'Antigua and Barbuda', u'Antigua and Barbuda'), (u'Argentina', u'Argentina'), (u'Armenia', u'Armenia'), (u'Aruba', u'Aruba'), (u'Australia', u'Australia'), (u'Austria', u'Austria'), (u'Azerbaijan', u'Azerbaijan'), (u'The Bahamas', u'The Bahamas'), (u'Bahrain', u'Bahrain'), (u'Bangladesh', u'Bangladesh'), (u'Barbados', u'Barbados'), (u'Belarus', u'Belarus'), (u'Belgium', u'Belgium'), (u'Belize', u'Belize'), (u'Benin', u'Benin'), (u'Bermuda', u'Bermuda'), (u'Bhutan', u'Bhutan'), (u'Bolivia', u'Bolivia'), (u'Bonaire', u'Bonaire'), (u'Bosnia and Herzegovina', u'Bosnia and Herzegovina'), (u'Botswana', u'Botswana'), (u'Bouvet Island', u'Bouvet Island'), (u'Brazil', u'Brazil'), (u'British Indian Ocean Territory', u'British Indian Ocean Territory'), (u'United States Minor Outlying Islands', u'United States Minor Outlying Islands'), (u'British Virgin Islands', u'British Virgin Islands'), (u'Brunei', u'Brunei'), (u'Bulgaria', u'Bulgaria'), (u'Burkina Faso', u'Burkina Faso'), (u'Burundi', u'Burundi'), (u'Cambodia', u'Cambodia'), (u'Cameroon', u'Cameroon'), (u'Canada', u'Canada'), (u'Cape Verde', u'Cape Verde'), (u'Cayman Islands', u'Cayman Islands'), (u'Central African Republic', u'Central African Republic'), (u'Chad', u'Chad'), (u'Chile', u'Chile'), (u'China', u'China'), (u'Christmas Island', u'Christmas Island'), (u'Cocos (Keeling) Islands', u'Cocos (Keeling) Islands'), (u'Colombia', u'Colombia'), (u'Comoros', u'Comoros'), (u'Republic of the Congo', u'Republic of the Congo'), (u'Democratic Republic of the Congo', u'Democratic Republic of the Congo'), (u'Cook Islands', u'Cook Islands'), (u'Costa Rica', u'Costa Rica'), (u'Croatia', u'Croatia'), (u'Cuba', u'Cuba'), (u'Cura\xe7ao', u'Cura\xe7ao'), (u'Cyprus', u'Cyprus'), (u'Czech Republic', u'Czech Republic'), (u'Denmark', u'Denmark'), (u'Djibouti', u'Djibouti'), (u'Dominica', u'Dominica'), (u'Dominican Republic', u'Dominican Republic'), (u'Ecuador', u'Ecuador'), (u'Egypt', u'Egypt'), (u'El Salvador', u'El Salvador'), (u'Equatorial Guinea', u'Equatorial Guinea'), (u'Eritrea', u'Eritrea'), (u'Estonia', u'Estonia'), (u'Ethiopia', u'Ethiopia'), (u'Falkland Islands', u'Falkland Islands'), (u'Faroe Islands', u'Faroe Islands'), (u'Fiji', u'Fiji'), (u'Finland', u'Finland'), (u'France', u'France'), (u'French Guiana', u'French Guiana'), (u'French Polynesia', u'French Polynesia'), (u'French Southern and Antarctic Lands', u'French Southern and Antarctic Lands'), (u'Gabon', u'Gabon'), (u'The Gambia', u'The Gambia'), (u'Georgia', u'Georgia'), (u'Germany', u'Germany'), (u'Ghana', u'Ghana'), (u'Gibraltar', u'Gibraltar'), (u'Greece', u'Greece'), (u'Greenland', u'Greenland'), (u'Grenada', u'Grenada'), (u'Guadeloupe', u'Guadeloupe'), (u'Guam', u'Guam'), (u'Guatemala', u'Guatemala'), (u'Guernsey', u'Guernsey'), (u'Guinea', u'Guinea'), (u'Guinea-Bissau', u'Guinea-Bissau'), (u'Guyana', u'Guyana'), (u'Haiti', u'Haiti'), (u'Heard Island and McDonald Islands', u'Heard Island and McDonald Islands'), (u'Honduras', u'Honduras'), (u'Hong Kong', u'Hong Kong'), (u'Hungary', u'Hungary'), (u'Iceland', u'Iceland'), (u'India', u'India'), (u'Indonesia', u'Indonesia'), (u'Ivory Coast', u'Ivory Coast'), (u'Iran', u'Iran'), (u'Iraq', u'Iraq'), (u'Republic of Ireland', u'Republic of Ireland'), (u'Isle of Man', u'Isle of Man'), (u'Israel', u'Israel'), (u'Italy', u'Italy'), (u'Jamaica', u'Jamaica'), (u'Japan', u'Japan'), (u'Jersey', u'Jersey'), (u'Jordan', u'Jordan'), (u'Kazakhstan', u'Kazakhstan'), (u'Kenya', u'Kenya'), (u'Kiribati', u'Kiribati'), (u'Kuwait', u'Kuwait'), (u'Kyrgyzstan', u'Kyrgyzstan'), (u'Laos', u'Laos'), (u'Latvia', u'Latvia'), (u'Lebanon', u'Lebanon'), (u'Lesotho', u'Lesotho'), (u'Liberia', u'Liberia'), (u'Libya', u'Libya'), (u'Liechtenstein', u'Liechtenstein'), (u'Lithuania', u'Lithuania'), (u'Luxembourg', u'Luxembourg'), (u'Macau', u'Macau'), (u'Republic of Macedonia', u'Republic of Macedonia'), (u'Madagascar', u'Madagascar'), (u'Malawi', u'Malawi'), (u'Malaysia', u'Malaysia'), (u'Maldives', u'Maldives'), (u'Mali', u'Mali'), (u'Malta', u'Malta'), (u'Marshall Islands', u'Marshall Islands'), (u'Martinique', u'Martinique'), (u'Mauritania', u'Mauritania'), (u'Mauritius', u'Mauritius'), (u'Mayotte', u'Mayotte'), (u'Mexico', u'Mexico'), (u'Federated States of Micronesia', u'Federated States of Micronesia'), (u'Moldova', u'Moldova'), (u'Monaco', u'Monaco'), (u'Mongolia', u'Mongolia'), (u'Montenegro', u'Montenegro'), (u'Montserrat', u'Montserrat'), (u'Morocco', u'Morocco'), (u'Mozambique', u'Mozambique'), (u'Myanmar', u'Myanmar'), (u'Namibia', u'Namibia'), (u'Nauru', u'Nauru'), (u'Nepal', u'Nepal'), (u'Netherlands', u'Netherlands'), (u'New Caledonia', u'New Caledonia'), (u'New Zealand', u'New Zealand'), (u'Nicaragua', u'Nicaragua'), (u'Niger', u'Niger'), (u'Nigeria', u'Nigeria'), (u'Niue', u'Niue'), (u'Norfolk Island', u'Norfolk Island'), (u'North Korea', u'North Korea'), (u'Northern Mariana Islands', u'Northern Mariana Islands'), (u'Norway', u'Norway'), (u'Oman', u'Oman'), (u'Pakistan', u'Pakistan'), (u'Palau', u'Palau'), (u'Palestine', u'Palestine'), (u'Panama', u'Panama'), (u'Papua New Guinea', u'Papua New Guinea'), (u'Paraguay', u'Paraguay'), (u'Peru', u'Peru'), (u'Philippines', u'Philippines'), (u'Pitcairn Islands', u'Pitcairn Islands'), (u'Poland', u'Poland'), (u'Portugal', u'Portugal'), (u'Puerto Rico', u'Puerto Rico'), (u'Qatar', u'Qatar'), (u'Republic of Kosovo', u'Republic of Kosovo'), (u'R\xe9union', u'R\xe9union'), (u'Romania', u'Romania'), (u'Russia', u'Russia'), (u'Rwanda', u'Rwanda'), (u'Saint Barth\xe9lemy', u'Saint Barth\xe9lemy'), (u'Saint Helena', u'Saint Helena'), (u'Saint Kitts and Nevis', u'Saint Kitts and Nevis'), (u'Saint Lucia', u'Saint Lucia'), (u'Saint Martin', u'Saint Martin'), (u'Saint Pierre and Miquelon', u'Saint Pierre and Miquelon'), (u'Saint Vincent and the Grenadines', u'Saint Vincent and the Grenadines'), (u'Samoa', u'Samoa'), (u'San Marino', u'San Marino'), (u'S\xe3o Tom\xe9 and Pr\xedncipe', u'S\xe3o Tom\xe9 and Pr\xedncipe'), (u'Saudi Arabia', u'Saudi Arabia'), (u'Senegal', u'Senegal'), (u'Serbia', u'Serbia'), (u'Seychelles', u'Seychelles'), (u'Sierra Leone', u'Sierra Leone'), (u'Singapore', u'Singapore'), (u'Sint Maarten', u'Sint Maarten'), (u'Slovakia', u'Slovakia'), (u'Slovenia', u'Slovenia'), (u'Solomon Islands', u'Solomon Islands'), (u'Somalia', u'Somalia'), (u'South Africa', u'South Africa'), (u'South Georgia', u'South Georgia'), (u'South Korea', u'South Korea'), (u'South Sudan', u'South Sudan'), (u'Spain', u'Spain'), (u'Sri Lanka', u'Sri Lanka'), (u'Sudan', u'Sudan'), (u'Suriname', u'Suriname'), (u'Svalbard and Jan Mayen', u'Svalbard and Jan Mayen'), (u'Swaziland', u'Swaziland'), (u'Sweden', u'Sweden'), (u'Switzerland', u'Switzerland'), (u'Syria', u'Syria'), (u'Taiwan', u'Taiwan'), (u'Tajikistan', u'Tajikistan'), (u'Tanzania', u'Tanzania'), (u'Thailand', u'Thailand'), (u'East Timor', u'East Timor'), (u'Togo', u'Togo'), (u'Tokelau', u'Tokelau'), (u'Tonga', u'Tonga'), (u'Trinidad and Tobago', u'Trinidad and Tobago'), (u'Tunisia', u'Tunisia'), (u'Turkey', u'Turkey'), (u'Turkmenistan', u'Turkmenistan'), (u'Turks and Caicos Islands', u'Turks and Caicos Islands'), (u'Tuvalu', u'Tuvalu'), (u'Uganda', u'Uganda'), (u'Ukraine', u'Ukraine'), (u'United Arab Emirates', u'United Arab Emirates'), (u'United Kingdom', u'United Kingdom'), (u'United States', u'United States'), (u'Uruguay', u'Uruguay'), (u'Uzbekistan', u'Uzbekistan'), (u'Vanuatu', u'Vanuatu'), (u'Venezuela', u'Venezuela'), (u'Vietnam', u'Vietnam'), (u'Wallis and Futuna', u'Wallis and Futuna'), (u'Western Sahara', u'Western Sahara'), (u'Yemen', u'Yemen'), (u'Zambia', u'Zambia'), (u'Zimbabwe', u'Zimbabwe')]

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

def contribute(request):
    bannertitle = "Contributions at a Glance:"

    changes = ProvChange.objects.all()
    accepted = ProvChange.objects.filter(status="Accepted")
    pending = ProvChange.objects.filter(status="Pending")
    users = User.objects.all()
    
    bannerleft = """
                    <div style="text-align:center">
                        <img style="width:100%" src="https://upload.wikimedia.org/wikipedia/commons/0/09/BlankMap-World-v2.png">
		    </div>
    """
    
    bannerright = """
                    <div style="text-align:left">

                        <br><br>
                        <b>How Does It Work?</b>
                        <br>
                        Choose a country from the list below. You can browse,
                        quality check, and suggest edits to existing province changes
                        already submitted by other users.
                        After a vetting process the change will be included in the
                        next version of the data available from the website.

                        <br><br>
                        <b>Who is it for?</b>
                        <br>
                        Whether you just want to track a recent change in your province, or map out the changes
                        for an entire country, all contributions count!

                    </div>
    """ 
    
    grids = []
    content = """
                <div style="text-align:center">

                        <div><em>
                            Users:
                            {users}
                            /
                            Contributions:
                            {changes}
                            /
                            Accepted:
                            {accepted}
                            /
                            Pending:
                            {pending}
                        
                        </em></div>
                </div>
                        """.format(changes=len(changes), users=len(users),
                                   accepted=len(accepted), pending=len(pending))

    grids.append(dict(title="",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))

    from django.db.models import Count,Max,Min
    
    fields = ["country","entries","mindate","maxdate"]
    lists = []
    rowdicts = dict([(countryid,dict(country=countryid,entries=0,mindate="-",maxdate="-")) for countryid,countryname in countries])
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
    grids.append(dict(title="Choose a Country:",
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
                return prov,"Merge"
            elif typ == "PartTransfer":
                prov = obj.fromname
                return prov,"Transfer"
            elif typ == "Breakaway":
                prov = obj.fromname
                return prov,"Split"
            elif typ == "NewInfo":
                prov = obj.fromname
                return prov,typ
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
        
        def getlinkrow(date,prov,typ,items):
            items = list(items)
            firstitem = items[0]
            if typ == "NewInfo":
                fields = ["fromcountry","source","date","fromname","fromalterns","fromtype","fromhasc","fromiso","fromfips","fromcapital","fromcapitalname"]
                params = urlencode(dict([(field,getattr(firstitem,field)) for field in fields]))
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(country), prov=urlquote(prov)) + params + '&type="NewInfo"'
                prov = markcountrychange(country, firstitem.fromname, firstitem.fromcountry)
            elif typ == "Split":
                fields = ["fromcountry","source","date","fromname","fromalterns","fromtype","fromhasc","fromiso","fromfips","fromcapital","fromcapitalname"]
                params = urlencode(dict([(field,getattr(firstitem,field)) for field in fields]))
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(country), prov=urlquote(prov)) + params + '&type="Split"'
                prov = markcountrychange(country, firstitem.fromname, firstitem.fromcountry)
            elif typ == "Merge":
                fields = ["tocountry","source","date","toname","toalterns","totype","tohasc","toiso","tofips","tocapital","tocapitalname"]
                params = urlencode(dict([(field,getattr(firstitem,field)) for field in fields]))
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(country), prov=urlquote(prov)) + params + '&type="Merge"'
                prov = markcountrychange(country, firstitem.toname, firstitem.tocountry)
            elif typ == "Transfer":
                fields = ["fromcountry","source","date","fromname","fromalterns","fromtype","fromhasc","fromiso","fromfips","fromcapital","fromcapitalname"]
                params = urlencode(dict([(field,getattr(firstitem,field)) for field in fields]))
                link = "/contribute/view/{country}/{prov}?".format(country=urlquote(country), prov=urlquote(prov)) + params + '&type="Transfer"'
                prov = markcountrychange(country, firstitem.fromname, firstitem.fromcountry)
            return link,(prov,typ)
        events = [getlinkrow(date,prov,typ,items) for (date,(prov,typ)),items in events]
        eventstable = lists2table(request, events, ["Province", "EventType"])

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
                        <a href="/contribute/" style="float:left; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Back to World
			</a>
			"""
        left = """	
			<h3 style="clear:both">Timeline for {countrytext}</h3>
			
                        <div id="blackbackground" style="">
                            <img style="width:200px;" src="http://www.freeiconspng.com/uploads/clock-event-history-schedule-time-icon--19.png">
                        </div>
                        <a style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;" href="/contribute/add/{country}">New date</a>
                        <br><br><br>
        """.format(countrytext=country.encode("utf8"), country=urlquote(country))
        right = """
                        <style>
                            #blackbackground a { color:white }
                            #blackbackground a:visited { color:grey }
                        </style>
                        
                        <div id="blackbackground" style="text-align: left">
                        <p style="font-size:large; font-weight:bold">Useful Sources:</p>
                        <p style="font-size:medium; font-style:italic">
                        <ul>
                            <li>
                            <a target="_blank" href="http://www.statoids.com">The Statoids website</a>
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
        """

        custombanner = """

                        {top}
                        
                        <table width="99%" style="clear:both; padding:0px; margin:0px">
                        <tr>
                        
                        <td style="width:48%; padding:1%; text-align:center; padding:0px; margin:0px; vertical-align:top">
                        {left}
                        </td>
                        
                        <td style="width:48%; padding:1%; padding:0px; margin:0px">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """.format(top=top, left=left, right=right)

        dates = [d["date"].isoformat() for d in (ProvChange.objects.filter(fromcountry=country).exclude(status="NonActive") | ProvChange.objects.filter(tocountry=country).exclude(status="NonActive")).order_by("date").values('date').distinct()]
        print dates

    ##    def getlinkrow(date):
    ##        link = "/contribute/view/{country}/?".format(country=urlquote(country)) + "date=" + date
    ##        return link, (date,)

    ##    daterows = [getlinkrow(date) for date in dates]
    ##    datestable = lists2table(request, daterows, ["Date"])

    ##    content = datestable
        
        grids = []
        for date in dates:
            content = getdateeventstable(date)
            grids.append(dict(title='{date}:'.format(date=date),
                              content=content+'<br><div width="100%" style="text-align:center"><a href="/contribute/add/{country}?date={date}" style="text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a></div>'.format(date=date, country=urlquote(country)),
                              style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                              width="99%",
                              ))
        
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

def markcountrychange(country, provtext, provcountry):
    if provcountry != country:
        provtext += " (%s)" % provcountry
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
        changes = ProvChange.objects.filter(fromcountry=country, date=date, type="NewInfo", fromname=prov, bestversion=True).exclude(status="NonActive") | ProvChange.objects.filter(tocountry=country, date=date, type="NewInfo", fromname=prov, bestversion=True).exclude(status="NonActive")
        change = next((c for c in changes.order_by("-added")), None)

        if change:
            oldinfo = '<li style="list-style:none">'+markcountrychange(country, change.fromname, change.fromcountry).encode("utf8")+"<br><br></li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Altnerate names: '+change.fromalterns.encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; ISO: '+change.fromiso.encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; FIPS: '+change.fromfips.encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; HASC: '+change.fromhasc.encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital: '+change.fromcapitalname.encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital moved: '+change.fromcapital.encode("utf8")+"</li>"
            oldinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Type: '+change.fromtype.encode("utf8")+"</li>"
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
        
            newinfo = '<li style="font-size:smaller; list-style:none"> {provtext}<a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a><br><br></li>'.format(pk=change.pk, provtext=markcountrychange(country, change.toname, change.tocountry).encode("utf8"))
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Alternate names: '+change.toalterns.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; ISO: '+change.toiso.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; FIPS: '+change.tofips.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; HASC: '+change.tohasc.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital: '+change.tocapitalname.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Capital moved: '+change.tocapital.encode("utf8")+"</li>"
            newinfo += '<li style="font-size:smaller; list-style:none">&nbsp;&nbsp; Type: '+change.totype.encode("utf8")+"</li>"
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


            pendingedits = ProvChange.objects.filter(changeid=change.changeid, status="Pending").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
            pendingeditstable = model2table(request, title="New Edits:", objects=pendingedits,
                                      fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])

            grids.append(dict(title="Pending Edits",
                              content=pendingeditstable,
                              style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                              width="99%",
                              ))

            oldversions = ProvChange.objects.filter(changeid=change.changeid, status="NonActive").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
            oldversionstable = model2table(request, title="Revision History:", objects=oldversions,
                                      fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])

            grids.append(dict(title="Revision History",
                              content=oldversionstable,
                              style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                              width="99%",
                              ))

            # NOT SURE BOUT FROMCOUNTRY HERE...
            conflicting = ProvChange.objects.filter(fromcountry=country, date=date, type="NewInfo", fromname=prov, bestversion=True).exclude(pk=change.pk)
            conflictingtable = model2table(request, title="Conflicting Submissions:", objects=conflicting,
                                          fields=["date","type","fromname","toname","country","user","added","status"])

            grids.append(dict(title="Conflicting Submissions",
                              content=conflictingtable,
                              style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                              width="99%",
                              ))

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
        changes = ProvChange.objects.filter(fromcountry=country,date=date,type="Breakaway",fromname=prov).exclude(status="NonActive") | ProvChange.objects.filter(tocountry=country,date=date,type="Breakaway",fromname=prov).exclude(status="NonActive")
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
        
        splitlist = "".join(('<li style="padding:10px 0px; list-style:none">&rarr; {provtext} <a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a></li>'.format(pk=change.pk, provtext=markcountrychange(country, change.toname, change.tocountry).encode("utf8")) for change in changes))
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
        changes = ProvChange.objects.filter(tocountry=country,date=date,type="FullTransfer",toname=prov).exclude(status="NonActive") | ProvChange.objects.filter(fromcountry=country,date=date,type="FullTransfer",toname=prov).exclude(status="NonActive")
        changes = changes.order_by("-added") # the dash reverses the order

        butstyle = 'text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;'
        plusbutstyle = 'text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:none; margin:5px;'

        givelist = "".join(('<li style="padding:10px 0px; list-style:none">{provtext} <a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a> &rarr;</li>'.format(pk=change.pk, provtext=markcountrychange(country, change.fromname, change.fromcountry).encode("utf8")) for change in changes))
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
        changes = ProvChange.objects.filter(tocountry=country,date=date,type="PartTransfer",fromname=prov).exclude(status="NonActive") | ProvChange.objects.filter(fromcountry=country,date=date,type="PartTransfer",fromname=prov).exclude(status="NonActive")
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
                <h2><em>Gave territory to:</em></h2>
                """

        butstyle = 'text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;'
        plusbutstyle = 'text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:medium; font-weight:bold; text-decoration:none; margin:5px;'

        splitlist = "".join(('<li style="padding:10px 0px; list-style:none">&rarr; {provtext} <a href="/provchange/{pk}/view" style="text-align:center; background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:small; font-weight:bold; text-decoration:underline; margin:10px;">View</a></li>'.format(pk=change.pk, provtext=markcountrychange(country, change.toname, change.tocountry).encode("utf8")) for change in changes))
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

                        {% if changelist %}
			
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

                        {% else %}

                            <tr>
                            <td></td>
                            {% for _ in fields %}
                                <td> - </td>
                            {% endfor %}
                            </tr>

                        {% endif %}
                            
		</table>
                """
    changelist = [(change.pk, [getattr(change,field) for field in fields]) for change in objects]
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

def dropchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)
    if request.user.username == change.user or 'user.administrator' in request.user.get_all_permission():
        change.status = "NonActive"
        change.save()

    return redirect("/provchange/{pk}/view/".format(pk=pk) )

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

    if change.type == "Breakaway":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["fromcountry","date","source","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Split&".format(country=urlquote(change.fromcountry), prov=urlquote(change.fromname)) + params
    elif change.type == "FullTransfer":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["tocountry","date","source","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Merge&".format(country=urlquote(change.tocountry), prov=urlquote(change.toname)) + params
    elif change.type == "PartTransfer":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["fromcountry","date","source","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Transfer&".format(country=urlquote(change.fromcountry), prov=urlquote(change.fromname)) + params
    elif change.type == "NewInfo":
        params = urlencode(dict([(k,getattr(change,k)) for k in ["fromcountry","date","source","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=NewInfo&".format(country=urlquote(change.fromcountry), prov=urlquote(change.fromname)) + params
    print 99999,change.type, change
    print 1111,eventlink

    pendingedits = ProvChange.objects.filter(changeid=change.changeid, status="Pending").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
    pendingeditstable = model2table(request, title="New Edits:", objects=pendingedits,
                              fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])

    oldversions = ProvChange.objects.filter(changeid=change.changeid, status="NonActive").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
    oldversionstable = model2table(request, title="Revision History:", objects=oldversions,
                              fields=["date","type","fromname","fromcountry","toname","tocountry","user","added","status"])

    args = {'pk': pk,
            'note': note,
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
                
    html = render(request, 'provchanges/viewchange.html', args)
        
    return html

@login_required
def editchange(request, pk):
    change = get_object_or_404(ProvChange, pk=pk)

    if request.method == "POST":
        fieldnames = [f.name for f in ProvChange._meta.get_fields()]
        formfieldvalues = dict(((k,v) for k,v in request.POST.items() if k in fieldnames))
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
        fields = ["first_name","last_name","email","institution"]

@login_required
def account_edit(request):
    userobj = User.objects.get(username=request.user)
    form = UserInfoForm(instance=userobj)
    if request.POST:
        userobj.first_name = request.POST["first_name"]
        userobj.last_name = request.POST["last_name"]
        userobj.email_name = request.POST["email"]
        userobj.institution = request.POST["institution"]
        print userobj.first_name
        userobj.save()
        return redirect("/account/")
    else:
        ##form.fields["email"].widget.attrs['readonly'] = "readonly"
        return render(request, 'provchanges/accountedit.html', {"user":request.user, "userinfoform":form}
                      )

@login_required
def account(request):
    userobj = User.objects.get(username=request.user)
    userform = UserInfoForm(instance=userobj)
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
                <div style="text-align:center">
                    {userinfoform}
                </div>
                <div style="text-align:center">
                    <a href="/account/edit" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                        Edit
                    </a>
                </div>
                <br>
                """.format(userinfoform=userform.as_p())

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

    
    bannerright = """
                    <br><br><br><br><br>
                    <a href="/logout" style="background-color:orange; color:white; border-radius:5px; padding:5px">
                        <b>Logout</b>
                        </a>
                        """
    grids.append(dict(title="Your Contributions:",
                      content="table...",
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="100%",
                      ))
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )












# Event forms

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

    step_title = "Source of Information"
    step_descr = """
                   Where are you getting the information from? 
                
                   """

    class Meta:
        model = ProvChange
        fields = ['source']

    def __init__(self, *args, **kwargs):
        super(SourceEventForm, self).__init__(*args, **kwargs)
        country = kwargs["initial"]["fromcountry"]
        sources = [r.source for r in ProvChange.objects.filter(fromcountry=country).annotate(count=Count('source')).order_by('-count')]
        mostcommon = sources[0]
        sources = sorted(set(sources))
        self.fields["source"].widget = ListTextWidget(data_list=sources, name="sources", attrs=dict(size=90))
        self.fields['source'].initial = mostcommon
        
from django.forms.widgets import RadioFieldRenderer

EVENTTYPEINFO = {"NewInfo": {"label": "NewInfo",
                         "short": "A change was made to a province's name, codes, or capital.",
                          "descr": """
                                    Description...
                                    """,
                          "img": '<img style="width:100px" src="http://www.gov.mb.ca/conservation/climate/images/climate_affect.jpg"/>',
                          },
              "Split": {"label": "Split",
                               "short": "A province split into multiple new ones",
                              "descr": """
                                        Description...
                                        """,
                              "img": '<img style="width:100px" src="http://www.gov.mb.ca/conservation/climate/images/climate_affect.jpg"/>',
                              },
             "Merge": {"label": "Merge",
                              "short": "One or more provinces merged entirely into another province.",
                              "descr": """
                                        Description...
                                        """,
                              "img": '<img style="width:100px" src="http://www.gov.mb.ca/conservation/climate/images/climate_affect.jpg"/>',
                              },
             "Transfer": {"label": "Transfer",
                              "short": "A province gave parts of its territory to one or more provinces.",
                              "descr": """
                                        Description...
                                        """,
                              "img": '<img style="width:100px" src="http://www.gov.mb.ca/conservation/climate/images/climate_affect.jpg"/>',
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

    step_title = "Type of Change"
    step_descr = """
                    What type of event was it? 
                   """
    type = forms.ChoiceField(choices=[("NewInfo","NewInfo"),("Split","Split"),("Merge","Merge"),("Transfer","Transfer")], widget=forms.RadioSelect(renderer=TypeEventRenderer))

##    class Meta:
##        widgets = {"type": forms.RadioSelect(renderer=TypeEventRenderer) }

class FromEventForm(forms.ModelForm):

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
    year = forms.ChoiceField(choices=[(yr,yr) for yr in range(1800, 2014+1)])
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

        url = "/contribute/view/{country}?date={date}".format(country=urlquote(country), date=urlquote(date))
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
                      "2": lambda wiz: wiz.get_cleaned_data_for_step("1")["type"] in ("Split","NewInfo","Transfer") if wiz.get_cleaned_data_for_step("1") else False,
                      "3": lambda wiz: wiz.get_cleaned_data_for_step("1")["type"] == "Merge" if wiz.get_cleaned_data_for_step("1") else False,
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
                kwargs["step_descr"] = "Please identify the province that transferred part of its territory?"
            elif typ == "Merge":
                kwargs["step_descr"] = "Please identify the province that gained territory after all the mergers?"

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
            prov = data["fromname"]
        elif data["type"] == "NewInfo":
            prov = data["fromname"]

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

    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=TypeChangeRenderer) }
        

class MergeTypeChangeForm(forms.ModelForm):
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=MergeTypeChangeRenderer) }

class TransferTypeChangeForm(forms.ModelForm):
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=TransferTypeChangeRenderer) }

class SplitTypeChangeForm(forms.ModelForm):
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=SplitTypeChangeRenderer) }

class GeneralChangeForm(forms.ModelForm):

    # USED TO SHOW INDIVIDUAL CHANGES
    # THE DESCRIPTIONS DONT ACTUALLY SHOW, SO SHOULD BE REMOVED
    # ...

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
        fields = ['date', 'source']
        widgets = {"date": CustomDateWidget()}

class FromChangeForm(forms.ModelForm):

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

function addlayer(geoj) {
    var geojson_format = new OpenLayers.Format.GeoJSON();
    var vectors = new OpenLayers.Layer.Vector("Existing Clip Polygons", {style:{fillColor:"blue", fillOpacity:0.5}});
    var features = geojson_format.read(geoj, "FeatureCollection");
    
    //vectors.addFeatures requires an array, thus
    if(features.constructor != Array) {
        features = [features];
    }
    vectors.addFeatures(features);
    jsmap.map.addLayers([vectors]);
};

function setupmap() {
    // layer switcher
    jsmap.map.addControl(new OpenLayers.Control.LayerSwitcher({'div':OpenLayers.Util.getElement('layerswitcher')}));
    syncwms();
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


class GeoChangeForm(forms.ModelForm):

    step_title = "Territory"
    step_descr = """
                    What did the giving province look like before giving away territory?
                   """

    class Meta:
        model = ProvChange
        fields = ["transfer_reference", "transfer_source", "transfer_geom"]
        widgets = {"transfer_geom": CustomOLWidget(attrs={"id":"geodjango_transfer_geom"}),
                    "transfer_source": ListTextWidget([], name="sources", attrs={'size': 90, "id":"id_transfer_source"}),
                    "transfer_reference": ListTextWidget([], name="references", attrs={'size': 90, "id":"id_transfer_reference"}),
                   }
        
    def __init__(self, *args, **kwargs):
        self.country = kwargs.pop("country")
        self.province = kwargs.pop("province")
        self.date = kwargs.pop("date")
        print "kwargs",kwargs
        super(GeoChangeForm, self).__init__(*args, **kwargs)
        print 999, self.fields["transfer_geom"].widget

        print kwargs
        if "initial" in kwargs:
            country = kwargs["initial"]["country"]
            provs = ProvChange.objects.filter(fromcountry=country) | ProvChange.objects.filter(tocountry=country)
            sources = sorted((r.transfer_source for r in provs.distinct("transfer_source")))
            references = sorted((r.transfer_reference for r in provs.distinct("transfer_reference")))
            self.fields['transfer_source'].widget._list = sources
            self.fields['transfer_reference'].widget._list = references

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
                        Make sure the map doesn't have a license that restricts sharing or derivative work. 
                        Here are some useful sources for historical maps:

                        <ul>
                            <li><a target="_blank" href="http://mapwarper.net/">MapWarper</a></li>
                            <li><a target="_blank" href="http://www.oldmapsonline.org/">OldMapsOnline</a></li>
                            <li><a target="_blank" href="https://www.loc.gov/maps/?q=administrative%20divisions">The Library of Congress Map Collection</a></li>
                            <li><a target="_blank" href="https://www.lib.utexas.edu/maps/historical/index.html">The Perry-Castaneda Library Map Collection</a></li>
                            <li><a target="_blank" href="http://alabamamaps.ua.edu/historicalmaps/">Alabama Maps Historical Maps</a></li>
                            <li><a target="_blank" href="http://www.zum.de/whkmla/region/indexa.html">World History at KMLA</a></li>
                            <li><a target="_blank" href="http://www.antiquemapsandprints.com/prints-and-maps-by-country-12-c.asp">Antique Maps and Prints</a></li>
                            <li><a target="_blank" href="http://catalogue.defap-bibliotheque.fr/index.php?lvl=index">La bibliotheque du Defap</a></li>
                        </ul>

                        Georeference the map at <a target="_blank" href="http://mapwarper.net/">MapWarper</a>
                        and get its "WMS" link (under the "Export" tab) so you can overlay it on the map.

                        <div style="padding:20px">WMS Map Link: {{ form.transfer_source }}</div>

                        <div style="padding:20px">Map Description: {{ form.transfer_reference }}</div>

                        <br>

                        <div>{{ form.transfer_geom }}</div>

                        <div style="clear:both">
                        <br>
                        Instructions:
                        <br>
                        <ol>
                            <li>
                            Guided by the map, draw a clipping polygon that traces the border between the giving and receiving province (if any).
                            </li>
                            <li>
                            If the giving province shares a border with any previously drawn giving provinces (shown in blue), make sure the clipping polygon
                            covers every part of that border, so that there is no gap in between. 
                            </li>
                            <li>
                            Then close the polygon by encircling all areas (incl. islands) that were transferred. Draw multiple polygons
                            if necessary.
                            </li>
                        </ol>
                        </div>
                        
                    """
        # add features
        country = self.country
        province = self.province
        date = self.date
        
        otherfeats = ProvChange.objects.filter(fromcountry=country, date=date).exclude(status="NonActive") | ProvChange.objects.filter(tocountry=country, date=date).exclude(status="NonActive")
        import json
        geoj = {"type":"FeatureCollection",
                "features": [dict(type="Feature", properties=dict(fromname=f.fromname), geometry=json.loads(f.transfer_geom.json))
                             for f in otherfeats if f.transfer_geom]}
        print json.dumps(geoj)
        html += """<script>
                addlayer('{geoj}')
                </script>
                """.format(geoj=json.dumps(geoj))
        
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
            trans = dict([(k.replace("to","from"),v) for k,v in eventvalues.items() if k.startswith("to")])
            eventvalues = dict([(k,v) for k,v in eventvalues.items() if not k.startswith("to")])
            eventvalues.update(trans)

        objvalues = dict(eventvalues)
        objvalues.update(formfieldvalues)
        print objvalues
        obj = ProvChange.objects.create(**objvalues)
        obj.changeid = obj.pk # upon first creation, changeid becomes the same as the pk, but remains unchanged for further revisions
        print obj
        
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
        params = urlencode(dict([(k,getattr(obj,k)) for k in ["fromcountry","date","source","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]]))
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
        params = urlencode(dict([(k,getattr(obj,k)) for k in ["fromcountry","date","source","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]]))
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
    date = None

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
        params = urlencode(dict([(k,getattr(obj,k)) for k in ["tocountry","date","source","toname","toalterns","toiso","tohasc","tofips","totype","tocapitalname","tocapital"]]))
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
                      "1": lambda wiz: False,
                      "2": lambda wiz: True,
                      "3": _geomode,}

    country = None
    province = None

    def get_form_kwargs(self, step=None):
        kwargs = {}
        if step == "2": # from or to form
            kwargs["step_descr"] = "Please identify the province that received territory?"
        elif step == "3":
            kwargs["country"] = self.country
            kwargs["province"] = self.province
            kwargs["date"] = self.request.GET["date"]
        return kwargs

    def get_form_initial(self, step=None):
        data = dict()
        if step == "2":
            data["tocountry"] = self.country
        elif step == "3":
            data["country"] = self.country
        return data  
    
    def done_redirect(self, obj):
        params = urlencode(dict([(k,getattr(obj,k)) for k in ["fromcountry","date","source","fromname","fromalterns","fromiso","fromhasc","fromfips","fromtype","fromcapitalname","fromcapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Transfer&".format(country=urlquote(self.country), prov=urlquote(obj.fromname)) + params
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



