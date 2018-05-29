from django.shortcuts import render, get_object_or_404, redirect
from django.template import Template,Context
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied

# Create your views here.

from django.contrib.gis import forms
from django.contrib.gis.geos import Polygon, MultiPolygon

from .models import ProvShape, CntrShape
from provchanges.models import ProvChange

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

                #if props['country'] not in 'Egypt':
                #    continue # temp dropping
                
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

            # update countries
            CntrShape.objects.all().delete()
            for f in ProvShape.objects.distinct('country'):
                cntr = f.country
                print 'country:', cntr
                feats = ProvShape.objects.filter(country=cntr, simplify=0)
                dates = sorted(set( [f.start for f in feats] + [f.end for f in feats] ))
                prevdate = dates[0]
                prevunion = None
                for date in dates[:-1]:
                    print prevdate,date
                    datefeats = feats.filter(start__lte=date, end__gt=date)
                    print len(list(datefeats))
                    geoms = (f.geom for f in datefeats)
                    first = next(geoms)
                    union = reduce(lambda prev,nxt: prev.union(nxt), geoms, first)
                    union = union.buffer(0.001).buffer(-0.001)
                    
                    if prevunion:
                        #print 'areadiff', prevunion.area, union.area, prevunion.area - union.area
                        if abs(prevunion.area - union.area) > 0.01:
                            print 'bbox',prevunion.extent
                            for tolerance in [0.2,0.1,0]:
                                geom = prevunion.simplify(tolerance, preserve_topology=True)
                                if geom.geom_type == 'Polygon':
                                    geom = MultiPolygon([geom])
                                cntrshape = CntrShape(name=cntr,
                                                  start=prevdate,
                                                  end=date,
                                                  simplify=tolerance,
                                                  geom=geom,
                                                  geoj=geom.geojson,)
                                cntrshape.save()
                            prevdate = date
                        else:
                            print 'no geo change'

                    prevunion = union

                # add last one
                date = dates[-1]
                print prevdate,date
                print 'bbox',prevunion.extent
                for tolerance in [0.2,0.1,0]:
                    geom = prevunion.simplify(tolerance, preserve_topology=True)
                    if geom.geom_type == 'Polygon':
                        geom = MultiPolygon([geom])
                    cntrshape = CntrShape(name=cntr,
                                      start=prevdate,
                                      end=date,
                                      simplify=tolerance,
                                      geom=geom,
                                      geoj=geom.geojson,)
                    cntrshape.save()

            print 'countries updated!'
            
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
    params = dict(((k,v) for k,v in request.query_params.items() if v))

    getlvl = int(float(params.pop('getlevel', 1)))
    queryset = ProvShape.objects.all()

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

    if getlvl == 1:
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

    elif getlvl == 0:
        # attribute filtering
        print 'apiparams',params
        # special name search
        if 'name' in params:
            queryset = queryset.filter(name__icontains=params['name']) | queryset.filter(alterns__icontains=params['name'])
        # add remaining conditions
        restdict = dict(((k,v) for k,v in params.items() if k!='name'))
        if restdict:
            queryset = queryset.filter(**restdict)

        # get countries from results
        countries = [row['country'] for row in queryset.distinct('country').values('country')]
        print countries




        # now get the country objects
        queryset = CntrShape.objects.all()
        queryset = queryset.filter(simplify=tolerance)
        queryset = queryset.filter(name__in=countries)

        if all((yr,mn,dy)):
            print 'filtering date'
            date = datetime.date(int(yr),int(mn),int(dy))
            queryset = queryset.filter(start__lte=date).filter(end__gte=date)




        import time
        t=time.time()

        # convert to json
        fields = ['geoj','name','start','end']
            
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

    else:
        raise Exception('getlevel must be 0 (countries) or 1 (provinces)')




    
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
        widgets = dict(country=forms.Select(attrs={'onchange':'submitsearch();'},
                                            choices=[("","")]+[(c.country,c.country) for c in ProvShape.objects.distinct('country')]))





