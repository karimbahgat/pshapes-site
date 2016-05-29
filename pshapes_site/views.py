"""pshapes_site

Static page views.

"""
from django.shortcuts import render
from django.template import Template,Context

from provchanges.models import ProvChange

shortdescr = """
Pshapes is an open-source crowdsourcing project for creating and quality-checking
data on historical provinces, created by and for data-enthusiasts, researchers,
and others. 
"""

def recentadds(request):
    html = """
		<table style="font-size:small"> 
		
			<style>
			table {
				border-collapse: collapse;
				width: 100%;
			}

			th, td {
				text-align: left;
				padding: 8px;
			}

			tr:nth-child(even){background-color: #f2f2f2}

			th {
				background-color: orange;
				color: white;
			}
			</style>
		
			<tr>
				<th> 
				</th>
				
				<th>
                <b>User</b>
				</th>

				<th>
                <b>Added</b>
				</th>
			
				<th>
                <b>Country</b>
				</th>

				<th>
                <b>Province</b>
				</th>
				
				<th>
                <b>Type</b>
				</th>
				
			</tr>
			</a>
			
			{% for change in changelist|slice:":3" %}
				<tr>
					<td>
					<a href="{% url 'viewchange' pk=change.pk %}">View</a>
					</td>
					
					<td>
					{{ change.user }}
					</td>

					<td>
					{{ change.added }}
					</td>

					<td>
					{{ change.country }}
					</td>
					
					<td>
					{{ change.toname }}
					</td>
					
					<td>
					{{ change.type }}
					</td>
					
				</tr>
			{% endfor %}
		</table>
	    """
    changelist = ProvChange.objects.all().order_by("-added") # the dash reverses the order
    rendered = Template(html).render(Context({"request":request, "shortdescr":shortdescr, "changelist":changelist}))
    return rendered

def home(request):
    changelist = ProvChange.objects.all().order_by("-added") # the dash reverses the order
    return render(request, 'pshapes_site/home.html', {"shortdescr":shortdescr, "changelist":changelist})

def home(request):
    bannertitle = "Crowdsourcing Historical Province Boundaries, 1946-2014"
    bannerleft = """
			<style>
			.shadow
			{
				display:block;
				position:relative;
				height:300px;
				background-image:url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYci40tiT9XecIGMtu8pLPGd7XqYXwNT_CCZ5PtyDA9ubVl0-P7g);
				background-size:100% 100%;
			}
			.shadow:before
			{
				display:block;
				content:'';
				position:absolute;
				width:100%;
				height:100%;
				-moz-box-shadow:inset 0px 0px 3px 1px rgba(0,0,0,1);
				-webkit-box-shadow:inset 0px 0px 3px 1px rgba(0,0,0,1);
				box-shadow:inset 0px 0px 10px 10px rgba(0,0,0,1);
			}
			</style>
			<div class="shadow"></div>
    """
    if request.user.is_authenticated:
        bannerright = """
                        <p>Welcome, {username}!</p>
                        Help keep track of our changing world:

                        <ul style="list-style-type:none">
                            <li><a href="/contribute/submitchange" style="background-color:orange; color:white; border-radius:5px; padding:5px">
                            <b>Submit New Change</b>
                            </a></li>
                            
                            <li><a href="/contribute/accepted/" style="background-color:orange; color:white; border-radius:5px; padding:5px">
                            <b>Review Existing Changes</b>
                            </a></li>
                        </ul>
                        """.format(username=request.user.username)
    else:
        bannerright = """
                        Help keep track of our changing world.
			<br>
			<br>
			<br>
			<a href="/registration" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Sign Up
			</a>
			or
			<a href="/login" style="background-color:orange; color:white; border-radius:10px; padding:10px; font-family:inherit; font-size:inherit; font-weight:bold; text-decoration:underline; margin:10px;">
			Login
			</a>
			"""
    grids = []
    grids.append(dict(title="What is Pshapes?",
                      content="""
                        <p style="color:black;">
                        <em><b><q>%s</q></b></em>
                        </p>
                        <div style="text-align:right;">
                        <a href="/about" style="color:white;"><b>Read More</b></a>
                        </div>
                        """%shortdescr
                      ))
    grids.append(dict(title="The Timecapsule:",
                  content="""
		<a href="/interactive" style="text-decoration:none;">		
		<table style="width:100%; border-radius:10px; padding:0% 0%; margins:0% 0%; background:linear-gradient(to left, rgba(255,165,0,0), rgba(255,165,0,1));">
		<tr>
		<td>
		<h4 style="color:black;">
		Go back in time to find out what the political landscape looked like at a particular date with our interactive time-enabled map.
		</h4>
		</td>
		
		<td>
		<img style="height:100px" src="http://cdn.shopify.com/s/files/1/0297/6893/products/Rapport_Optima_Single_Time_Capsule_Watch_Winder_W193_profile_front.png?v=1445374446">
		</td>
		
		</tr>
		</table>
		
		</a>
                """,
                style="padding:0% 0%; background-size:100% 100%; background-image:url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxvPpRIf5PnwOmOqIz47XUiU99_7XhcfelMm5iiTrKbYiIoSXi)",
                  ))
    
    grids.append(dict(title="Recent Additions:",
                      content=recentadds(request),
                      style="background-color:white; margins:0 0; padding: 0 0; border-style:none",
                      ))
    
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

def about(request):
    return render(request, 'pshapes_site/about.html')

def about(request):
    grids = []
    bannertitle = "About Pshapes"
    bannerleft = """
                <div style="text-align:left">
                %s
                </div>
                """ % shortdescr
    bannerright = ""
    grids.append(dict(title="Contact",
                      content="""
                            The Pshapes concept and website was created by Karim Bahgat in 2015-2016. 

                            <br><br>

                            He can be contacted at karim.bahgat.norway@gmail.com. 
                            """
                      ))
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

def testgrid(request):
    grids = tuple([("title%s"%i, "content%s"%i) for i in range(5)])
    bannertitle = "Banner Title"
    bannerleft = "Banner left"
    bannerright = "Banner right"
    return render(request, 'pshapes_site/base_grid.html', {"grids":grids,"bannertitle":bannertitle,
                                                           "bannerleft":bannerleft, "bannerright":bannerright}
                  )

