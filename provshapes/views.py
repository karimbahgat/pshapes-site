from django.shortcuts import render, get_object_or_404, redirect
from django.template import Template,Context
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied

# Create your views here.

from django.contrib.gis import forms
from django.contrib.gis.geos import Polygon, MultiPolygon

from .models import ProvShape

from rest_framework import response
from rest_framework import decorators

import urllib2
import json
import datetime
import threading

def update_dataset(request):
    if request.user.is_staff:
        print 'getting data...'
        raw = request.FILES['file'].read()
        def work():
            print 'deleting existing...'
            ProvShape.objects.all().delete()
            print 'parsing json...'
            #raw = open(request.FILES['file'].temporary_file_path().replace('\\','/'), 'rb').read() #urllib2.urlopen('https://github.com/karimbahgat/pshapes/raw/master/processed.geojson').read()
            datadict = json.loads(raw)
            print 'adding', datadict.keys(), len(datadict['features'])
            for feat in datadict['features']:
                props = feat['properties']
                if not props['start'] or props['start']=='None':
                    print 'missing start date, not adding:', props
                    continue
                values = dict(name=props['name'],
                              alterns='|'.join(props['alterns']),
                              country=props['country'],
                              iso=props['iso'],
                              fips=props['fips'],
                              hasc=props['hasc'],
                              start=props['start'],
                              end=props['end'],
                              )
                print values
    ##            values = dict()
    ##            for fl in ProvShape._meta.fields:
    ##                flname = fl.name
    ##                print flname
    ##                if flname == 'id':
    ##                    continue
    ##                values[flname] = feat[flname]
                if feat['geometry']['type'] == 'Polygon':
                    polys = [Polygon(*feat['geometry']['coordinates'])]
                elif feat['geometry']['type'] == 'MultiPolygon':
                    polys = [Polygon(*poly) for poly in feat['geometry']['coordinates']]
                else:
                    raise Exception('Geometry must be polygon or multipolygon, not %s' % feat['geometry']['type'])
                #print str(polys)[:100]
                geom = MultiPolygon(*polys)

                for tolerance in [0.2,0.1,0.05,0.025,0]:
                    _geom = geom.simplify(tolerance, preserve_topology=True)
                    if _geom.geom_type == 'Polygon':
                        _geom = MultiPolygon([_geom])
                    values['simplify'] = tolerance
                    values['geom'] = _geom
                    values['geoj'] = _geom.geojson
                    provshape = ProvShape(**values)
                    provshape.save()
                
            print 'provshapes updated!'
            
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
        print 'updating provshapes, thread started, this may take a while'
        return redirect(request.META['HTTP_REFERER'])
        
    else:
        print 'You do not have permission to update the provshapes dataset'
        raise PermissionDenied

@decorators.api_view(["GET"])
def apiview(request):
    print request.query_params
    print "------"
    queryset = ProvShape.objects.all()

    params = dict(((k,v) for k,v in request.query_params.items() if v))

    frmt = params.pop('format', None)

    # speed and size optimization for geometries
    # main bottleneck is creating geojson from geometry object
    # solving this by fetching precomputed and/or pre-simplified geojson strings
    tolerance = float(params.pop('simplify', 0))
    print 'simplify',tolerance
    if not tolerance in [0.2,0.1,0.05,0.025,0]:
        raise Exception('simplify parameter must be one of %s' % [0.2,0.1,0.05,0.025,0])
    queryset = queryset.filter(simplify=tolerance)

    # date filter
    yr = params.pop('year', None)
    mn = params.pop('month', None)
    dy = params.pop('day', None)
    
    if all((yr,mn,dy)):
        print 'filtering date'
        date = datetime.date(int(yr),int(mn),int(dy))
        queryset = queryset.filter(start__lte=date).filter(end__gte=date)

    # bbox filter
    bbox = params.pop('bbox', None)
    if bbox:
        bbox = map(float, bbox.split(','))
        print bbox
        box = Polygon.from_bbox(bbox)
        queryset = queryset.filter(geom__bboverlaps=box)

    # attribute filtering
    print 'apiparams',params
    # special name search
    if 'name' in params:
        queryset = queryset.filter(name__icontains=params['name']) | queryset.filter(alterns__icontains=params['name'])
    # add remaining conditions
    restdict = dict(((k,v) for k,v in params.items() if k!='name'))
    if restdict:
        queryset = queryset.filter(**restdict)

    import time
    t=time.time()

    # convert to json
    fields = ['geoj','name','alterns','country','iso','fips','hasc','start','end']
        
    jsondict = dict(type='FeatureCollection', features=[])
    for props in queryset.values(*fields):        
        props['start'] = props['start'].isoformat()
        props['end'] = props['end'].isoformat()

        geojstring = props.pop('geoj')
        geoj = json.loads(geojstring)

        # NOTE: wkt or hex is way faster than real-time geojson (ca 75%)
        # TODO: maybe consider using that in future...
        #geoj = geom.wkt #.hex

        #print str(geoj)[:200]
        fdict = dict(type='Feature', properties=props, geometry=geoj)
        jsondict['features'].append(fdict)

##    from django.core.serializers import serialize
##    jsondict = serialize('geojson', queryset,
##                          geometry_field='geom',
##                          #fields=('name',))
##                         )
        
    print time.time()-t
    
##    # to raw string
##    raw = json.dumps(jsondict)
##    print time.time()-t
##    from django.http import HttpResponse
##    response = HttpResponse(content_type='application/json')
##    response.write(raw)
##    print time.time()-t

    # alternative json response
    from django.http import JsonResponse
    response = JsonResponse(jsondict)
    print time.time()-t
    
    return response
    #return response.Response(jsondict)