def viewprov(request):

    date = datetime.date(*map(int,request.GET['date'].split('-')))
    country = request.GET['country']
    name = request.GET['name']
    prov = ProvShape.objects.filter(simplify=0, country=country, name=name, start__lte=date, end__gt=date).first()

    bannertitle = '<h2 style="padding-top:10px">%s (%s - %s)</h2>' % (prov.name.encode('utf8'), prov.start.year, prov.end.year)
    
    mapp = """
	<script src="http://openlayers.org/api/2.13/OpenLayers.js"></script>

            <div style="width:95%; height:44vh; margins:auto; border-radius:10px; background-color:rgb(0,162,232);" id="map">
            </div>
	
	<script defer="defer">
	var map = new OpenLayers.Map('map', {allOverlays: true,
                                            controls:[],
                                            });
	</script>

        <script>
	// empty country layer
	var style = new OpenLayers.Style({fillColor:"rgb(200,200,200)", strokeWidth:0.2, strokeColor:'white'},
					);
	var countryLayer = new OpenLayers.Layer.Vector("Country", {styleMap:style});
	map.addLayers([countryLayer]);

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
        
	// empty province layer
	var style = new OpenLayers.Style({fillColor:"rgb(122,122,122)", strokeWidth:0.2, strokeColor:'white'},
					);
	var provLayer = new OpenLayers.Layer.Vector("Provinces", {styleMap:style});
	map.addLayers([provLayer]);

        renderprovs = function(data) {
		var geojson_format = new OpenLayers.Format.GeoJSON();
		var geoj_str = JSON.stringify(data);
		provs = geojson_format.read(geoj_str, "FeatureCollection");
		
		feats = [];
		for (feat of provs) {
                        feats.push(feat);
		};
		provLayer.addFeatures(feats);
	};
        $.getJSON('/api', {simplify:0, year:date[0], month:date[1], day:date[2], country:country, getlevel:1}, renderprovs);


        // hardcoded highlight prov

	var hstyle = new OpenLayers.Style({fillColor:"rgb(62,95,146)", strokeWidth:2, strokeColor:'white'},
					);
	var highlightLayer = new OpenLayers.Layer.Vector("Highlight", {styleMap:hstyle});
	map.addLayers([highlightLayer]);

        var geojson_format = new OpenLayers.Format.GeoJSON();
        highlightProv = geojson_format.read(prov_geoj, "FeatureCollection");
        
        feats = [];
        for (feat of highlightProv) {
                feats.push(feat);
        };
        highlightLayer.addFeatures(feats);
        map.zoomToExtent(highlightLayer.getDataExtent());
        map.zoomOut();
        map.zoomOut();



        //Set up a click handler
        OpenLayers.Control.Click = OpenLayers.Class(OpenLayers.Control, {                
            defaultHandlerOptions: {
                'single': true,
                'double': false,
                'pixelTolerance': 0,
                'stopSingle': false,
                'stopDouble': false
            },

            initialize: function(options) {
                this.handlerOptions = OpenLayers.Util.extend(
                    {}, this.defaultHandlerOptions
                );
                OpenLayers.Control.prototype.initialize.apply(
                    this, arguments
                ); 
                this.handler = new OpenLayers.Handler.Click(
                    this, {
                        'click': this.trigger
                    }, this.handlerOptions
                );
            }, 

            trigger: function(e) {
                //A click happened!
                var lonlat = map.getLonLatFromViewPortPx(e.xy)

                //alert("You clicked near " + lonlat.lat + ", " + lonlat.lon);

                var point = new OpenLayers.Geometry.Point(lonlat.lon, lonlat.lat);
                for (feat of provLayer.features) {
                    if (point.intersects(feat.geometry)) {
                        //alert('match');
                        //alert(feat.attributes.name);
                        var name = feat.attributes.name;
                        var country = feat.attributes.country;
                        var date = feat.attributes.start;
                        window.location.href = "/viewprov?country="+country+"&name="+name+"&date="+date;
                        return true;
                        };
                };
            }

        });

        var click = new OpenLayers.Control.Click();
        map.addControl(click);
        click.activate();


        </script>
        """ 
    
    bannerleft = """
                <div style="margin-top:30px">
                        <div style="text-align:center">
                            <script>
                                var country = '{country}'
                                var date = '{date}'.split('-');
                                var prov_geoj = '{geoj}';
                            </script>
                            
                            {mapp}

                            <br>

                            <a href="/explore/?country={country}&name={name}&date={date}" style="text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">
                            Explore in Map View
                            </a>
                            
                        </div>
                </div>
                <br>
                        """.format(mapp=mapp, geoj=prov.geoj, date=request.GET['date'], country=country.encode('utf8'), name=prov.name.encode('utf8'))


