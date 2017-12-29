"""pshapes_site

Static page views.

"""
from django.shortcuts import render, redirect
from django.template import Template,Context
from django.contrib.auth.decorators import login_required

from provchanges.models import ProvChange, Comment, Vouch
from provshapes.models import ProvShape

shortdescr = """
Pshapes (pronounced p-shapes) is an open-source crowdsourcing project for creating and maintaining
data on historical provinces, created by and for data-enthusiasts, researchers,
and others. 
"""

def lists2table(request, lists, fields):
    html = """
		<table style="font-size:small"> 
		
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
					{% if url %}
                                            <a href="{{ url }}">View</a>
                                        {% endif %}
					</td>
					
                                        {% for value in row %}
                                            <td>{{ value | safe}}</td>
                                        {% endfor %}
					
				</tr>
			{% endfor %}
		</table>
                """
    rendered = Template(html).render(Context({"request":request, "fields":fields, "lists":lists}))
    return rendered

def recentadds(request, num=5):
    html = """
		<table style="font-size:small"> 

			<tr>
				<th> 
				</th>
				
				<th>
                <b>User</b>
				</th>

				<th>
                <b>Added</b>
				</th>
			
				<th>
                <b>Country</b>
				</th>

				<th>
                <b>Province</b>
				</th>
				
				<th>
                <b>Type</b>
				</th>
				
			</tr>
			</a>
			
			{% for change in changelist %}
				<tr>
					<td>
					<a href="{% url 'viewchange' pk=change.pk %}">View</a>
					</td>
					
					<td>
					{{ change.user }}
					</td>

					<td>
					{{ change.added }}
					</td>

                            {% if "Transfer" in change.type %}

					<td>
					{{ change.tocountry }}
					</td>
					
					<td>
					{{ change.toname }}
					</td>

			    {% else %}

					<td>
					{{ change.fromcountry }}
					</td>
					
					<td>
					{{ change.fromname }}
					</td>

			    {% endif %}
					
					<td>
					{{ change.type }}
					</td>
					
				</tr>
			{% endfor %}
		</table>
	    """
    changelist = ProvChange.objects.all().order_by("-added")[:num]   # the dash reverses the order
    rendered = Template(html).render(Context({"request":request, "shortdescr":shortdescr, "changelist":changelist}))
    return rendered



def home(request):
    changelist = ProvChange.objects.all().order_by("-added") # the dash reverses the order
    return render(request, 'pshapes_site/home.html', {"shortdescr":shortdescr, "changelist":changelist})

def home(request):
    bannertitle = ""
##    bannerleft = """
##			<style>
##			.shadow
##			{
##				display:block;
##				position:relative;
##				height:300px;
##				background-image:url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYci40tiT9XecIGMtu8pLPGd7XqYXwNT_CCZ5PtyDA9ubVl0-P7g);
##				background-size:100% 100%;
##			}
##			.shadow:before
##			{
##				display:block;
##				content:'';
##				position:absolute;
##				width:100%;
##				height:100%;
##				-moz-box-shadow:inset 0px 0px 3px 1px rgba(0,0,0,1);
##				-webkit-box-shadow:inset 0px 0px 3px 1px rgba(0,0,0,1);
##				box-shadow:inset 0px 0px 10px 10px rgba(0,0,0,1);
##			}
##			</style>
##			<div class="shadow"></div>
##    """
    if not request.user.is_authenticated():
        quickstartbut = """
			<a href="/registration" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Sign Up
			</a>
			or
			<a href="/login" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Login
			</a>
			"""
    else:
        quickstartbut = """
			<a href="/contribute/countries" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Get Started
			</a>
			"""
    bannerright = """
                    <br>
                    <h3 style="text-align:left">Crowdsourcing Historical Province Boundaries</h3>
                    <div style="text-align:left">
                        <p>%s</p>

                        <p style="font-size:smaller"><em>Note: This is an early Alpha trial version of the website to test
                        out the data collection effort. Suggestions
                        and feature requests are welcome.</em>
                        </p>
                    </div>

                    <br>
                    <div style="text-align:right;">
                        <a href="/about" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                        <b>Read More</b>
                        </a>
                    </div>
                    <br>
                    """ % shortdescr
    #<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYci40tiT9XecIGMtu8pLPGd7XqYXwNT_CCZ5PtyDA9ubVl0-P7g">
    bannerleft = """
                    <br>
                    <img src="/static/webfrontimg.png" width="80%%">
                    <p>
                    %s
                    </p>
                    """ % quickstartbut
