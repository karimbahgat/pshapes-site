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
                    <br><br>
                    <div style="text-align:center">
                        [INSERT MAP HERE]
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
    rowdicts = dict([(countryid,dict(country=countryid,entries=0,mindate="-",maxdate="-")) for countryid,countryname in ProvChange._meta.get_field("country").choices])
    for rowdict in ProvChange.objects.values("country").annotate(entries=Count('pk'),
                                                                 mindate=Min("date"),
                                                                 maxdate=Max("date")):
        rowdicts[rowdict["country"]] = rowdict

    for country in sorted(rowdicts.keys()):
        rowdict = rowdicts[country]
        print rowdict
        row = [rowdict[f] for f in fields]
        url = "/contribute/view/%s" % urlquote(rowdict["country"])
        lists.append((url,row))
    
    countriestable = lists2table(request, lists=lists,
                              fields=fields)
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


def viewcountry(request, country):
    # TODO: Add "new-event" button
    bannertitle = "%s:"%country.encode("utf8")
    bannerleft = """
                    <div style="text-align:left">
                        [INSERT MAP HERE]
		    </div>
    """
    bannerright = """
			Maybe some country stats...
    """

    changes = ProvChange.objects.filter(country=country).order_by("-added") # the dash reverses the order
    import itertools
    def typeprov(obj):
        typ = obj.type
        if "Transfer" in typ:
            prov = obj.toname
            return "Expansion",prov
        elif typ == "Breakaway":
            prov = obj.fromname
            return "Split",prov
        elif typ == "NewInfo":
            prov = obj.toname
            return typ,prov
    def events():
        datekey = lambda o: o.date
        for date,dategroup in itertools.groupby(sorted(changes,key=datekey), key=datekey):
            dategroup = list(dategroup)
            #splits
            subkey = lambda o: o.fromname
            for splitfrom,splitgroup in itertools.groupby(sorted(dategroup,key=subkey), key=subkey):
                splitgroup = list(splitgroup)
                splits = [ch for ch in splitgroup if ch.type == "Breakaway"]
                if splits:
                    splits.extend((ch for ch in splitgroup if ch.type == "NewInfo"))
                    yield (date,("Split",splitfrom)), splits
            # mergers
            subkey = lambda o: o.toname
            for mergeto,mergegroup in itertools.groupby(sorted(dategroup,key=subkey), key=subkey):
                mergegroup = list(mergegroup)
                mergers = [ch for ch in mergegroup if "Transfer" in ch.type]
                if mergers:
                    mergers.extend((ch for ch in mergegroup if ch.type == "NewInfo"))
                    yield (date,("Expansion",mergeto)), mergers
            # newinfos
            subkey = lambda o: o.fromname
            for fromname,newgroup in itertools.groupby(sorted(dategroup,key=subkey), key=subkey):
                newinfos = [ch for ch in newgroup if "NewInfo" == ch.type and ch not in splits and ch not in mergers]
                if newinfos:
                    yield (date,("NewInfo",fromname)), newinfos

    events = events()
    