##    imgmeta = 'https://en.wikipedia.org/w/api.php?action=query&titles={name}&prop=images&format=json&formatversion=2'.format(name=prov.name)
##    firstimg = json.loads(urllib2.urlopen(imgmeta).read())['query']['pages'][0]['images'][0]['title']
##    if firstimg.startswith('File:'): firstimg = firstimg[5:]
##    wikiimgurl = "https://commons.wikimedia.org/wiki/Special:FilePath/" + firstimg + '?width=300'
##
##    wikimeta = 'https://en.wikipedia.org/w/api.php?action=query&titles={name}&prop=extracts&exintro=&format=json&formatversion=2'.format(name=prov.name)
##    wikiextract = json.loads(urllib2.urlopen(wikimeta).read())['query']['pages'][0]['extract']
##
##    infobox = """
##                        <p>
##                        {wikiextract}
##                        <img width="80%" src="{wikiimgurl}">
##                        </p>
##                """.format(wikiimgurl=wikiimgurl, wikiextract=wikiextract.encode('utf8'))

    infobox = ""

    bannerright = """
                    <br><br><br><br>
                    <div style="text-align:left"><b>

                        <p>
                        Country: {country}
                        </p>

                        <p>
                        Alternate names: {alterns}
                        </p>

                        <p>
                        ISO code: {iso}
                        </p>

                        <p>
                        FIPS code: {iso}
                        </p>

                        <p>
                        HASC code: {iso}
                        </p>

                        {infobox}
                        
                    </b></div>
                        """.format(country=prov.country.encode('utf8'),
                                   alterns='; '.join(prov.alterns.encode('utf8').split('|')),
                                   iso=prov.iso, fips=prov.fips, hasc=prov.hasc,
                                   infobox=infobox,
                                   )

    grids = []

    # TODO: need to consider that alternate names may have been used to match changes with provs

    # prev change
    def addlink(country, name, date, typ, country2=None):
        link = "/viewprov?country=%s&name=%s&date=%s" % (country.encode('utf8'), name.encode('utf8'), date - datetime.timedelta(days=1))
        button = """
                        <a href="{link}" style="text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">
                        <<
                        </a>
                    """.format(link=link)
        if country2 and country2 != country:
            name += ' (%s)' % country.encode('utf8')
        info = """
                        <h3 style="margin:0">{name}</h3>
                        <p>Type: {typ}
                        </p>
                    """.format(typ=typ, name=name.encode('utf8'))
        return """
                    <div style="margin-left:40px">
                    <div style="display:inline-block; vertical-align:top">{button}</div>
                    <div style="display:inline-block; vertical-align:top">{info}</div>
                    </div>
                    """.format(button=button, info=info)

    content = '<h3 style="margin-left:20px">%s:</h3>' % prov.start
    
    prep = ProvChange.objects.filter(status__in=["Active","Pending"], tocountry=prov.country, date=prov.start).exclude(type='Begin')
    for name in [prov.name] + prov.alterns.split('|'):
        if not name: continue
        results = [o for o in prep if name in [o.toname]+o.toalterns.split('|')]
        if results: break
        
    # if previously existed and received territory from another province (*Existing), means current prov existed prior to the change (implicit in the event type)
    # NOTE: the old FullTransfer and PartTransfer will produce wrong results sometimes, since doesnt differentiate
    typs = [o.type for o in results]
    if ('TransferExisting' in typs or 'MergeExisting' in typs or 'FullTransfer' in typs or 'PartTransfer' in typs) and not 'NewInfo' in typs:
        content += addlink(prov.country, prov.name, prov.start, 'Before Gaining Territory')
    # if not, the same situation can be found if previously gave away parts of territory, but then we have to look for frommatch rather than tomatch
    else:
        prep2 = ProvChange.objects.filter(status__in=["Active","Pending"], type__in=['Breakaway','TransferExisting','TransferNew','PartTransfer'], fromcountry=prov.country, date=prov.start)
        for name in [prov.name] + prov.alterns.split('|'):
            if not name: continue
            results2 = [o for o in prep2 if name in [o.fromname]+o.fromalterns.split('|')]
            for o in results2:
                o.type = 'Before Losing Territory'
            if results2: break
        if results2 and not 'NewInfo' in [o.type for o in results]:
            results += [results2[0]] # one is enough to represent
        
    if not results:
        # no match for the name, but maybe as part of a multiple event (*)
        results = list(prep.filter(toname='*'))
        for o in results:
            o.fromname = prov.name

    if results:
        # one or more changes
        # add all changes
        for prevchange in results:
            content += addlink(prevchange.fromcountry, prevchange.fromname, prevchange.date, prevchange.type, country2=prevchange.tocountry)

    else:
        # no more changes
        button = """
                        <a style="text-align:center; background-color:gray; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">
                        <<
                        </a>
                    """
        info = """
                        <p>No more changes
                        </p>
                    """
        content += """
                    <div style="margin-left:20px">
                    <div style="display:inline-block; vertical-align:top">{button}</div>
                    <div style="display:inline-block; vertical-align:top">{info}</div>
                    </div>
                    """.format(button=button, info=info)
    grids.append(dict(title='Previous change:',
                     content=content,
                     style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                     width="45%",
                     ))

    # next change

    # OLD