##    if request.user.is_authenticated():
##        bannerright = """
##                        <br>
##                        <p>Not sure what to put here...</p>
##                        <p>Maybe slideshow of stepbystep instructions...</p>
##                        <p>Or latest site news or blog/progress notes...</p>
##                        """ 

    grids = []
##    grids.append(dict(title="Project News:",
##                      content="""
##                            <p>October 2016: <br> Alpha Website up-and-running</p>
##                            """,
##                      width="25%",
##                      ))

##    grids.append(dict(title="What is Pshapes?",
##                      content="""
##                        <p style="color:black;">
##                        <em><b><q>%s</q></b></em>
##                        </p>
##                        <div style="text-align:right;">
##                        <a href="/about" style="color:white;"><b>Read More</b></a>
##                        </div>
##                        """%shortdescr
##                      ))
##    grids.append(dict(title="The Timecapsule:",
##                  content="""
##		<a href="/interactive" style="text-decoration:none;">		
##		<table style="width:100%; border-radius:10px; padding:0% 0%; margins:0% 0%; background:linear-gradient(to left, rgba(255,165,0,0), rgba(255,165,0,1));">
##		<tr>
##		<td>
##		<h4 style="color:black;">
##		Go back in time to find out what the political landscape looked like at a particular date with our interactive time-enabled map.
##		</h4>
##		</td>
##		
##		<td>
##		<img style="height:100px" src="http://cdn.shopify.com/s/files/1/0297/6893/products/Rapport_Optima_Single_Time_Capsule_Watch_Winder_W193_profile_front.png?v=1445374446">
##		</td>
##		
##		</tr>
##		</table>
##		
##		</a>
##                """,
##                style="padding:0% 0%; background-size:100% 100%; background-image:url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxvPpRIf5PnwOmOqIz47XUiU99_7XhcfelMm5iiTrKbYiIoSXi)",
##                  ))

    # random check
    obj = ProvChange.objects.exclude(status="NonActive").order_by('?').first()
    typ = {'NewInfo': 'changed information to',
           'Breakaway': 'split into',
           'PartTransfer': 'tranferred territory to',
           'FullTransfer': 'merged into',
           'Begin': 'was created'}[obj.type]
    country = obj.fromcountry
    fromname = "'%s'" % obj.fromname
    toname = "'%s'" % obj.toname
    if obj.fromcountry != obj.tocountry:
        toname += ' (%s)' % obj.tocountry
    if obj.type == 'Begin':
        country = obj.tocountry
        fromname = toname
        toname = ""
    vouches = list(Vouch.objects.filter(changeid=obj.changeid, status='Active'))
    vouchicon = """
    				<div style="display:inline; color:white; border-radius:10px; padding:7px; margin:10px; height:40px">
				<a style="color:black; font-family:inherit; font-size:inherit; font-weight:bold;">
				%s
				</a>
				<img src="https://d30y9cdsu7xlg0.cloudfront.net/png/110875-200.png" height=30px />
				</div>
				""" % len(vouches)
    comments = list(Comment.objects.filter(changeid=obj.changeid, status='Active'))
    commenticon = """
		<div style="display:inline; color:white; border-radius:10px; padding:7px; margin:10px; height:40px">
		<a style="color:black; font-family:inherit; font-size:inherit; font-weight:bold;">
		%s
		</a>
		<img src="https://png.icons8.com/metro/540/comments.png" height=25px />
		</div>
				""" % len(comments)
    content = """
                <h3>{country}</h3>
                <div style="font-size:small">
                <p><b>{date}:</b> {fromname} {typ} {toname}</p>
                <p><em>(Source: {source})</em></p> 

                <a href="provchange/{pk}/view" style="background-color:rgb(7,118,183); float:right; border: 1px solid white; color:white; border-radius:10px; padding:7px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:7px; position:relative; bottom:5px">
                Check Now
                </a>
                
                <div style="">{vouchicon}{commenticon}</div>
                </div>
                """.format(date=obj.date, country=country.encode("utf8"), fromname=fromname.encode("utf8"), typ=typ, toname=toname.encode("utf8"),
                           vouchicon=vouchicon, commenticon=commenticon, pk=obj.pk, source=obj.source.encode("utf8"))

    grids.append(dict(title="Quick Check:",
                      content=content,
                      #style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="30%",
                      ))

    grids.append(dict(title="Recent Additions:",
                      content=recentadds(request),
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="63%",
                      ))

    # comments
    comments = Comment.objects.filter(status="Active").order_by("-added") # the dash reverses the order
    fields = ["added","country","title","user","text","withdraw"]
    lists = []
    for c in comments[:2]:
        rowdict = dict([(f,getattr(c, f, "")) for f in fields])
        rowdict['added'] = rowdict['added'].strftime('%Y-%M-%d %H:%M')
        if rowdict['user'] == request.user.username:
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
                                        fields=["Added","Country","Title","User","Comment",""])

    grids.append(dict(title="Recent Discussions",
                      content=content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="93%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

##def about(request):
##    return render(request, 'pshapes_site/about.html')

about_menu = """
                    <br>

                    <style>
                    li {padding-bottom:5px}
                    </style>
                    
                    <div style="text-align:left">

                        <img src="/static/pshapes pen2 transp.png" width="100%">

                        <h4>Common Questions</h4>

                        <style>
                            .blackbackground a { color:white }
                            .blackbackground a:visited { color:white }
                        </style>

                        <ul class="blackbackground">
                        <li><a href="/about/whatispshapes/">What is Pshapes?</a></li>
                        <li><a href="/about/motivation/">Motivation and Background</a></li>
                        <li><a href="/about/otherdata/">Aren't There Other Datasets?</a></li>
                        <li><a href="/about/whycrowdsourcing/">Why Crowdsourcing?</a></li>
                        <li><a href="/about/howitworks/">How Does It Work?</a></li>
                        <li><a href="/about/contact/">Contact</a></li>
                        </ul>

                    </div>
            """

about_banner = """
                        <table width="99%" style="clear:both; padding:0px; margin:0px">
                        <tr>
                        
                        <td style="width:30%; padding:1%; text-align:center; padding:10px; margin:0px; vertical-align:top">
                        {left}
                        </td>
                        
                        <td style="width:65%; padding:1%; padding:0px; padding-bottom:30px; margin:0px; vertical-align:top; text-align:center">
                        {right}
                        </td>

                        </tr>
                        </table>
                        """

about_grid = []

def about(request):
    return redirect("/about/whatispshapes")

def about_whatispshapes(request):
    grids = []
    bannertitle = ""
    bannerright = """
                    <br>
                    <h3 style="text-align:left">What is Pshapes?</h3>
                    <div style="text-align:left">
                        <p>
                        The idea behind the Pshapes project is very simple. Most databases of administrative areas avilable today
                        are simply snapshots of their boundaries on a particular date. As long as we have this,
                        as well as a chronology of changes, that should be enough to reverse or forward engineer the situation to
                        any point in the past or future. Where Pshapes contributes is in the tracking of changes
                        as well as a method for reconstructing the world's boundaries based on these changes.
                        </p>
                    </div>
                            """
    bannerleft = about_menu
    custombanner = about_banner.format(left=bannerleft, right=bannerright)
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":about_grid,"custombanner":custombanner,"bannertitle":bannertitle}
                  )

def about_motivation(request):
    grids = []
    bannertitle = ""
    bannerright = """
                    <br>
                    <h3 style="text-align:left">Motivation and Background</h3>
                    <div class="blackbackground" style="text-align:left">

                        <p>
                        The Pshapes project was first inspired by <a href="http://nils.weidmann.ws/projects/cshapes.html">the Cshapes dataset</a>, which tracks historical
                        country borders and changes since 1946. Hence, the name Pshapes to parallel the Cshapes dataset. 
                        </p>

                        <p>
                        No such historical data exists yet for subnational administrative boundaries (see "Aren't There Other Datasets?"). 
                        Sub-national administrative area and boundary data 
                        have in recent years become essential for many analysts and policy makers.
                        The data that currently exist are great for representing
                        modern or the most-recent boundaries. But subnational borders and names
                        change quite frequently, and are very different today than
                        they were even just a few years ago.
                        </p>

                        <p>
                        This makes it quite challenging for data providers to get an overview of
                        past changes or regularly come out with new updates. For good reasons,
                        existing datasets on administrative boundaries simply 
                        do not capture these historical changes and are only updated every few years.
                        </p>

                        <p>
                        Better data is needed for earlier historic periods.
                        In project afer project, geospatial data are frequently created based on information,
                        that are originally reported at the administrative level, such as government statistics.
                        These then have to be geocoded to their historical administrive areas, but using only data
                        for the modern period. This means a lot of names are no longer valid, or borders have changed
                        dramatically, requiring substantial followups to match historical units to modern boundaries.
                        </p>

                        <p>
                        The Pshapes project grew
                        out of this need for an open-source and easily maintainable dataset
                        for not only to uncover administrative units' changes for past historical periods,
                        but also to help keep track of future changes as they occur. 
                        </p>

                        <p>
                        The Pshapes project is the work of <a href="https://github.com/karimbahgat">Karim Bahgat</a> and started development in 2016,
                        but was not finalized for alpha release until late 2017. 
                        </p>
                        
                        </div>
                            """
    bannerleft = about_menu
    custombanner = about_banner.format(left=bannerleft, right=bannerright)
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":about_grid,"custombanner":custombanner,"bannertitle":bannertitle}
                  )

