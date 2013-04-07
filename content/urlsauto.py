from django.conf.urls.defaults import *

rootpatterns = patterns('',
    (r'^content/', include('content.urls')),
)
