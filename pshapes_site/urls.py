"""pshapes_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib.gis import admin

admin.site.site_header = "Pshapes Website Admin"

urlpatterns = [

    # -----
    # HOME
    url('^$', "pshapes_site.views.home"),


    # ------------
    # INTERACTIVE
    url('^explore/$', "provshapes.views.explore"),


    # -----------
    # CONTRIBUTE
    #url('^contribute/$', "provchanges.views.contribute"),
    #url('^guidelines/$', "provchanges.views.guidelines_understanding"),
    #url('^guidelines/understanding/$', "provchanges.views.guidelines_understanding"),
    #url('^guidelines/codingrules/$', "provchanges.views.guidelines_codingrules"),
    #url('^guidelines/mapping/$', "provchanges.views.guidelines_mapping"),

    # country
    url('^contribute/view/(?P<country>[^/]+)/$', "provchanges.views.viewcountry"),
    url('^contribute/add/$', "provchanges.views.addcountry"),
    url('^contribute/edit/(?P<country>[^/]+)/$', "provchanges.views.editcountry"),

    # province (event or change depending on get params)
    url('^contribute/countries/$', "provchanges.views.allcountries"), 
    url('^contribute/view/(?P<country>[^/]+)/(?P<province>[^/]+)/$', "provchanges.views.viewprov"), # event
    url('^contribute/add/(?P<country>[^/]+)/$', "provchanges.views.addprov"),
    url('^contribute/add/(?P<country>[^/]+)/(?P<province>[^/]+)/$', "provchanges.views.addprov"),
    url('^contribute/edit/(?P<country>[^/]+)/(?P<province>[^/]+)/$', "provchanges.views.editprov"), # event

    # provchange (should be phased out, maybe allow via get param instead?)
    url(r'^provchange/(?P<pk>[0-9]+)/edit/$', "provchanges.views.editchange", name="editchange"),
    url(r'^provchange/(?P<pk>[0-9]+)/view/$', "provchanges.views.viewchange", name="viewchange"),
    url(r'^provchange/(?P<pk>[0-9]+)/withdraw/$', "provchanges.views.withdrawchange"),
    url(r'^provchange/(?P<pk>[0-9]+)/resubmit/$', "provchanges.views.resubmitchange"),
    url(r'^provchange/(?P<pk>[0-9]+)/addvouch/$', "provchanges.views.addvouch"),
    url(r'^provchange/(?P<pk>[0-9]+)/withdrawvouch/$', "provchanges.views.withdrawvouch"),

    url(r'^addissue/$', "provchanges.views.addissue"),
    url(r'^addissuecomment/$', "provchanges.views.addissuecomment"),
    url(r'^editissue/(?P<pk>[0-9]+)/$', "provchanges.views.editissue"),
    url(r'^viewissue/(?P<pk>[0-9]+)/$', "provchanges.views.viewissue"),
    url(r'^dropissue/(?P<pk>[0-9]+)/$', "provchanges.views.dropissue"),
    url(r'^dropissuecomment/(?P<pk>[0-9]+)/$', "provchanges.views.dropissuecomment"),
    
    url(r'^addsource/$', "provchanges.views.addsource"),
    url(r'^viewsource/(?P<pk>[0-9]+)/$', "provchanges.views.viewsource"),
    url(r'^editsource/(?P<pk>[0-9]+)/$', "provchanges.views.editsource"),
    url(r'^dropsource/(?P<pk>[0-9]+)/$', "provchanges.views.dropsource"),

    url(r'^addmap/$', "provchanges.views.addmap"),
    url(r'^viewmap/(?P<pk>[0-9]+)/$', "provchanges.views.viewmap"),
    url(r'^editmap/(?P<pk>[0-9]+)/$', "provchanges.views.editmap"),
    url(r'^dropmap/(?P<pk>[0-9]+)/$', "provchanges.views.dropmap"),



    # -----
    # DATA
    url('^download/$', "pshapes_site.views.download"),
    url('^download/final/$', "pshapes_site.views.download_final"),
    url('^download/raw/$', "pshapes_site.views.download_raw"),
    


    # ------
    # ABOUT
    url('^about/$', "pshapes_site.views.about"),
    url('^about/motivation/$', "pshapes_site.views.about_motivation"),
    url('^about/otherdata/$', "pshapes_site.views.about_otherdata"),
    url('^about/whycrowdsourcing/$', "pshapes_site.views.about_whycrowdsourcing"),
    url('^about/tutorial/$', "pshapes_site.views.about_tutorial"),
    url('^about/contact/$', "pshapes_site.views.about_contact"),



    # --------
    # (USERS)
    url('^account/$', "provchanges.views.account"),
    url('^account/edit/$', "provchanges.views.account_edit"),
    url('^registration/$', "provchanges.views.registration"),
    url('^login/$', "provchanges.views.login"),
    url('^logout/$', "provchanges.views.logout"),


    # -------
    # (TESTING)
    #url('^testgrid/$', "pshapes_site.views.testgrid"),
    #url('^timetest/$', "cshapes.views.mapview"),
    #url('^advanced/$', "provchanges.views.advancedchanges"),
    
    url('^update/$', "provshapes.views.update_dataset"),
    url('^api/$', "provshapes.views.apiview"),
    
    url(r'^admin/', include(admin.site.urls)),



    url('^migratecomments/$', "provchanges.views.migrate_comments"),


    
]

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns.extend([
                    url(r'^api/cshapes/$', "cshapes.views.apiview")
                    ])