def about_otherdata(request):
    grids = []
    bannertitle = ""
    bannerright = """
                    <br>
                    <h3 style="text-align:left">What About Other Boundary Data?</h3>
                    <div class="blackbackground" style="text-align:left">

                                <p>
                                Although there are several administrative boundary datasets currently available,
                                researchers looking to use these for any type of longitudinal 
                                short or long term historical purpose will quickly find that these become quite limited.
                                </p>

                                <p>
                                The most similar alternative to the Pshapes dataset in terms of historical
                                changes is <a href="http://www.fao.org/geonetwork/srv/en/metadata.show?id=12691">
                                the UN's Global Administrative Units Layer (GAUL) data</a>.
                                But these data only provide yearly snapshots,
                                don't extend further back than 1990, are not publically availabe to all,
                                and its restrictive license prohibits certain uses.
                                </p>

                                <p>
                                In the public domain, possibly the most widely used dataset is <a href=
                                "http://www.gadm.org/">the Global Administrative
                                Areas (GADM) data</a>. These are provided at multiple detailed administrative levels,
                                but are only a snapshot of the latest situation. 
                                </p>

                                <p>
                                Another one that has been made available and increasingly used in recent years due to its
                                light weight and permissive license is <a href="http://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-1-states-provinces/">
                                the Natural Earth Admin-1 dataset of states and provinces.</a>
                                These data however are also just a snapshot in time, and are not frequently updated.
                                The same applies to <a href="http://quattroshapes.com/">the Quattroshapes dataset</a>, which extends the
                                Natural Earth data to include 2nd and lower-level divisions
                                </p>

                                <p>
                                Another possible source for historical administrative boundaries is
                                <a href="https://international.ipums.org/international/gis_yrspecific_1st.shtml">
                                the IPUMS GIS boundary files</a>. While these include historical changes, they only provide
                                snapshots for years in which censuses were held, the boundaries are specific to census tracts, 
                                and the files are only available for a selection of developing countries.
                                </p>

                                <p>
                                Similarly, the <a href="https://spatialdata.dhsprogram.com/boundaries/">
                                DHS survey program's Spatial Data Repository</a> has started providing historical province
                                boundary data, but only for the survey-specific sampling regions and years,
                                and limited to developing countries.
                                </p>
                        </div>
                            """
    bannerleft = about_menu
    custombanner = about_banner.format(left=bannerleft, right=bannerright)
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":about_grid,"custombanner":custombanner,"bannertitle":bannertitle}
                  )

