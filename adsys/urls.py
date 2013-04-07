from django.conf.urls.defaults import *;
from django.views.generic.simple import direct_to_template;
from django.contrib.auth import views as auth_views;

from adsys.views import *;

urlpatterns = patterns('',
    url(r'^admin$', ad_table_op, 
        {'template': 'default.html'},       name='adsystem_man'),
    url(r'^cron/$',  cron_avtars, 
        {'template': 'default.html'},       name='adsystem_cron'),
    url(r'^p$',  view_avtars, 
        {'template': 'default.html'},       name='adsystem_pic'),
    url(r'^comp/$',  cron_composer, 
        {'template': 'default.html'},       name='adsystem_comp'),
    
)
