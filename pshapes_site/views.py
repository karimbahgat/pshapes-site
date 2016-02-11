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