##    nextchange = ProvChange.objects.exclude(type='Begin').filter(status__in=["Active","Pending"], fromcountry=prov.country, fromname=prov.name, date__gte=date).order_by('date').first()
##    if not nextchange:
##        # no match for the name, but maybe as part of a multiple event (*)
##        nextchange = ProvChange.objects.exclude(type='Begin').filter(status__in=["Active","Pending"], fromcountry=prov.country, fromname='*', date__gte=date).order_by('date').first()
##        if nextchange: nextchange.toname = prov.name
##    if nextchange:
##        link = "/viewprov?country=%s&name=%s&date=%s" % (nextchange.tocountry.encode('utf8'), nextchange.toname.encode('utf8'), nextchange.date + datetime.timedelta(days=1))
##        button = """
##                        <a href="{link}" style="text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">
##                        >>
##                        </a>
##                    """.format(link=link)
##        info = """
##                        <h3 style="margin:0">{date}</h3>
##                        <p>Type: {typ}
##                        </p>
##                    """.format(typ=nextchange.type, date=prov.end)

    # NEW
    def addlink(country, name, date, typ, country2=None):
        link = "/viewprov?country=%s&name=%s&date=%s" % (country.encode('utf8'), name.encode('utf8'), date ) #+ datetime.timedelta(days=1))
        button = """
                        <a href="{link}" style="text-align:center; background-color:orange; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">
                        >>
                        </a>
                    """.format(link=link)
        if country2 and country2 != country:
            name += ' (%s)' % country.encode('utf8')
        info = """
                        <h3 style="margin:0">{name}</h3>
                        <p>Type: {typ}
                        </p>
                    """.format(typ=typ, name=name.encode('utf8'))
        return """
                    <div style="margin-left:40px">
                    <div style="display:inline-block; vertical-align:top">{info}</div>
                    <div style="display:inline-block; vertical-align:top">{button}</div>
                    </div>
                    """.format(button=button, info=info)

    content = '<h3 style="margin-left:20px">%s:</h3>' % prov.end
    
    prep = ProvChange.objects.filter(status__in=["Active","Pending"], fromcountry=prov.country, date=prov.end).exclude(type='Begin')
    for name in [prov.name] + prov.alterns.split('|'):
        if not name: continue
        results = [o for o in prep if name in [o.fromname]+o.fromalterns.split('|')]
        if results: break

    # if breakaway or giving away parts of territory, means a continuation of current prov continues to exist (implicit in the event type)
    # TODO: maybe show change type icon
    typs = [o.type for o in results]
    if ('Breakaway' in typs or 'TransferNew' in typs or 'TransferExisting' in typs or 'PartTransfer' in typs) and not 'NewInfo' in typs:
        content += addlink(prov.country, prov.name, prov.end, 'Remaining')

    # needs for receiving as well, ie gained territory, but need to match with toname instead of fromname
    # NOTE: the old FullTransfer and PartTransfer will produce wrong results sometimes, since doesnt differentiate
    else:
        prep2 = ProvChange.objects.filter(status__in=["Active","Pending"], type__in=['TransferExisting','MergeExisting','PartTransfer','FullTransfer'], tocountry=prov.country, date=prov.end)
        print list(prep2)
        
        for name in [prov.name] + prov.alterns.split('|'):
            if not name: continue
            results2 = [o for o in prep2 if name in [o.toname]+o.toalterns.split('|')]
            for o in results2:
                o.type = 'After Gaining Territory'
            if results2: break
        
    if not results:
        # no match for the name, but maybe as part of a multiple event (*)
        results = list(prep.filter(fromname='*'))
        for o in results:
            o.toname = prov.name
    if not results:
        # if still no event, even *, then add after gaining (see results2 above)
        if results2:
            results += [results2[0]] # one is enough to represent
            
    if results:
        # one or more changes
        # add all changes
        for nextchange in results:
            content += addlink(nextchange.tocountry, nextchange.toname, nextchange.date, nextchange.type, country2=nextchange.fromcountry)

    else:
        # no more changes
        button = """
                        <a style="text-align:center; background-color:gray; color:white; border-radius:5px; padding:5px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:none; margin:5px;">
                        >>
                        </a>
                    """
        info = """
                        <p>No more changes
                        </p>
                    """
        content += """
                    <div style="margin-left:20px">
                    <div style="display:inline-block; vertical-align:top">{info}</div>
                    <div style="display:inline-block; vertical-align:top">{button}</div>
                    </div>
                    """.format(button=button, info=info)
    grids.append(dict(title='Next change:',
                     content=content,
                     style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                     width="45%",
                     ))

    # nearby wikipedia entries and pictures
    # TODO: search by location (centroid and radius)
    # TODO: also filter to only show images from within the daterange (&prop=imageinfo&iiprop=extmetadata, and 'imageinfo'-'extmetadata'-'DateTimeOriginal'-'value')
    #url = 'https://en.wikipedia.org/w/api.php?action=query&prop=coordinates%7Cpageimages%7Cpageterms&colimit=50&piprop=thumbnail&pithumbsize=144&pilimit=50&wbptterms=description&generator=geosearch&ggscoord=37.786952%7C-122.399523&ggsradius=10000&ggslimit=50&format=json'

    # old bbox approach
    # but bbox are too big for wikipeida to handle in most cases
    # expects topleft,bottomright, apparently thinking of coordinates as lat/long, thus expecting y/x instead of the usual x/y
    # see https://en.wikipedia.org/w/api.php?action=help&modules=query%2Bgeosearch
