#from django.conf.urls.defaults import patterns, include, url
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from content.views import viewframedcontentV2 as golink;
from content.views import viewbyschool as index;

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bbs_dig.views.home', name='home'),
    # url(r'^bbs_dig/', include('bbs_dig.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$$',     index,  {'template':'content_by_school.html'},      name='home'),
    url(r'^go$',    golink, {'template':'framed_link_content.html'},    name='golink'),
    
    (r'^content/',  include('content.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    #(r'^ad/',      include('adsys.urls')),
)

