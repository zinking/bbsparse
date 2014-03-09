from django.conf.urls.defaults import *;

from django.contrib.auth import views as auth_views;

from content.views import *;

urlpatterns = patterns('',
    url(r'^linkbyschools.json$', linkbyschools, {}, name='linkbyschools'),
)

"""
url(r'^management/home/$', manangement, 
    {'template': 'admin_interface.html'} ,      name='mgmthome'),
url(r'^management$', admin_db_op, 
    {'template': 'default.html'} ,              name='adminop'),
    
url(r'^management/cron/$',  gae_cron_job_parse, 
    {'template': 'cron_result.html'} ,          name='mgmtcron'),
url(r'^management/mblog/$', gae_cron_job_sendblog, 
    {'template': 'cron_mblog_result.html'} ,    name='mgmtcron_mblog'),
url(r'^management/setup/$', gae_setup_initial_data, 
    {'template': 'cron_result.html'} ,          name='mgmtstup'),
    
    url(r'^go$',viewframedcontentV2, {'template':'framed_link_content.html'},    name='content_framed_detailV2'),
    url(r'^status/$',view_parsing_status,  {'template':'school_status_list.html'},     name='view_parsing_status'),
"""