##    xmin,ymin,xmax,ymax = list(prov.geom.extent)
##    bbox = ymax,xmin,ymin,xmax 
##    bbox = '|'.join(map(str,bbox))

##    pages = []
##    imgs = []
##    from django.contrib.gis.geos import GEOSGeometry
##    from random import uniform
##    bbox = prov.geom.extent
##    searchflag = True
##    while searchflag:
##        # look for images around random point within area
##        x,y = uniform(bbox[0],bbox[2]), uniform(bbox[1],bbox[3])
##        point = GEOSGeometry('POINT(%s %s)' % (x,y))
##        if not point.intersects(prov.geom):
##            print 'random point failed!'
##            continue
##        point = '|'.join([str(y),str(x)])
##        radius = 10000
##        searchpagesurl = "https://en.wikipedia.org/w/api.php?action=query&generator=geosearch&ggscoord=%s&ggsradius=%s&ggslimit=50&format=json" % (point,radius)
##        print searchpagesurl
##        result = json.loads(urllib2.urlopen(searchpagesurl).read())
##        if not 'query' in result:
##            print 'no articles near that coordinate!'
##            continue
##        # now search for images inside those articles
##        pages += result['query']['pages'].values()
##        pageids = result['query']['pages'].keys()
##        pageids = '|'.join(map(str,pageids))
##        searchimgurl = "https://en.wikipedia.org/w/api.php?action=query&pageids=%s&prop=images&format=json" % pageids
##        print searchimgurl
##        result = json.loads(urllib2.urlopen(searchimgurl).read())
##        if not 'query' in result:
##            print 'unexpected error, no hits for the page ids!'
##            continue
##        for pageid,pagedict in result['query']['pages'].items():
##            print pagedict
##            if not 'images' in pagedict:
##                print 'no images in this article'
##                continue
##            for img in pagedict['images']:
##                imgname = img['title'].encode('utf8')
##                if imgname.lower().endswith('.svg'):
##                    continue
##                imgname = imgname[5:] if imgname.startswith('File:') else imgname
##                if imgname in (img['imgname'] for img in imgs):
##                    continue
##                imgurl = "https://commons.wikimedia.org/wiki/Special:FilePath/%s?width=200" % imgname
##                imgs.append(dict(imgname=imgname, imgurl=imgurl))
##                print 'adding',len(imgs),imgurl
##                if len(imgs) >= 6:
##                    searchflag = False
##                    break
##            if not searchflag:
##                break
##
##    # first wiki pages
##    grids.append(dict(title='Wikipedia Articles:',
##             content='',
##             style="background-color:white; margins:20px; padding: 0 0; border-style:none",
##             width="97%",
##             ))
##    
##    for page in pages[:6]:
##        page['title'] = page['title'].encode('utf8')
##        linkbox = """
##                    <div style="padding-left:10px" >
##                    <a style="color:black" href="https://en.wikipedia.org/?curid={pageid}">
##                    <img style="padding-right:10px" height="40px" align="left" src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Tango_style_Wikipedia_Icon.svg/2000px-Tango_style_Wikipedia_Icon.svg.png">
##                    <h3>{title}</h3>
##                    </a>
##                    </div>
##                    """.format(**page)
##        grids.append(dict(title='',
##                         content=linkbox,
##                         style="background-color:white; margins:20px; padding: 0 0; border-style:none",
##                         width="30%",
##                         height="100px",
##                         ))
##
##    # then imgs
##    grids.append(dict(title='In Pictures:',
##                     content='',
##                     style="background-color:white; margins:20px; padding: 0 0; border-style:none",
##                     width="97%",
##                     ))
##    
##    for img in imgs:
##        content = """
##                            <div style="text-align:center">
##                            <h3>{imgname}</h3>
##                            <img height="200px" src="{imgurl}">
##                            </div>
##                    """.format(**img)
##        grids.append(dict(title='',
##                         content=content,
##                         style="background-color:white; margins:20px; padding: 0 0; border-style:none",
##                         width="30%",
##                         height="200px",
##                         ))
        

    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )




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
    provs = ProvShape.objects.all() #.order_by("country", "name", "start")

    # ignore simplified versions
    provs = provs.filter(simplify=0)
    
    if request.GET:
        #filterdict = dict(((k,v) for k,v in request.GET.items() if v))
        #provs = provs.filter(**filterdict)
        filterdict = dict(((k,v) for k,v in request.GET.items() if v))
        initdate = filterdict.pop('date', None)
        # special name search
        if 'name' in request.GET and request.GET['name']:
            provs = provs.filter(name__icontains=request.GET['name']) | provs.filter(alterns__icontains=request.GET['name'])
        # add remaining conditions
        restdict = dict(((k,v) for k,v in filterdict.items() if k!='name'))
        if restdict:
            provs = provs.filter(**restdict)
    else:
        initdate = None
        filterdict = dict()

    dates = [d.isoformat() for d in sorted(provs.distinct('start').values_list('start',flat=True))]
    #dates = [d.isoformat() for d in sorted(set(provs.values_list('start', flat=True)))]
    #if dates: dates.append( provs.latest('end').end.isoformat() )
    if dates: dates.append( max(provs.distinct('end').values_list('end',flat=True)).isoformat() )
    #print dates
    
    if not initdate: initdate = dates[-1]
    
    custombanner = render(request, 'provshapes/mapview.html',
                          dict(getparams=json.dumps(filterdict),
                               searchform=searchform, dates=dates, initdate=initdate),
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
    for rowdict in provs.values(*fields)[:50]:
        #rowdict = dict([(f,getattr(p, f, "")) for f in fields])
        rowdict['alterns'] = '; '.join(rowdict['alterns'].split('|'))
        link = "/viewprov?country=%s&name=%s&date=%s" % (rowdict['country'].encode('utf8'), rowdict['name'].encode('utf8'), rowdict['start'])
        linkimg = '<a href="%s"><img height="30px" src="/static/globe.png"></a>' % link
        row = [linkimg] + [rowdict[f] for f in fields]
        lists.append((None,row))

    listtable = lists2table(request, lists, [""]+fields)
    
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