def about_whycrowdsourcing(request):
    grids = []
    bannertitle = ""
    bannerright = """
                    <br>
                    <h3 style="text-align:left">Why Crowdsourcing?</h3>
                    <div style="text-align:left">
                                <p>
                                The Pshapes project has a very different structure than other administrative area datasets.
                                </p>

                                <p>
                                Instead of being carefully collected and coded by a handful of experts, the project has focused
                                on the speed, efficiency, and quality control of a crowdsourcing approach.
                                Due to the vast amount of work in coding all historical changes for the entire globe,
                                crowdsourcing helps spread the cost of coding and lowers the bar for contributing. 

                                <p>Such an approach is only
                                possible because it was realized that a lot of the work required to make spatially
                                integrated boundary data is wasted on duplicative and strenous work by GIS experts manually
                                repeating the same steps over and over. These repetative tasks can be automated,
                                while the information needed is actually fairly straightforward and do not require any
                                expert knowledge or skills.
                                </p>

                                <p>
                                This is why we broke these two processes apart:
                                <ul>
                                <li>Letting users and other contributors take care
                                of the data entry through the website's user-friendly interface, </li>
                                <li>while leaving the more difficult parts
                                of constructing the final dataset up to an automated algorithm with expert supervision.</li>
                                </ul>
                                </p>

                        </div>
                            """
    bannerleft = about_menu
    custombanner = about_banner.format(left=bannerleft, right=bannerright)
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":about_grid,"custombanner":custombanner,"bannertitle":bannertitle}
                  )

