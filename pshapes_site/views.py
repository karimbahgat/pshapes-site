"""pshapes_site

Static page views.

"""
from django.shortcuts import render

from provchanges.models import ProvChange

shortdescr = """
Pshapes is an open-source crowdsourcing project for creating and quality-checking
data on historical provinces, created by and for data-enthusiasts, researchers,
and others. 
"""

def home(request):
    changelist = ProvChange.objects.all().order_by("-added") # the dash reverses the order
    return render(request, 'pshapes_site/home.html', {"shortdescr":shortdescr, "changelist":changelist})

def about(request):
    return render(request, 'pshapes_site/about.html')

def testgrid(request):
    grids = tuple([("title%s"%i, "content%s"%i) for i in range(5)])
    bannertitle = "Banner Title"
    bannerleft = "Banner left"
    bannerright = "Banner right"
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

