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
    url('^$', "cshapes.views.mapview_lite"),
    url('^method/$', "pshapes_site.views.method"),
    url('^download/$', "pshapes_site.views.download"),
    url('^contact/$', "pshapes_site.views.contact"),

    url('^dashboard/$', "provchanges.views.dashboard"),
    url('^submitchange/$', "provchanges.views.submitchange"),
    url(r'^provchange/(?P<pk>[0-9]+)/edit/$', "provchanges.views.editchange", name="editchange"),

    url('^registration/$', "provchanges.views.registration"),
    url('^login/$', "provchanges.views.login"),
    url('^logout/$', "provchanges.views.logout"),
    
    url('^timetest/$', "cshapes.views.mapview"),
    url(r'^admin/$', include(admin.site.urls)),
]

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns.extend([
                    url(r'^api/cshapes/$', "cshapes.views.apiview")
                    ])