##    sortkey = lambda o:(o.date,typeprov(o))
##    events = itertools.groupby(sorted(changes,key=sortkey), key=sortkey)
    
    def getlinkrow(date,prov,typ,items):
        items = list(items)
        firstitem = items[0]
        if typ == "NewInfo":
            if len(set((i.type for i in items))) > 1:
                return None # if items has NewInfo and some other type that means it should be part of that other type and not listed as a separate newinfo event
            link = "/provchange/{pk}/view/".format(pk=firstitem.pk)
        elif typ == "Split":
            fields = ["country","source","date","fromname","fromtype","fromhasc","fromiso","fromfips","fromcapital"]
            params = urlencode(dict([(field,getattr(firstitem,field)) for field in fields]))
            link = "/contribute/view/{country}/{prov}?".format(country=urlquote(country), prov=urlquote(prov)) + params + '&type="Split"'
        elif typ == "Expansion":
            fields = ["country","source","date","toname","totype","tohasc","toiso","tofips","tocapital"]
            params = urlencode(dict([(field,getattr(firstitem,field)) for field in fields]))
            link = "/contribute/view/{country}/{prov}?".format(country=urlquote(country), prov=urlquote(prov)) + params + '&type="Expansion"'
        return link,(date,prov,typ)
    events = [getlinkrow(date,prov,typ,items) for (date,(typ,prov)),items in events]
    eventstable = lists2table(request, events, ["Date", "Province", "EventType"])

    content = eventstable
    
    grids = []
    grids.append(dict(title='List of events: <a href="/contribute/add/%s">Add event</a>' % urlquote(country),
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
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
        # add event, ensure enough params
        return addevent(request, country)

    else:
        # add individual change (preferably to existing event), ensure enough params are provided
        return addchange(request, country, province)


def viewevent(request, country, province):
    # TODO: add "edit-event" button in main banner
    # and "add-change" button down by the table
    assert all((param in request.GET for param in "date type".split()))
    #country = request.GET["country"].strip('"').strip("'").strip()
    y,m,d = map(int,request.GET["date"].strip('"').strip("'").strip().split("-"))
    date = datetime.date(year=y,month=m,day=d)
    prov = province #request.GET["prov"].strip('"').strip("'").strip()
    typ = request.GET["type"].strip('"').strip("'").strip()
    
    bannertitle = '<a href="/contribute/view/{country}" style="color:inherit">{countrytext}</a>, {provtext}:'.format(country=urlquote(country),countrytext=country.encode("utf8"),provtext=prov.encode("utf8"))
    bannerleft = """
                    <div style="text-align:left">
                        <b>Event type:</b> {typ}
                        <br><br>
                        <b>Date:</b> {date}
                        <br><br>
                        
		    </div>
    """.format(typ=typ,date=date)
    bannerright = """
                        <br><br><br><br>
			What else... Maybe image for type of event, and quick stats of how many changes etc in this event...
    """
    print "TYPE",repr(typ)
    if typ == "NewInfo":
        # shouldnt happen...
        fields = ["fromname","type"]
        changes = ProvChange.objects.filter(country=country,date=date,type="NewInfo",toname=prov)
    elif typ == "Split":
        fields = ["fromname","toname","type","status"]
        changes = ProvChange.objects.filter(country=country,date=date,type__in=["Breakaway","NewInfo"],fromname=prov)
    elif typ == "Expansion":
        fields = ["fromname","toname","type","status"]
        changes = ProvChange.objects.filter(country=country,date=date,type__in=["FullTransfer","PartTransfer"],toname=prov) | ProvChange.objects.filter(country=country,date=date,type="NewInfo",fromname=prov)
    changes = changes.order_by("-added") # the dash reverses the order
    changestable = model2table(request, title="", objects=changes, fields=fields)

    content = changestable
    
    grids = []
    grids.append(dict(title='Event changes: <a href="/contribute/add/{country}/{province}?{params}">Add change</a>'.format(country=urlquote(country), province=urlquote(prov), params=request.GET.urlencode()),
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="99%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
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
    elif request.GET["type"].lower().strip('"') == "expansion":
        func = AddExpansionChangeWizard.as_view(country=country, province=province)
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
        params = urlencode(dict([(k,getattr(change,k)) for k in ["country","date","source","fromname","fromiso","fromhasc","fromfips","fromtype","fromcapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Split&".format(country=urlquote(change.country), prov=urlquote(change.fromname)) + params
    elif "Transfer" in change.type:
        params = urlencode(dict([(k,getattr(change,k)) for k in ["country","date","source","toname","toiso","tohasc","tofips","totype","tocapital"]]))
        eventlink = "/contribute/view/{country}/{prov}/?type=Expansion&".format(country=urlquote(change.country), prov=urlquote(change.fromname)) + params
    elif change.type == "NewInfo":
        eventlink = None
        pass # ...
    print 99999,change.type, change
    print 1111,eventlink

    pendingedits = ProvChange.objects.filter(changeid=change.changeid, status="Pending").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
    pendingeditstable = model2table(request, title="New Edits:", objects=pendingedits,
                              fields=["date","type","fromname","toname","country","user","added","status"])

    oldversions = ProvChange.objects.filter(changeid=change.changeid, status="NonActive").exclude(pk=change.pk).order_by("-added") # the dash reverses the order
    oldversionstable = model2table(request, title="Revision History:", objects=oldversions,
                              fields=["date","type","fromname","toname","country","user","added","status"])

    args = {'pk': pk,
            'note': note,
            'eventlink': eventlink,
            'metachange': MetaChangeForm(instance=change),
            'typechange': TypeChangeForm(instance=change),
            'generalchange': GeneralChangeForm(instance=change),
            'histomap': HistoMapForm(instance=change),
            'georef': GeorefForm(instance=change),
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
                'histomap': HistoMapForm(instance=change),
                'georef': GeorefForm(instance=change),
                'geochange': GeoChangeForm(instance=change),
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

        













# Event forms

class GeneralEventForm(forms.ModelForm):

    step_title = "Basic Information"
    step_descr = """
                    Welcome to the step-by-step wizard for submitting historical
                    changes to the "primary" or "level-1" sub-administrative units of countries.
                    At what date did the event occur, and where are you getting the information from? 
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
                   """

    class Meta:
        model = ProvChange
        fields = ['date', 'source']
        widgets = {"date": CustomDateWidget()}

from django.forms.widgets import RadioFieldRenderer

EVENTTYPEINFO = {"NewInfo": {"label": "NewInfo",
                         "short": "A change was made to a province's name, codes, or capital.",
                          "descr": """
                                    Most province changes are as simple as changes in their basic information. 
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
             "Expansion": {"label": "Expansion",
                              "short": "A province received territory from or merged entirely with other provinces.",
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
    type = forms.ChoiceField(choices=[("NewInfo","NewInfo"),("Split","Split"),("Expansion","Expansion")], widget=forms.RadioSelect(renderer=TypeEventRenderer))

##    class Meta:
##        widgets = {"type": forms.RadioSelect(renderer=TypeEventRenderer) }

class FromEventForm(forms.ModelForm):

    step_title = "From Province"
    step_descr = """
                    Please identify the province that split.
                   """

    class Meta:
        model = ProvChange
        fields = 'fromname fromiso fromfips fromhasc fromcapital fromtype'.split()

class ToEventForm(forms.ModelForm):

    step_title = "To Province"
    step_descr = """
                    Please identify the province that expanded / received territory?
                   """

    class Meta:
        model = ProvChange
        fields = 'toname toiso tofips tohasc tocapital totype'.split()


class AddEventWizard(SessionWizardView):
    form_list = [   GeneralEventForm,
                     TypeEventForm,
                      FromEventForm,
                      ToEventForm,
                      ]

    # NOTE: MUST BE EITHER EXPANSION OR SPLIT OR NEWINFO EVENT, WITH GET PARAMS FOR ALL CONSTANT EVENTINFO
    condition_dict = {"0": lambda wiz: True,
                      "1": lambda wiz: True,
                      "2": lambda wiz: wiz.get_cleaned_data_for_step("1")["type"] in ("Split","NewInfo") if wiz.get_cleaned_data_for_step("1") else False,
                      "3": lambda wiz: wiz.get_cleaned_data_for_step("1")["type"] == "Expansion" if wiz.get_cleaned_data_for_step("1") else False,
                      }

    country = None

    def __iter__(self):
        for step in self.get_form_list():
            yield self.get_form(step=step)
 
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
        print "DATA",data
        country = self.country
        
        if data["type"] == "Expansion":
            prov = data["toname"]
        elif data["type"] == "Split":
            prov = data["fromname"]
        elif data["type"] == "NewInfo":
            sfafdsafdas
            # ....
            
        keys = data.keys() #["date","source","type"]
        params = urlencode( [(key,data[key]) for key in keys] + [("country",country)] )
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

class ExpansionTypeChangeRenderer(RadioFieldRenderer):

    def render(self):
        choices = [(w,TYPEINFO[w.choice_label]) for w in self if w.choice_label in ["NewInfo","PartTransfer","FullTransfer"]]
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
        choices = [(w,TYPEINFO[w.choice_label]) for w in self if w.choice_label in ["NewInfo","Breakaway"]]
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
                    What type of change was it? Multiple changes may have to be submitted for the same date.
                    For instance, on a given date, a province may receive territory from two of its neighbours, annex
                    a third neighbour, and change its name and ISO code. 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=TypeChangeRenderer) }
        

class ExpansionTypeChangeForm(forms.ModelForm):
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? Multiple changes may have to be submitted for the same date.
                    For instance, on a given date, a province may receive territory from two of its neighbours, annex
                    a third neighbour, and change its name and ISO code. 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=ExpansionTypeChangeRenderer) }

class SplitTypeChangeForm(forms.ModelForm):
    step_title = "Type of Change"
    step_descr = """
                    What type of change was it? Multiple changes may have to be submitted for the same date.
                    For instance, on a given date, a province may receive territory from two of its neighbours, annex
                    a third neighbour, and change its name and ISO code. 
                   """

    class Meta:
        model = ProvChange
        fields = ['type']
        widgets = {"type": forms.RadioSelect(renderer=SplitTypeChangeRenderer) }

class GeneralChangeForm(forms.ModelForm):

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
        fields = ['country', 'date', 'source']
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
    
    def render(self, name, value, attrs=None):
        output = super(CustomOLWidget, self).render(name, value, attrs=attrs)
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
// layer switcher
geodjango_5_transfer_geom.map.addControl(new OpenLayers.Control.LayerSwitcher({'div':OpenLayers.Util.getElement('layerswitcher')}));

// other controls
/*
geodjango_5_transfer_geom.map.controls.forEach(function (contr){
    alert(contr.displayClass)
    //geodjango_5_transfer_geom.map.removeControl(contr);
    if (contr.displayClass != "olControlDrawFeaturePolygon")
        {
        geodjango_5_transfer_geom.map.removeControl(contr);
        };
    });
*/
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

    def clean(self):
        data = super(GeorefForm, self).clean()
        if data:
            if "mapwarper.net" in data['transfer_source']:
                pass
            else:
                mapwarpid = data['transfer_source']
                data['transfer_source'] = "http://mapwarper.net/maps/wms/%s" % mapwarpid
        return data
        
    def as_p(self):
        html = """
                        Georeferencing is as easy as matching a handful of control points on your historical map image with the equivalent
                        locations on a real-world map.
                        For this you must <a href="http://mapwarper.net/">create an account or login to the MapWarper project website</a>.

                        <br><br>
                        <img style="display:block" align="middle" height=300px src="http://dirtdirectory.org/sites/dirtdirectory.org/files/screenshots/mapwarper.PNG"/>
                        <br>

                        Once finished with georeferencing, simply insert the MapWarper ID of your georeferenced map
                        (a short number near the top of the MapWarper page)
                        into the field below. 

                        <div style="padding:20px"><b>MapWarper Map ID: </b>{{ form.transfer_source }}</div>
                """
        rendered = Template(html).render(Context({"form":self}))
        return rendered


class GeoChangeForm(forms.ModelForm):

    step_title = "Territory"
    step_descr = """
                    What did the giving province look like before giving away territory?
                   """

    class Meta:
        model = ProvChange
        fields = ["transfer_geom"]
        widgets = {"transfer_geom": CustomOLWidget() }
        
    def __init__(self, *args, **kwargs):
        super(GeoChangeForm, self).__init__(*args, **kwargs)
        print 999, self.fields["transfer_geom"].widget
        
    def as_p(self):
        html = """
                        Finally, draw on the map. Identify the borders of the province that gave away the territory, as it looked like prior to giving away territory.
                        This will be used to determine the extent of the territory that changed hands.

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
        formfieldvalues["added"] = datetime.date.today()
        formfieldvalues["bestversion"] = True
        print formfieldvalues

        eventvalues = dict(((k,v) for k,v in self.request.GET.items()))
        print eventvalues

        if eventvalues["type"].strip('"') == "Expansion" and formfieldvalues["type"].strip('"') == "NewInfo":
            # all tos become froms when newinfo for expansion event
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
        html = redirect("/provchange/%s/view/" % obj.pk)

        return html


class AddSplitChangeWizard(AddChangeWizard):

    form_list = [   SplitTypeChangeForm,
                    ToChangeForm,
                      ]

    country = None
    province = None
    
    def get_form(self, step=None, data=None, files=None):
        print "HELLOOOO", self.request.GET, repr(self.request.GET["type"].lower())
        if data:
            print data
            data = dict([(key,data.getlist(key)[0] if isinstance(data.getlist(key),list) else data.getlist(key)) for key in data.keys()])
        else:
            data = {}
        print data

        form = super(AddSplitChangeWizard, self).get_form(step, data=data, files=files)        

        return form

class AddExpansionChangeWizard(AddChangeWizard):

    form_list = [   ExpansionTypeChangeForm,
                    FromChangeForm,
                    ToChangeForm,
                     HistoMapForm,
                     GeorefForm,
                      GeoChangeForm,
                      ]
    
    def _geomode(wiz):
        typeformdata = wiz.get_cleaned_data_for_step("0") or {"type":"NewInfo"}
        print wiz.get_cleaned_data_for_step("0")
        return "Transfer" in typeformdata["type"]

    condition_dict = {"0": lambda wiz: True,
                      "1": lambda wiz: wiz.get_cleaned_data_for_step("0")["type"] != "NewInfo" if wiz.get_cleaned_data_for_step("0") else None,
                      "2": lambda wiz: wiz.get_cleaned_data_for_step("0")["type"] == "NewInfo" if wiz.get_cleaned_data_for_step("0") else None,
                      "3": _geomode,
                      "4": _geomode,
                      "5": _geomode,}

    country = None
    province = None
    
    def get_form(self, step=None, data=None, files=None):
        print "HELLOOOO", self.request.GET, repr(self.request.GET["type"].lower())
        if data:
            print data
            data = dict([(key,data.getlist(key)[0] if isinstance(data.getlist(key),list) else data.getlist(key)) for key in data.keys()])
        else:
            data = {}
        print data

        form = super(AddExpansionChangeWizard, self).get_form(step, data=data, files=files)        

        if isinstance(form, GeoChangeForm):
            # ADD CUSTOM WMS
            typeformdata = self.get_cleaned_data_for_step("0") or {"type":"NewInfo"}
            if "Transfer" in typeformdata["type"]:
                wmsdata = self.get_cleaned_data_for_step("4") or {}
                wms = wmsdata.get("transfer_source")
                if wms:
                    wms = wms.split("?")[0]+"?service=wms&format=image/png" # trim away junk wms params and ensure uses transparency
                    form.fields['transfer_geom'].widget.wms = wms
        return form
    

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



