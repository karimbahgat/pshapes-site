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
    content = """
    <div id="provframe">
    None selected
    </div>
    
    <script>
    function selectfunc(feature) {
        alterns = feature.attributes.Alterns.join("; ");
        if (alterns) {
            alterns = " (" + alterns + ")";
        };
        table = "<table>"
            table += "<tr>"
            table += "<td>Country: </td>"
            table += "<td>" + feature.attributes.country + "</td>"
            table += "</tr>"
            
            table += "<tr>"
            table += "<td>Name: </td>"
            table += "<td>" + feature.attributes.Name + alterns + "</td>"
            table += "</tr>"
            
            table += "<tr>"
            table += "<td>Time period: </td>"
            table += "<td>" + feature.attributes.start + " to " + feature.attributes.end + "</td>"
            table += "</tr>"

            table += "<tr>"
            table += "<td>Codes: </td>"
            table += "<td>ISO=" + feature.attributes.ISO + ", FIPS=" + feature.attributes.FIPS + ", HASC=" + feature.attributes.HASC + "</td>"
            table += "</tr>"
        table += "</table>"
        document.getElementById("provframe").innerHTML = table;
    };
    function unselectfunc(feature) {
        document.getElementById("provframe").innerHTML = "None selected";
    };
    selectControl = new OpenLayers.Control.SelectFeature(provLayer, {onSelect: selectfunc, onUnselect: unselectfunc, selectStyle: {fillColor: "turquoise", strokeWidth: 2}});
    map.addControl(selectControl);
    selectControl.activate();
    </script>
    """
    grids.append(dict(title="Province:",
                      content=content,
                      width="99%")
                 )

    return render(request, 'pshapes_site/base_grid.html', dict(custombanner=custombanner,
                                                               grids=grids)
                  )






