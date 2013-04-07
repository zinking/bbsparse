from django.conf.urls.defaults import *

rootpatterns = patterns('',
    (r'^ad/', include('adsys.urls')),
)
