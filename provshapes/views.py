from django.shortcuts import render
from django.template.loader import render_to_string

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

    ###

    
    mapp = render_to_string("provshapes/mapview.html")

    custombanner = mapp

    grids = []
    grids.append(dict(title="Province:",
                      content="None selected",
                      width="99%")
                 )

    return render(request, 'pshapes_site/base_grid.html', dict(custombanner=custombanner,
                                                               grids=grids)
                  )





