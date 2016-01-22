from django.shortcuts import render

# Create your views here.



def mapview(request):
    return render(request, 'cshapes/mapview.html')

def mapview_lite(request):
    return render(request, 'cshapes/mapview_lite.html')



from cshapes.models import cshapes
from rest_framework import viewsets, generics, views, decorators, response

@decorators.api_view(["GET"])
def apiview(request):
    print request.query_params
    print "------"
    queryset = cshapes.objects.all()
    
    yr = request.query_params.get('year', None)
    mn = request.query_params.get('month', None)
    dy = request.query_params.get('day', None)
    
    if all((yr,mn,dy)):
        queryset = cshapes.objects.filter(gwsyear__lte=yr
                                          ).filter(
                                              gweyear__gte=yr)

    # builtin django doesnt work due to bug, geoms just become null values...
##    from django.core.serializers import serialize
##    jsonstring = serialize("geojson", queryset,
##                          geometry_field='geom',
##                          fields=('cntry_name',"gwsyear"),
##                           )
##
##    import json
##    jsondict = json.loads(jsonstring)

    # django-geojson, auto transforms if different srids so requires checking
    from djgeojson.serializers import Serializer as GeoJSONSerializer
    
    jsonstring = GeoJSONSerializer().serialize(queryset,
                                              geometry_field='geom',
                                               )

    import json
    jsondict = json.loads(jsonstring)

    # still very slow, maybe best way is just to get the normal values dict
    # and then separately convert the geom wkt to geoj
    ### jsondict = queryset.values("cntry_name","gwsyear")
    
    
    return response.Response(jsondict)

    
# original most correct using geo rest framework, but super super slow

##from cshapes.serializers import CshapesSerializer
##class CshapesViewSet(viewsets.ModelViewSet):
##    """
##    API endpoint that allows users to be viewed or edited.
##    """
##    serializer_class = CshapesSerializer
##
##    queryset = cshapes.objects.all()
##    def get_queryset(self):
##        queryset = cshapes.objects.all()
##        
##        yr = self.request.query_params.get('year', None)
##        mn = self.request.query_params.get('month', None)
##        dy = self.request.query_params.get('day', None)
##        
##        if all((yr,mn,dy)):
##            queryset = cshapes.objects.filter(gwsyear__lte=yr
##                                              ).filter(
##                                                  gweyear__gte=yr)
##
##        return queryset
            
        

