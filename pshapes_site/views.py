"""pshapes_site

Static page views.

"""
from django.shortcuts import render, redirect
from django.template import Template,Context
from django.contrib.auth.decorators import login_required

from provchanges.models import ProvChange, Comment, Vouch, Issue, IssueComment, Map
from provshapes.models import ProvShape

shortdescr = """
Pshapes (pronounced p-shapes) is an open-source crowdsourcing project for creating and maintaining
data on historical provinces and boundaries.
The online platform makes it possible for anyone who has an interest in a particular country
to code it themselves, whether that be data-enthusiasts, historians, researchers, or country-experts.
Most of the information is already available from
our list of online sources, making it easy to jump straight into it with little or no background-knowledge.
"""

def text_formatted(text):
    import re
    val = text
    
    def repl(matchobj):
        id = matchobj.group(2)
        return '<a target="_blank" href="/viewmap/{id}/"><img height="15px" src="/static/map.png">{id}</a>'.format(id=id)
    val,n = re.subn('#(map)([0-9]*)', repl, val)
    def repl(matchobj):
        id = matchobj.group(2)
        return '<a target="_blank" href="/viewsource/{id}/"><img height="15px" src="/static/source.png">{id}</a>'.format(id=id)
    val,n = re.subn('#(source)([0-9]*)', repl, val)
    return val.encode('utf8')

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
					<td style="vertical-align:top;" class="{{ classname }}">
					{% if url %}
                                            <a href="{{ url }}">View</a>
                                        {% endif %}
					</td>
					
                                        {% for value in row %}
                                            <td style="vertical-align:top" class="{{ classname }}">{{ value | safe}}</td>
                                        {% endfor %}
					
				</tr>
			{% endfor %}
		</table>
                """
    rendered = Template(html).render(Context({"request":request, "fields":fields, "lists":lists, "classname":classname, "color":color}))
    return rendered

def recentadds(request, num=3):
    html = """
		<table style="font-size:small"> 

			<tr>
				<th> 
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
					<a href="{% url 'viewchange' pk=change.pk %}">
					<img height="30px" src="/static/typechange.png">
					</a>
					</td>

					<td>
					{{ change.added | date:"M d, Y" }}
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

    quickstartbut = """
                    <a href="/about" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
                    Read More
                    </a>
                    """
    bannerright = """
                    <br><br>
                    <h3 style="text-align:left">Crowdsourcing Historical Province Boundaries</h3>
                    <div style="text-align:left">
                        <p>{shortdescr}</p>

                        <p style="font-size:smaller"><em>Note: This is an early Alpha trial version of the website to test
                        out the data collection effort. Suggestions
                        and feature requests are welcome.</em>
                        </p>
                    </div>

                    <br>
                    <div style="text-align:right;">
                        {quickstartbut}
                    </div>
                    <br>
                    """.format(shortdescr=shortdescr, quickstartbut=quickstartbut)
    #<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYci40tiT9XecIGMtu8pLPGd7XqYXwNT_CCZ5PtyDA9ubVl0-P7g">
