# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from content.views import viewframedcontentV2 as golink;
from content.views import viewbyschool as index;


urlpatterns =  patterns('',
    url(r'^$$',     index,  {'template':'content_by_school.html'},      name='home'),
    url(r'^go$',    golink, {'template':'framed_link_content.html'},    name='golink'),
    
    (r'^content/',  include('content.urls')),
    #(r'^ad/',      include('adsys.urls')),
)

