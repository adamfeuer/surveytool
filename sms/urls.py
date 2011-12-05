from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    (r'^$', 'sms.views.sms'),  
    (r'^$', 'sms.views.project'),  
)