##    bannerleft = """
##                    <img src="/static/pshapes pen2 transp.png" width="40%">
##                    <img src="/static/webfrontimg.png" width="60%%" style="border-radius:5px">
##                    <br><br><br>
##                    """



    from provchanges.models import User
    from django.db.models import Count
    changes = ProvChange.objects.filter(status__in=["Active","Pending"]).count()
    edits = ProvChange.objects.filter(status="NonActive").count() # each edit pushes the old version into nonactive
    countrycount = ProvChange.objects.filter(status="Pending").values("fromcountry").distinct().count()
    discussions = Issue.objects.filter(changeid__isnull=True, status="Active").count()
    issues = Issue.objects.filter(changeid__isnull=False, status="Active").count()
    vouches = Vouch.objects.filter(status="Active").count()
    users = User.objects.all().count()

    mapp = """
	<script src="http://openlayers.org/api/2.13/OpenLayers.js"></script>

            <div style="width:95%; height:44vh; margins:auto; border-radius:10px; background-color:rgb(0,162,232);" id="map">
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






        function selectfunc(feature) {
            var name = feature.attributes.name;
            window.location.href = "/contribute/view/"+name;
        };
        function highlightfunc(feature) {
            //alert('hover');
            feature.style = {fillColor:"rgb(62,95,146)", strokeWidth:0.1, strokeColor:'white'}
            provLayer.redraw();
        };
        function unhighlightfunc(feature) {
            //alert('unhover');
            feature.style = {fillColor:"rgb(122,122,122)", strokeWidth:0.1, strokeColor:'white'}
            provLayer.redraw();
        };
        selectControl = new OpenLayers.Control.SelectFeature(provLayer, {onSelect: selectfunc,
                                                                        callbacks: {over:highlightfunc,
                                                                                    out:unhighlightfunc}
                                                                        } );
        map.addControl(selectControl);
        selectControl.activate();

        $.getJSON('/api', {simplify:0.2, year:2015, month:1, day:1, getlevel:0}, renderprovs);
        
        </script>
        """
    
    bannerleft = """
                <div style="margin-top:30px">
                        
                        <h2 style="text-align:center">Welcome to Pshapes</h2>
                
                        <div style="text-align:center">
                            {mapp}
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
                            Historical changes
                            </td>

                            <td>
                            <h1>{avgedits}</h1>
                            Edits per Change
                            </td>

                            <td>
                            <h1>{vouches}</h1>
                            Vouches
                            </td>
                            
                            <td>
                            <h1>{issues}</h1>
                            Issues
                            </td>

                            <td>
                            <h1>{discussions}</h1>
                            Discussions
                            </td>
                        </tr>
                        </table>
                        </b>
                </div>
                <br>
                        """.format(mapp=mapp,
                                   users=users,
                                   changes=changes,
                                   avgedits=format(edits/float(changes), '.1f'),
                                   issues=issues,
                                   discussions=discussions,
                                   vouches=vouches,
                                   countrycount=countrycount,
                                   )


    
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

