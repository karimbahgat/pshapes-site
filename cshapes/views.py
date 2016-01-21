from django.shortcuts import render

# Create your views here.

def mapview(request):
    return render(request, 'cshapes/mapview.html')



from cshapes.models import cshapes
from rest_framework import viewsets, generics, views
from cshapes.serializers import CshapesSerializer

##class CshapesViewSet(views.APIView):
##    def get(self, request):
##        data = cshapes.objects.values()
##        print str(data)[:100]
##        return Response(data)
    
class CshapesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = CshapesSerializer

    queryset = cshapes.objects.all()
    def get_queryset(self):
        queryset = cshapes.objects.all()
        
        yr = self.request.query_params.get('year', None)
        mn = self.request.query_params.get('month', None)
        dy = self.request.query_params.get('day', None)
        
        if all((yr,mn,dy)):
            queryset = cshapes.objects.filter(gwsyear__lte=yr
                                              ).filter(
                                                  gweyear__gte=yr)

        return queryset
            
        

