from django.shortcuts import render

# Create your views here.

def interactive(request):
    return render(request, 'provshapes/interactive.html')

def data(request):
    return render(request, 'provshapes/data.html')