##    # random check
##    obj = ProvChange.objects.exclude(status="NonActive").order_by('?').first()
##    country = obj.fromcountry
##    if obj.fromcountry != obj.tocountry:
##        tocountry = ' (%s)' % obj.tocountry
##    else:
##        tocountry = ''
##    # override special for begin
##    if obj.type == 'Begin':
##        country = obj.tocountry
##        tocountry = ''
##    # texts
##    if obj.type == 'NewInfo':
##        changetext = "'%s' changed information to '%s'%s" % (obj.fromname,obj.toname,tocountry)
##    elif obj.type == 'Breakaway':
##        changetext = "'%s'%s seceded from '%s'" % (obj.toname,tocountry,obj.fromname)
##    elif obj.type == 'SplitPart':
##        changetext = "'%s'%s was created when '%s' split apart" % (obj.toname,tocountry,obj.fromname)
##    elif obj.type == 'TransferNew':
##        changetext = "'%s' transferred territory to form part of '%s'%s" % (obj.fromname,obj.toname,tocountry)
##    elif obj.type == 'MergeNew':
##        changetext = "'%s' merged to form part of '%s'%s" % (obj.fromname,obj.toname,tocountry)
##    elif obj.type == 'TransferExisting':
##        changetext = "'%s' transferred territory to '%s'%s" % (obj.fromname,obj.toname,tocountry)
##    elif obj.type == 'MergeExisting':
##        changetext = "'%s' merged into '%s'%s" % (obj.fromname,obj.toname,tocountry)
##    elif obj.type == 'Begin':
##        changetext = "'%s' was created" % obj.toname
##
##    # OLD, to be deprecated
##    elif obj.type == 'PartTransfer':
##        changetext = "'%s' transferred territory to '%s'%s" % (obj.fromname,obj.toname,tocountry)
##    elif obj.type == 'FullTransfer':
##        changetext = "'%s' merged into '%s'%s" % (obj.fromname,obj.toname,tocountry)
##
##    
##    vouches = list(Vouch.objects.filter(changeid=obj.changeid, status='Active'))
##    vouchicon = """
##    				<div style="display:inline; color:white; border-radius:10px; padding:7px; margin:10px; height:40px">
##				<a style="color:black; font-family:inherit; font-size:inherit; font-weight:bold;">
##				%s
##				</a>
##				<img src="/static/vouch.png" height=30px />
##				</div>
##				""" % len(vouches)
##    issues = Issue.objects.filter(changeid=obj.changeid, status='Active').count()
##    issueicon = """
##		<div style="display:inline; color:white; border-radius:10px; padding:7px; margin:10px; height:40px">
##		<a style="color:black; font-family:inherit; font-size:inherit; font-weight:bold;">
##		%s
##		</a>
##		<img src="/static/issue.png" height=25px />
##		</div>
##				""" % issues
##    content = """
##                <h3>{country}</h3>
##                <div style="font-size:small">
##                <p><b>{date}:</b> {changetext}</p>
##                <p><em>(Source: {source})</em></p> 
##
##                <a href="provchange/{pk}/view" style="background-color:rgb(7,118,183); float:right; color:white; border-radius:10px; padding:7px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:7px; position:relative; bottom:5px">
##                Check Now
##                </a>
##                
##                <div style="">{vouchicon}{issueicon}</div>
##                </div>
##                """.format(date=obj.date, country=country.encode("utf8"), changetext=changetext.encode("utf8"),
##                           vouchicon=vouchicon, issueicon=issueicon, pk=obj.pk, source=text_formatted(obj.source))
##
##    grids.append(dict(title="Quality Check:",
##                      content=content,
##                      style="background-color:orange; border-radius:0",
##                      #style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                      width="30%",
##                      ))



    # random prov
    query = ProvShape.objects.raw('''SELECT id, ST_AsSVG(geom) as svg, name, country, start, "end"
                                    FROM provshapes_provshape
                                    WHERE simplify=0.025
                                    ORDER BY random()
                                    ''')
    obj = next(iter(query), None)
    if obj:
        # TODO: not very effective since we parse and calculate bbox from the SVG string, because the coordinates in ST_AsSVG() are not the same as the real coords and bbox
        svg = obj.svg
        multis = svg.replace(' Z', '').split('M ')
        flat = [float(v) for mult in multis for v in mult.replace('L ','').strip().split()]
        xs,ys = flat[0::2],flat[1::2]
        bbox = min(xs),min(ys),max(xs),max(ys)
        xmin,ymin,xmax,ymax = bbox
        w,h = xmax-xmin,ymax-ymin
        viewbox = '%s %s %s %s' % (xmin,ymin,w,h)
        #print obj.country,obj.name,bbox,viewbox
        icon = '<svg height="100px" viewBox="{viewbox}" preserveAspectRatio="xMidYMid meet"><path d="{path}" /></svg>'.format(path=svg, viewbox=viewbox)
    else:
        icon = ""

    content = """
                <h3>{name}, {country}</h3>
                <div style="text-align:center">
                    <a href="/viewprov?country={country}&name={name}&date={date}">
                    {icon}
                    </a>
                </div>
                
                <div style="font-size:small; margin-bottom:10px">
                    <p><b>{name}</b> was a province that existed in <b>{country}</b>
                    from <b>{start}</b> to <b>{end}</b>
                    </p>

                    <a href="/viewprov?country={country}&name={name}&date={date}" style="background-color:rgb(7,118,183); color:white; border-radius:10px; padding:7px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:7px">
                    View
                    </a>
                </div>
                """.format(country=obj.country.encode("utf8"), name=obj.name.encode("utf8"),
                           icon=icon, date=obj.start,
                           start=obj.start.year, end=obj.end.year)

    grids.append(dict(title="Featured Province:",
                      content=content,
                      style="background-color:orange; border-radius:0",
                      #style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="30%",
                      ))


    # recent changes
    changelist = ProvChange.objects.all().order_by("-added")   # the dash reverses the order
    fields = ["","Added","Country","Name","Type"]
    lists = []
    for o in changelist[:6]:
        link = "/provchange/%s/view" % o.pk
        linkimg = '<a href="%s"><img style="opacity:0.9" src="/static/typechange.png" height="25px"></a>' % link
        row = [linkimg, o.added.strftime('%b %#d, %Y'), o.fromcountry.encode('utf8'), o.fromname.encode('utf8'), o.type]
        lists.append((None,row))
        
    content = lists2table(request, lists=lists, fields=fields,
                          classname="recentadds", color='orange')
    grids.append(dict(title="Recent Additions:",
                      content='<div style="font-size:small">%s</div>' % content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="63%",
                      ))

    # comments
    issues = Issue.objects.filter(status="Active").order_by("-added") # the dash reverses the order
    comments = IssueComment.objects.filter(status="Active").order_by("-added") # the dash reverses the order
    objects = sorted(list(issues[:3]) + list(comments[:3]),
                     key=lambda d: d.added, reverse=True)
    fields = ["added","country","title","text"]
    lists = []
    for o in objects[:3]:
        if isinstance(o, Issue):
            pk = o.pk
            rowdict = dict(added=o.added, user=o.user, text=o.text,
                           country=o.country, title=o.title)
        elif isinstance(o, IssueComment):
            pk = o.issue.pk
            rowdict = dict(added=o.added, user=o.user, text=o.text,
                           country=o.issue.country, title=o.issue.title)
        rowdict['added'] = rowdict['added'].strftime('%b %#d, %Y')
        rowdict['text'] = text_formatted(rowdict['text'][:300]+'...' if len(rowdict['text']) > 300 else rowdict['text'])
        rowdict['country'] = rowdict['country'].encode('utf8')
        link = "/viewissue/%s" % pk
        linkimg = '<a href="%s"><img style="opacity:0.9" src="/static/comment.png" height="30px"></a>' % link
        row = [linkimg] + [rowdict[f] for f in fields]
        lists.append((None,row))
        
    content = lists2table(request, lists=lists, fields=["","Added","Country","Title","Comment"],
                          classname="recentcomments", color='rgb(27,138,204)')

    grids.append(dict(title="Recent Discussions:",
                      content='<div style="font-size:small">%s</div>' % content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="93%",
                      ))

    # maps
    maps = Map.objects.filter(status="Active").order_by("-added") # the dash reverses the order
    objects = maps
    fields = ["added","country","title","note"]
    lists = []
    for o in objects[:3]:
        pk = o.pk
        rowdict = dict([(f,getattr(o, f)) for f in fields])
        rowdict['added'] = rowdict['added'].strftime('%b %#d, %Y')
        rowdict['note'] = text_formatted(rowdict['note'][:300]+'...' if len(rowdict['note']) > 300 else rowdict['note'])
        rowdict['country'] = '; '.join(rowdict['country'].encode('utf8').split('|'))[:40]
        if len(rowdict['country']) >= 40: rowdict['country'] += '...'
        link = "/viewmap/%s" % pk
        linkimg = '<a href="%s"><img style="opacity:0.8" src="/static/map.png" height="30px"></a>' % link
        row = [linkimg] + [rowdict[f] for f in fields]
        lists.append((None,row))
        
    content = lists2table(request, lists=lists, fields=["","Added","Country","Title","Note"],
                          classname="recentmaps", color='rgb(58,177,73)')

    grids.append(dict(title="<br>Recent Maps:",
                      content='<div style="font-size:small">%s</div>' % content,
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      width="93%",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

##def about(request):
##    return render(request, 'pshapes_site/about.html')

about_menu = """
                    <style>
                    li {padding-bottom:5px}
                    </style>
                    
                    <div style="text-align:left; padding-top:10px">

                        <h2>About the Pshapes Project</h2>

                        <div style="width:100%; text-align:left">
                            <img style="padding-left:20px" src="/static/webfrontimg.png" width="80%">
                        </div>

                        <div style="padding-left:20px">
                            <h4>Introduction</h4>

                            <style>
                                .blackbackground a { color:white }
                                .blackbackground a:visited { color:white }
                            </style>

                            <ul class="blackbackground">
                            <li><a href="/about/motivation/">Motivation and Background</a></li>
                            <li><a href="/about/otherdata/">Aren't There Other Datasets?</a></li>
                            <li><a href="/about/whycrowdsourcing/">Why Crowdsourcing?</a></li>
                            <li><a href="/about/nextsteps/">Next Steps</a></li>
                            </ul>

                            <h4 class="blackbackground"><a href="/about/tutorial/">Coding Historical Changes</a></h4>

                            <ul class="blackbackground">
                            <li><a href="/about/tutorial/#sources">Sources of information</a></li>
                            <li><a href="/about/tutorial/#levels">Administrative levels</a></li>
                            <li><a href="/about/tutorial/#events">Adding events</a></li>
                            <li><a href="/about/tutorial/#georeferencing">Georeferencing maps</a></li>
                            <li><a href="/about/tutorial/#exclude">What to include or exclude</a></li>
                            <li><a href="/about/tutorial/#betweencountries">Changes between countries</a></li>
                            <li><a href="/about/tutorial/#definecountry">How to define a country</a></li>
                            <li><a href="/about/tutorial/#finishing">Finishing up</a></li>
                            </ul>
                        </div>

                    </div>
            """

about_banner = """
                        <table width="99%" style="clear:both; padding:0px; margin:0px">
                        <tr>
                        
                        <td style="width:45%; padding:1%; text-align:center; padding:10px; margin:0px; vertical-align:top">
                        {left}
                        </td>
                        
                        <td style="width:45%; padding:1%; padding:0px; padding-bottom:30px; margin:0px; vertical-align:top; text-align:center">
                        <br>
                        {right}
                        </td>

                        </tr>
                        </table>
                        """

about_grid = []

def about(request):
    return redirect("/about/motivation")

def about_motivation(request):
    grids = []
    bannertitle = ""
    bannerright = """
                    <br><br><br>
                    <h3 style="text-align:left">Motivation and Background</h3>
                    <div class="blackbackground" style="text-align:left">

                        <p>
                        Most databases of administrative areas avilable today
                        are simply snapshots of their boundaries on a particular date.
                        These are frequently used by researchers, analysts, and policy makers to
                        geocode or visualize information originally reported at the administrative
                        level, such as government statistics, surveys, NGO reports, and historical documents.
                        </p>

                        <p>
                        But problems arise because administrative units change quite frequently,
                        so even if looking at just the last few years, a lot of names will no longer be valid
                        or their borders adjusted,
                        requiring substantial followups to match historical units to modern boundaries.
                        </p>

                        <p>
                        So why is there <a href="/about/otherdata/">no historical data yet for subnational administrative boundaries?</a>
                        It has already been done at the country-level. The <a href="http://nils.weidmann.ws/projects/cshapes.html">Cshapes dataset</a> tracks historical
                        country borders and changes since 1946. It records these changes as a series of lifetimes, with a separate row and geometry for each time the country changes.
                        The Pshapes project attempts to do for provinces what Cshapes has done for countries, hence, the name "Pshapes".
                        </p>

                        <p>
                        It turns out the transient nature of sub-national administrative units makes it quite challenging for data providers to get an overview of
                        province-level changes or regularly come out with new updates. It is for good reasons that
                        existing datasets on administrative boundaries simply 
                        do not capture these historical changes and are only updated every few years.
                        </p>

                        <p>
                        But one website in particular, <a href="http://www.statoids.com/">Statoids.com</a>, has shown that tracking the changes of administrative units is
                        indeed possible, and has already done much of the work. So as long as we have the modern boundaries, as well as a chronology
                        of changes, that should be enough to reverse or forward engineer the situation to any point in the past or future.
                        </p>

                        <p>
                        The other major hurdle in collecting historical boundary data is that boundary data
                        usually involve highly technical tasks and require dedicated geospatial software and skills.
                        The specialized nature of this approach makes it less than ideal for coding the vast number of historical changes
                        at the global level.
                        </p>

                        <p>
                        Pshapes grew
                        out of this need for an open-source, low-cost, and easily maintainable dataset
                        for coding historical changes of global administrative units.
                        </p>

                        <p>
                        The Pshapes concept, website, and database is the work of <a href="https://github.com/karimbahgat">Karim Bahgat</a> and started as an idea in 2016,
                        but after much testing was not finalized for alpha release until early 2018. 
                        </p>

                        <br>
                        <hr>
                        
                        <p style="font-style:italic; margin-left:10px">
                        * Sadly, it appears that the Statoids website, one of the main sources for historical province changes,
                        <a href="http://www.statoids.com/mgtletter.html">will not be updated as frequently as before</a>.
                        Hopefully, Pshapes can build on and continue the great work, vision, and legacy of the author of that website,
                        Gwilliam Law. 
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
                    <br><br><br>
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
                    <br><br><br>
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

                                <p>All possible province changes can be categorized into a handful of change types.
                                Provinces can change information such as their name, capital, or administrative codes.
                                Provinces can dissolve into several new ones or experience a secession. 
                                New provinces can be formed by taking all or parts of territories from multiple provinces.
                                Existing provinces can adjust the boundary between them. 
                                </p>

                                <p>
                                Provided we know what the provinces look like today and have the sequence and types of changes over time,
                                it is possible to automate the necessary
                                geospatial operations that a human coder would usually do, clipping apart or gluing together
                                geometries. 
                                </p>

                                <p>
                                The starting point can be any third-party global dataset of province boundaries reflecting how the situation looks like
                                on a given (preferably recent) date. 
                                The system would increment through the events listed in the change-data, starting with the
                                most recent and going gradually further back in time. 
                                </p>

                                <p>
                                Multiple complex configuratios of these changes can occur in a single event,
                                and when processed in this way, the jigzaw puzzle of broken off parts and changing
                                ownerships will reorganize itself to recreate how the provinces
                                looked prior to the event.
                                </p>

                                <p>
                                Doing these same iterative changes manually by hand would have 
                                required that the reference dataset be chosen in advance, essentially
                                locking in and tying down all the labor to that particular data, making it vulnerable to any particular
                                errors or reconsiderations discovered later on.
                                By focusing on replication and automation we can more efficiently 
                                harness and reuse all the work put into the collective data collection. 
                                </p>

                                <p>
                                By having this automated system in place, this enables us to simplify the data collection strategy so that users
                                only code the pieces of information or parts that changed (not performing the more time-consuming modifications).
                                </p>

                        </div>
                            """
    bannerleft = about_menu
    custombanner = about_banner.format(left=bannerleft, right=bannerright)
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":about_grid,"custombanner":custombanner,"bannertitle":bannertitle}
                  )

from provchanges.views import map_resources

def about_tutorial(request):
    grids = []
    bannertitle = ""
    bannerright = """
                    <br><br><br>
                    <h3 style="text-align:left">Coding Historical Changes</h3>
                    <div class="blackbackground" style="text-align:left">

                                <p>
                                If you are looking to code new countries and historical changes to Pshapes, this page will walk you through the process on how to get started. 
                                </p>

                                <h4 id="sources">Sources of Information</h4>
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
                                <p>Some recommended sources:</p>
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

                                    <li>
                                    <a target="_blank" href="http://www.worldstatesmen.org/">World Statesmen website</a>
                                    </li>
                                </ul>
                                </p>
                                
                                <h4 id="levels">Administrative Levels</h4>
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
                                
                                <h4 id="events">Adding Events</h4>
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
                                
                                <h4 id="georeferencing">Georeferencing Maps</h4>
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
                                <p>Some recommended map sources:</p>
                                <ul>
                                """ + map_resources + """
                                </ul>
                                </p>
                                
                                <h4 id="exclude">What to do Include or Exclude</h4>
                                <p>
                                In some cases, transfers of territory may be listed with the names of lower-level areas, and these should just be
                                listed as partial territorial transfers and drawn roughly by hand.
                                </p>
                                <p>
                                However, if the change seems very small,
                                or if there are too many of these types of minor changes, it is okay to ignore most of them and only focus on
                                the big changes.
                                </p>
                                
                                <h4 id="betweencountries">Changes Between Countries</h4>
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
                                
                                <h4 id="definecountry">How To Define a Country</h4>
                                <p>
                                It might not always be clear what constitutes a country. At all times follow what seems to have been the most
                                widely used country-units and names. For instance, overseas territories and dependencies which have their own
                                ISO country codes should be considered as separate countries. 
                                </p>
                                <p>
                                For historical territories under foreign colonial rule, these should be
                                coded as separate from the ruling power. For countries simply achieving independence or countries with only minor
                                changes in their official name, avoid changing the country name.
                                </p>
                                
                                <h4 id="finishing">Finishing Up</h4>
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
                            """
    bannerleft = about_menu
    custombanner = about_banner.format(left=bannerleft, right=bannerright)
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":about_grid,"custombanner":custombanner,"bannertitle":bannertitle}
                  )


