from django.conf.urls.defaults import *;

from django.contrib.auth import views as auth_views;

from content.views import *;

urlpatterns = patterns('',
    url(r'^linkbyschools.json$', linkbyschools, {}, name='linkbyschools'),
    url(r'^status/$',view_parsing_status,  {'template':'status.html'},     name='view_parsing_status'),
    url(r'^go$',viewframedcontentV2, {'template':'frame.html'},    name='content_framed_detailV2'),
)

