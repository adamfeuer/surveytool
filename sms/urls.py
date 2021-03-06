from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    (r'^$', 'sms.views.sms'),  
    url(r'^sms$', 'sms.views.sms', name="sms"),
    url(r'^projects$', 'sms.views.projects', name="projects"),
    url(r'^new_project$', 'sms.views.new_project', name="new_project"),
    url(r'^save_project$', 'sms.views.save_project', name="save_project"),
    (r'^delete_project/(?P<project_id>\d+)/$', 'sms.views.delete_project'),
    (r'^edit_project/(?P<project_id>\d+)/$', 'sms.views.edit_project'),
    (r'^project_messages_csv/(?P<project_id>\d+)/$', 'sms.views.project_messages_csv'),
    (r'^project_intake_ids_csv/(?P<project_id>\d+)/$', 'sms.views.project_intake_ids_csv'),
    url(r'^messages$', 'sms.views.messages', name="messages"),
    url(r'^new_message$', 'sms.views.new_message', name="new_message"),
    (r'^delete_message/(?P<message_id>\d+)/$', 'sms.views.delete_message'),
    (r'^edit_message/(?P<message_id>\d+)/$', 'sms.views.edit_message'),
    url(r'^save_message$', 'sms.views.save_message', name="save_message"),
    (r'^messages_for_project/(?P<project_id>\d+)/$', 'sms.views.messages_for_project'),
    (r'^delete_messages/(?P<project_id>\d+)/$', 'sms.views.delete_messages_for_project'),
    (r'^generate_messages/(?P<project_id>\d+)/$', 'sms.views.generate_messages'),
    url(r'^make_signup_url$', 'sms.views.make_signup_url', name="make_signup_url"),
)
