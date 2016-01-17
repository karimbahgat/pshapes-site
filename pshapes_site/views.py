"""pshapes_site

Static page views.

"""
from django.shortcuts import render

def contact(request):
    return render(request, 'pshapes_site/contact.html')

def method(request):
    return render(request, 'pshapes_site/method.html')

def download(request):
    return render(request, 'pshapes_site/download.html')
