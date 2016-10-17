from django.shortcuts import render

# Create your views here.

def underconstruction(request):
    grids = []
    bannertitle = "Under construction..."
    bannerleft = "This page is currently under construction"
    bannerright = ""
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

def interactive(request):
    return render(request, 'provshapes/interactive.html')

def interactive(request):
    grids = []
    bannertitle = "Interactive data explorer"
    bannerleft = '<p style="text-align:left">This functionality is not yet available, but will be once the first stable version is released. </p>'
    bannerright = ""
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

def data(request):
    return render(request, 'provshapes/data.html')

def data(request):
    return underconstruction(request)
