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

    return render(request, 'provshapes/mapview.html')