class SearchForm(forms.ModelForm):

    class Meta:
        model = ProvShape
        fields = ["name","country"]
        widgets = dict(country=forms.Select(attrs={'onchange':'submitsearch()'},
                                            choices=[("","")]+[(c.country,c.country) for c in ProvShape.objects.distinct('country')]))

def explore(request):

    ###
    
    #mapp = render_to_string("provshapes/mapview.html")

    initdict = dict(request.GET.items()) if request.GET else {}
    searchform = SearchForm(initial=initdict)

##    bannerright = """
##    <h3 style="color:white; text-align:left;">
##    Historical Provinces
##    </h3>
##    <div style="text-align:left">
##        <p>
##        Here you can search, browse, and view a map of all historical provinces that have been coded so far.
##        </p>
##    </div>
##    """


    # main area with table and map
    provs = ProvShape.objects.all().order_by("country", "name", "start")
    if request.GET:
        #filterdict = dict(((k,v) for k,v in request.GET.items() if v))
        #provs = provs.filter(**filterdict)
        filterdict = dict(((k,v) for k,v in request.GET.items() if v))
        # special name search
        if 'name' in request.GET and request.GET['name']:
            provs = provs.filter(name__icontains=request.GET['name']) | provs.filter(alterns__icontains=request.GET['name'])
        # add remaining conditions
        restdict = dict(((k,v) for k,v in filterdict.items() if k!='name'))
        if restdict:
            provs = provs.filter(**restdict)
    else:
        filterdict = dict()

    custombanner = render(request, 'provshapes/mapview.html',
                          dict(getparams=json.dumps(filterdict), searchform=searchform),
                          ).content
    

    grids = []

##    content = """
##    <a class="toptabs" onClick="document.getElementById('maptab').style.display = 'none'; document.getElementById('listtab').style.display = '';">
##    List
##    </a>
##    """
##    
##    grids.append(dict(title="",
##                     content=content,
##                      style="text-align:center; font-size:large; font-weight:bold",
##                     width="10%",
##                     ))
##
##
##    content = """
##    <a class="toptabs" onClick="document.getElementById('maptab').style.display = ''; document.getElementById('listtab').style.display = 'none';">
##    Map
##    </a>
##    """
##    
##    grids.append(dict(title="",
##                     content=content,
##                      style="text-align:center; font-size:large; font-weight:bold",
##                     width="10%",
##                     ))



##    # add prov table for each country
##    for c in provs.distinct('country')[:2]: # limit to 5 countries for faster loading
##
##        fields = ["name","alterns","start","end"]
##        lists = []
##        for p in provs.filter(country=c.country):
##            rowdict = dict([(f,getattr(p, f, "")) for f in fields])
##            row = [rowdict[f] for f in fields]
##            lists.append(("[Link]",row))
##
##        listtable = lists2table(request, lists, fields)
##        
##        grids.append(dict(title=c.country,
##                         content=listtable,
##                         style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
##                         width="100%",
##                         ))

    fields = ["name","alterns","country","start","end"]
    lists = []
    for p in provs[:50]:
        rowdict = dict([(f,getattr(p, f, "")) for f in fields])
        row = [rowdict[f] for f in fields]
        lists.append(("[Link]",row))

    listtable = lists2table(request, lists, fields)
    
    grids.append(dict(title="Results (first 50 only)",#"Results (showing %s of %s):" % (min(len(provs),50), len(provs)),
                     content=listtable,
                     style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                     width="100%",
                     ))

##    content = """
##    <div id="provframe">
##    None selected
##    </div>
##    
##    <script>
##    function selectfunc(feature) {
##        alterns = feature.attributes.Alterns.join("; ");
##        if (alterns) {
##            alterns = " (" + alterns + ")";
##        };
##        table = "<table>"
##            table += "<tr>"
##            table += "<td>Country: </td>"
##            table += "<td>" + feature.attributes.country + "</td>"
##            table += "</tr>"
##            
##            table += "<tr>"
##            table += "<td>Name: </td>"
##            table += "<td>" + feature.attributes.Name + alterns + "</td>"
##            table += "</tr>"
##            
##            table += "<tr>"
##            table += "<td>Time period: </td>"
##            table += "<td>" + feature.attributes.start + " to " + feature.attributes.end + "</td>"
##            table += "</tr>"
##
##            table += "<tr>"
##            table += "<td>Codes: </td>"
##            table += "<td>ISO=" + feature.attributes.ISO + ", FIPS=" + feature.attributes.FIPS + ", HASC=" + feature.attributes.HASC + "</td>"
##            table += "</tr>"
##        table += "</table>"
##        document.getElementById("provframe").innerHTML = table;
##    };
##    function unselectfunc(feature) {
##        document.getElementById("provframe").innerHTML = "None selected";
##    };
##    selectControl = new OpenLayers.Control.SelectFeature(provLayer, {onSelect: selectfunc, onUnselect: unselectfunc, selectStyle: {fillColor: "turquoise", strokeWidth: 2}});
##    map.addControl(selectControl);
##    selectControl.activate();
##    </script>
##    """

    return render(request, 'pshapes_site/base_grid.html', dict(custombanner=custombanner,
                                                               grids=grids)
                  )

def underconstruction(request):
    grids = []
    bannertitle = "Under construction..."
    bannerleft = "This page is currently under construction"
    bannerright = ""
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

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