def about_howitworks(request):
    grids = []
    bannertitle = ""
    bannerright = """
                    <br>
                    <h3 style="text-align:left">How Does It Work?</h3>
                    <div style="text-align:left">

                            <p>
                            Since Pshapes is based on the idea of 
                            automating the more technical and repepative tasks, this means that we need a system
                            that can successfully process the user information and construct the final dataset at a later point.
                            </p>

                            <p>
                            The final dataset is created as follows:
                            </p>

                            <ol>

                                <li>
                                The system starts by asking for a
                                complete global dataset of province boundaries reflecting how the situation looks like
                                on a given (preferably recent) date. This can be any third-party dataset, including the ones listed earlier. 
                                </li>

                                <li>It then increments through the events listed in the Pshapes change-data, starting with the
                                most recent and going gradually further back in time. 
                                </li>

                                <li>
                                As the Pshapes change-events are processed in reverse chronological order, they can be boiled down to three basic types.
                                </li>

                                    <ul>

                                    <li>
                                    <b>NewInfo</b>
                                    Most changes simply involve changes to a province name or code. These events are handled
                                    by simply noting the start-date of the existing modern province, and then adding a new province
                                    that ends on that same date. Any subsequent changes involving that province will in turn result in
                                    registering its start-date, before again adding the next historical iteration of that province.
                                    <br><br>
                                    </li>

                                    <li>
                                    <b>Splits</b>
                                    If on a given date a split event was registered, this means that the current state of our boundary
                                    dataset contains all the resulting breakaway
                                    provinces and that these used to belong to a single large province. To
                                    recreate this older province all we have to do is glue together the geometries of the provinces
                                    that were registered as splitting away (incl. the remnants of the original province in case
                                    the split was incomplete).
                                    <br><br>
                                    </li>
                                    
                                    <li>
                                    <b>Transfers and Mergers</b>
                                    The last type of change include events where a province receives territory from one or
                                    more other provinces. 
                                    If the receiving province was pre-existing then we are talking about a partial transfer of
                                    territory. Since our boundary data represents the larger version of the province after it
                                    received the territory, all that is needed is to cut off the piece that was received (based on a
                                    cookie-cutter polygon that users draw when encountering such events) and glue it
                                    back together to the province that originally gave away the territory.
                                    The same principle applies if the receiving province did not previously exist but instead came
                                    into existence as a result of two or more such transfers.
                                    Finally, transfers can also involve the full transfer of entire provinces that afterwards cease to exist.
                                    These are often known as mergers or annexations, but they are handled in the same way as other transfers
                                    of territories: cut it off and give it back to its previous owner.
                                    <br><br>
                                    </li>

                                    </ul>

                                <li>
                                Multiple complex configuratios of these changes can occur in a single event,
                                and when processed in this way, the jigzaw puzzle of broken off parts and changing
                                ownerships will reorganize itself to recreate how the provinces
                                looked prior to the event.
                                </li>

                                <li>
                                Through repeating this process we can reverse geocode our
                                way back in time for as long as we have a continuous list of changes. 
                                </li>

                            </ol>

                            <p>
                            By having this automated system in place, this enables us to simplify the data collection strategy so that users
                            only code the pieces of information or parts that changed (not performing the actual modifications).
                            </p>

                            <p>
                            Doing these same iterative changes manually by hand would have 
                            required that the reference dataset be chosen in advance, essentially
                            locking in and tying down all the labor to that particular data, making it vulnerable to any particular
                            errors or reconsiderations discovered later on.
                            By focusing on replication and automation we can more efficiently 
                            harness and reuse all the work put into the collective data collection. 
                            </p>
                                
                        </div>
                            """
    bannerleft = about_menu
    custombanner = about_banner.format(left=bannerleft, right=bannerright)
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":about_grid,"custombanner":custombanner,"bannertitle":bannertitle}
                  )

