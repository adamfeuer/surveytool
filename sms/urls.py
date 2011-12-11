from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    (r'^$', 'sms.views.sms'),  
    url(r'^sms$', 'sms.views.sms', name="sms"),
    url(r'^projects$', 'sms.views.projects', name="projects"),
    url(r'^new_project$', 'sms.views.new_project', name="new_project"),
    url(r'^save_project$', 'sms.views.save_project', name="save_project"),
    (r'^delete_project/(?P<project_id>\d+)/$', 'sms.views.delete_project'),
    (r'^project/(?P<project_id>\d+)/$', 'sms.views.project'),
    url(r'^messages$', 'sms.views.messages', name="messages"),
    url(r'^new_message$', 'sms.views.new_message', name="new_message"),
    (r'^sms/delete_message/(?P<message_id>\d+)/$', 'sms.views.delete_message'),
)
