from django.shortcuts import render, get_object_or_404, redirect
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

def update_dataset(request):
    if 1: #'user.administrator' in request.user.get_all_permissions():
        print 'deleting existing...'
        ProvShape.objects.all().delete()
        print 'downloading...'
        raw = urllib2.urlopen('https://github.com/karimbahgat/pshapes/raw/master/processed.geojson').read()
        datadict = json.loads(raw)
        print 'adding', datadict.keys(), len(datadict['features'])
        for feat in datadict['features']:
            props = feat['properties']
            values = dict(name=props['Name'],
                          alterns='|'.join(props['Alterns']),
                          country=props['country'],
                          iso=props['ISO'],
                          fips=props['FIPS'],
                          hasc=props['HASC'],
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
            values['geom'] = MultiPolygon(*polys)
            provshape = ProvShape(**values)
            provshape.save()
        print 'provshapes updated!'
        return redirect(request.META['HTTP_REFERER'])
        
    else:
        print 'You do not have permission to update the provshapes dataset'
        raise PermissionDenied

@decorators.api_view(["GET"])
def apiview(request):
    print request.query_params
    print "------"
    queryset = ProvShape.objects.all()

    params = dict(request.query_params.items())

    frmt = params.pop('format', None)
    
    yr = params.pop('year', None)
    mn = params.pop('month', None)
    dy = params.pop('day', None)
    
    if all((yr,mn,dy)):
        print 'filtering date'
        date = datetime.date(int(yr),int(mn),int(dy))
        queryset = queryset.filter(start__lte=date).filter(end__gte=date)

    bbox = params.pop('bbox', None)
    if bbox:
        bbox = map(float, bbox.split(','))
        print bbox
        box = Polygon.from_bbox(bbox)
        queryset = queryset.filter(geom__intersects=box)

    tolerance = params.pop('simplify', None)
    print 'simplify',tolerance

    # attribute filtering
    print 'apiparams',params
    if params:
        queryset = queryset.filter(**params)

    # convert to json
    jsondict = dict(type='FeatureCollection', features=[])
    for obj,props in zip(queryset, queryset.values('name','alterns','country','iso','fips','hasc','start','end')):
        geom = obj.geom
        if tolerance:
            geom = geom.simplify(float(tolerance))
        geoj = json.loads(geom.geojson)
        #print str(geoj)[:200]
        fdict = dict(type='Feature', properties=props, geometry=geoj)
        jsondict['features'].append(fdict)

##    from django.core.serializers import serialize
##    jsondict = serialize('geojson', queryset,
##                          geometry_field='geom',
##                          #fields=('name',))
##                         )
    
    return response.Response(jsondict)
       
def mapzoomtest(request):

    ###

    if "Name" in request.GET:
        custombanner = '<h3 style="text-align:center; padding:10%;">Province search still under construction...</h3>'

        return render(request, 'pshapes_site/base_grid.html', dict(custombanner=custombanner)
                      )
    
    mapp = render_to_string("provshapes/mapzoomtest.html")

    custombanner = mapp

    grids = []
    content = """
    <div id="provframe">
    None selected
    </div>
    
    <script>
    function selectfunc(feature) {
        alterns = feature.attributes.Alterns.join("; ");
        if (alterns) {
            alterns = " (" + alterns + ")";
        };
        table = "<table>"
            table += "<tr>"
            table += "<td>Country: </td>"
            table += "<td>" + feature.attributes.country + "</td>"
            table += "</tr>"
            
            table += "<tr>"
            table += "<td>Name: </td>"
            table += "<td>" + feature.attributes.Name + alterns + "</td>"
            table += "</tr>"
            
            table += "<tr>"
            table += "<td>Time period: </td>"
            table += "<td>" + feature.attributes.start + " to " + feature.attributes.end + "</td>"
            table += "</tr>"

            table += "<tr>"
            table += "<td>Codes: </td>"
            table += "<td>ISO=" + feature.attributes.ISO + ", FIPS=" + feature.attributes.FIPS + ", HASC=" + feature.attributes.HASC + "</td>"
            table += "</tr>"
        table += "</table>"
        document.getElementById("provframe").innerHTML = table;
    };
    function unselectfunc(feature) {
        document.getElementById("provframe").innerHTML = "None selected";
    };
    selectControl = new OpenLayers.Control.SelectFeature(provLayer, {onSelect: selectfunc, onUnselect: unselectfunc, selectStyle: {fillColor: "turquoise", strokeWidth: 2}});
    map.addControl(selectControl);
    selectControl.activate();
    </script>
    """
    grids.append(dict(title="Province:",
                      content=content,
                      width="99%")
                 )

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

def explore(request):
    return render(request, 'provshapes/explore.html')

def explore(request):
    grids = []
    bannertitle = ""
    custombanner = """
                <div style="text-align:center">
                <h2>Interactive data explorer</h2>
                <img src="http://www.iconarchive.com/download/i66283/jommans/ironman-style/Internet-Explorer.ico">
                <p style="text-align:center"><em>This functionality is not yet available, but will be once the first stable version is released.</em></p>
                """
    bannerright = ''
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids, "custombanner":custombanner}
                  )

def explore(request):
    import urllib2
    import json

    ###

    if "Name" in request.GET:
        custombanner = '<h3 style="text-align:center; padding:10%;">Province search still under construction...</h3>'

        return render(request, 'pshapes_site/base_grid.html', dict(custombanner=custombanner)
                      )
    
    mapp = render_to_string("provshapes/mapview.html")

    custombanner = mapp

    grids = []
    content = """
    <div id="provframe">
    None selected
    </div>
    
    <script>
    function selectfunc(feature) {
        alterns = feature.attributes.Alterns.join("; ");
        if (alterns) {
            alterns = " (" + alterns + ")";
        };
        table = "<table>"
            table += "<tr>"
            table += "<td>Country: </td>"
            table += "<td>" + feature.attributes.country + "</td>"
            table += "</tr>"
            
            table += "<tr>"
            table += "<td>Name: </td>"
            table += "<td>" + feature.attributes.Name + alterns + "</td>"
            table += "</tr>"
            
            table += "<tr>"
            table += "<td>Time period: </td>"
            table += "<td>" + feature.attributes.start + " to " + feature.attributes.end + "</td>"
            table += "</tr>"

            table += "<tr>"
            table += "<td>Codes: </td>"
            table += "<td>ISO=" + feature.attributes.ISO + ", FIPS=" + feature.attributes.FIPS + ", HASC=" + feature.attributes.HASC + "</td>"
            table += "</tr>"
        table += "</table>"
        document.getElementById("provframe").innerHTML = table;
    };
    function unselectfunc(feature) {
        document.getElementById("provframe").innerHTML = "None selected";
    };
    selectControl = new OpenLayers.Control.SelectFeature(provLayer, {onSelect: selectfunc, onUnselect: unselectfunc, selectStyle: {fillColor: "turquoise", strokeWidth: 2}});
    map.addControl(selectControl);
    selectControl.activate();
    </script>
    """
    grids.append(dict(title="Province:",
                      content=content,
                      width="99%")
                 )

    return render(request, 'pshapes_site/base_grid.html', dict(custombanner=custombanner,
                                                               grids=grids)
                  )