def about_contact(request):
    grids = []
    bannertitle = ""
    bannerright = """
                    <br>
                    <h3 style="text-align:left">Contact</h3>
                    <div style="text-align:left">
                                <p>
                                The Pshapes framework is still in early alpha version and continually evolving.
                                As a community platform the main goal is to make it as easy and user-friendly as
                                possible. 
                                </p>
                                <p>
                                For any questions, issues, or feature requests,
                                please contact Karim Bahgat (karim.bahgat.norway@gmail.com). 
                                </p>                                

                        </div>
                            """
    bannerleft = about_menu
    custombanner = about_banner.format(left=bannerleft, right=bannerright)
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":about_grid,"custombanner":custombanner,"bannertitle":bannertitle}
                  )

def download(request):
    grids = []
    bannertitle = ""
    versiondate = ProvShape.objects.first().added
    bannerright = """
                    <br>
                    <h3 style="text-align:left">The Pshapes-Natural Earth Dataset</h3>
                    <div style="text-align:left">
                        <p>
                        Here we provide the latest historical boundary dataset that has been reverse-engineered
                        using the <a target="_blank" style="color:white;" href="http://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-1-states-provinces/">
                        <em>Natural Earth province boundaries</em></a>
                        as the starting-point. 
                        </p>
                        <p>Version: Alpha ({versiondate})</p>
                    </div>

                    <br>
                    <div style="text-align:right;">
                        <a href="/download/final/" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                        <img height=20px src="https://www.picpng.com/image/view/63838">
                        <b>Download Boundary Data</b>
                        </a>
                    </div>
                    <br>
                    """.format(versiondate=versiondate)
##    bannerleft = """
##                    <div style="text-align:center; padding:20px">
##                        <img style="width:100%" src="/static/webdownloadimg.png">
##		    </div>
##		    """
    bannerleft = """
	<script src="http://openlayers.org/api/2.13/OpenLayers.js"></script>

            <div style="width:90%; height:40vh; margins:auto; background-color:white;" id="map">
            </div>
	
	<script defer="defer">
	var map = new OpenLayers.Map('map', {allOverlays: true,
                                            resolutions: [0.5,0.6,0.7,0.8,0.9,1],
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
	var style = new OpenLayers.Style({fillColor:"rgb(62,95,146)", strokeWidth:0.1, strokeColor:'white'},
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
		map.zoomToExtent([-170,70,180,-40]);
		//map.zoomToExtent([-150,70,150,-70]);
		//map.zoomToExtent([-80,30,80,-30]);
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
	};

        $.getJSON('/api', {simplify:0.2}, renderprovs);
        
        </script>
	"""