def about_nextsteps(request):
    grids = []
    bannertitle = ""
    bannerright = """
                    <br><br><br>
                    <h3 style="text-align:left">Next Steps</h3>
                    <div style="text-align:left">
                                <p>
                                The Pshapes framework is still in early alpha version and continually evolving.
                                </p>
                                <p>
                                The current stage will focus on piloting the data collection effort,
                                getting feedback from users, and establishing proof-of-concept.
                                Sources for funding are also currently being sought, to help maintain, 
                                improve, and add new features to the platform. 
                                </p>
                                <p>
                                As a community platform the main goal is to make it as easy and user-friendly as
                                possible. It is therefore dependent on the questions, issues, and feature requests of
                                the contributors, so please do not hesitate to contact.
                                </p>
                                <br>
                                <p>
                                Karim Bahgat
                                </p>
                                <p>
                                karim.bahgat.norway@gmail.com
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

    downloadlist = [
                    [
                     '''<img height=50px src="http://www.seismicportal.eu/images/json_file.png">''',
                     '<a style="color:white" class="blackbackground" href="/download/final/">Provinces</a>',
                     'The main dataset of historical province boundaries',
                     ],
                    [
                     '''<img height="50px" src="http://downloadicons.net/sites/default/files/csv-file-icon-32586.png">''',
                     '<a style="color:white" href="/download/raw/">Raw Change Data</a>',
                     'The latest data dump of the user contributions data is always available on-demand. This is the raw data used to replicate or rebuild the pshapes dataset.',
                     ],
                    [
                     '''<img height="50px" src="http://icons.iconarchive.com/icons/hopstarter/soft-scraps/256/Adobe-PDF-Document-icon.png">''',
                     'Provinces (Codebook)',
                     'Codebook describing the main historical province data.',
                     ],
                    [
                     '''<img height="50px" src="http://icons.iconarchive.com/icons/hopstarter/soft-scraps/256/Adobe-PDF-Document-icon.png">''',
                     'Raw Change Data (Codebook)',
                     'Codebook describing the latest data dump of the user contributions data.',
                     ],
                    [
                     '''<img style="filter:invert(100)" height="50px" src="https://image.flaticon.com/icons/svg/25/25231.svg">''',
                     '<a style="color:white" href="https://github.com/karimbahgat/pshapes">Replication Code</a>',
                     '''            The Pshapes framework uses reverse polygon change-tracking to interpret
                                    the user-contributed data and create the final historical boundary dataset.
                                    This tool is open-source and freely available to programmers,
                                    allowing users to create their own historical versions of any input province dataset.
                                    ''',
                     ],
                    ]

    bannerright = '<br><br><br><h3 style="text-align:left">Main data downloads:</h3><table style="border-spacing:10px">%s</table>' \
                  % ''.join(['<tr>%s</tr>' % ''.join(['<td style="text-align:left; vertical-align:top">%s</td>' % v for v in row])
                             for row in downloadlist])
##    bannerleft = """
##                    <div style="text-align:center; padding:20px">
##                        <img style="width:100%" src="/static/webdownloadimg.png">
##		    </div>
##		    """
    bannerleft = """
                
                <h2 style="padding-top:10px; text-align:left">The Pshapes-Natural Earth Dataset</h2>
                    <div style="width:100%; text-align:left">
                        <img style="padding-left:20px" src="/static/webfrontimg.png" width="80%">
                    </div>
                    <div style="text-align:left; clear:both">
                        <p>
                        Here we provide the latest historical boundary dataset that has been reverse-engineered
                        using the <a target="_blank" style="color:white;" href="http://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-1-states-provinces/">
                        <em>Natural Earth province boundaries</em></a>
                        as the starting-point. 
                        </p>
                    </div>
                    <div style="text-align:left; margin-left:10px">
                        <p>Version: Alpha ({versiondate})</p>
                        <p>
                        License: Non-commercial use and attribution (<a target="_blank" style="color:white;" href="https://creativecommons.org/licenses/by-nc/3.0/">CC BY-NC 3.0</a>). 
                        </p>
                        <p>If you use these data, please cite:
                            <ul>
                                <li><em>
                                Bahgat, Karim (YEAR). Pshapes Database of Historical Province Boundaries, version [VERSION]. Available at www.pshapes.org. Accessed [DATE ACCESSED]. 
                                </em></li>
                            </ul>
                        </p>
                    </div>
                """.format(versiondate=versiondate)

    grids = []
    lists = [       ['''<a href="/download/countries/">
                            <img height=50px src="http://www.seismicportal.eu/images/json_file.png">
                        </a>''',
                     'Countries',
                     '''Historical country boundaries derived from the Pshapes-Natural Earth province data.
                        For now, boundaries only, no country metadata.''',
                     ],
                    ['''<a>
                            <img height=50px src="http://downloadicons.net/sites/default/files/csv-file-icon-32586.png">
                        </a>''',
                     'Historical Gazetteer (TBA)',
                     """Gazetteer of worldwide place names from the GeoNames dataset, where the
                         administrative unit of each place is historically correct based on the Pshapes boundaries.
                         Useful for historical placename geocoding, since duplicate placenames often requires matching both the name
                         of the place and the name of the administrative division (which can change over time).
                         [To be added in the future / Not yet available].""",
                     ],
            ]
    lists = [(None,r) for r in lists]
                    
    content = lists2table(request, lists, ['', 'File', 'Description'])
    grids.append(dict(title="Additional Data Products:",
                      content=content,
                      width="96%",
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
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

def download_countries(request):
    from provshapes.views import apiview
    request.GET = request.GET.copy()
    request.GET['getlevel'] = 0
    response = apiview(request)
    print type(response)
    response['Content-Disposition'] = 'attachment; filename="pshapes_natearth_countries.json"'    
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

