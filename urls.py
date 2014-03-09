# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$$',     index,  {'template':'content_by_school.html'},      name='home'),
    url(r'^$$',     TemplateView.as_view(template_name="index.html"),   name='home'),
    url(r'',        include('social_auth.urls')),
    #url(r'^go$',    golink, {'template':'framed_link_content.html'},    name='golink'),
    
    (r'^content/',  include('content.urls')),
    (r'^read/',     include('read.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    #(r'^ad/',      include('adsys.urls')),
)