##                                The Pshapes framework uses reverse polygon geocoding to interpret
##                                the user-contributed data and create the final historical boundary dataset.
##                                This tool is open-source and freely available to programmers,
##                                allowing users to create their own historical versions of any input province dataset.

    grids.append(dict(title="Raw Data Dump", # <img width="100%" border="2" src="http://images.wisegeek.com/physical-data.jpg">
                      content="""
                                <b>
                                The latest data dump of the user
                                contributions data is always available on-demand. This is the raw data
                                used to replicate or rebuild the pshapes dataset.

                                <div style="text-align:center">
                                <table>
                                    <tr>
                                        <td style="text-align:center"><a href="/download/raw/"><img width="50px" src="http://downloadicons.net/sites/default/files/csv-file-icon-32586.png"><p>CSV</p></a></td>
                                        <td style="text-align:center"><img width="50px" src="http://icons.iconarchive.com/icons/hopstarter/soft-scraps/256/Adobe-PDF-Document-icon.png"><p>Manual</p></td>
                                    </tr>
                                </table>
                                </div>

                                </b>
                               """,
                      width="46%",
                      ))

    grids.append(dict(title="Building Your Own", # <img width="50%"
                      content="""
                                <b>
                                <table>
                                <tr>
                                    <td>
                                    The Pshapes framework uses reverse polygon geocoding to interpret
                                    the user-contributed data and create the final historical boundary dataset.
                                    This tool is open-source and freely available to programmers,
                                    allowing users to create their own historical versions of any input province dataset.
                                    </td>

                                    <td style="text-align:center"><a href="https://github.com/karimbahgat/pshapes"><img width="50px" src="https://image.flaticon.com/icons/svg/25/25231.svg"><p>GitHub</p></a></td>

                                </table>
                                </tr>
                                </b>
                                """,
                      width="46%",
                      ))                      
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannerleft":bannerleft,"bannerright":bannerright,"bannertitle":bannertitle}
                  )

def download_final(request):
    from provshapes.views import apiview
    #request.GET = request.GET.copy()
    #request.GET['simplify'] = 0.001
    response = apiview(request)
    print type(response)
    response['Content-Disposition'] = 'attachment; filename="pshapes_natearth_final.json"'
    
##    # get geojson
##    import datetime
##    def encode(val):
##        if isinstance(val, datetime.date):
##            return val.isoformat()
##        elif val is None:
##            return None
##        else:
##            return val.encode("utf8")
##    fields = "name alterns country iso fips hasc start end".split()
##    geoj = {'type': 'FeatureCollection', 'features':[]}
##    for obj in ProvShape.objects.all():
##        geoj['features'].append({'properties':dict([(f,encode(getattr(obj, f))) for f in fields]),
##                                 'geometry':obj.geom.geojson, # json serializer creates weird backslashes, better to make manually...
##                                 })
##    # dump to json string
##    import json
##    raw = json.dumps(geoj)
    # return
    
    return response

def download_raw(request):
    from django.http import HttpResponse
    import csv, datetime
    tday = datetime.date.today()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pshapes_raw_%s.csv"' % tday 
    fields = "source status date type fromcountry fromname fromalterns fromiso fromfips fromhasc fromtype fromcapitalname fromcapital tocountry toname toalterns toiso tofips tohasc totype tocapitalname tocapital transfer_source transfer_reference transfer_geom".split()
    writer = csv.writer(response)
    writer.writerow(fields)
    def encode(val):
        if isinstance(val, datetime.date):
            return val.isoformat()
        elif "Polygon" in str(type(val)):
            return val.json
        elif val is None:
            return None
        else:
            return val.encode("utf8")
    for obj in ProvChange.objects.all():
        row = [encode(getattr(obj, f)) for f in fields]
        writer.writerow(row)
        
    return response

def testgrid(request):
    grids = tuple([("title%s"%i, "content%s"%i) for i in range(5)])
    bannertitle = "Banner Title"
    bannerleft = "Banner left"
    bannerright = "Banner right"
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

