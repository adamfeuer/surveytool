from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('userena.urls')),
    url(r'^accounts/(?P<username>[\.\w]+)/surveys/$', 'sms.views.surveys_select', name='userena_surveys_select'),
    (r'^messages/', include('userena.contrib.umessages.urls')),
    url(r'^$',
        direct_to_template,
        {'template': 'static/home.html'},
        name='home'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^sms/sms$', 'sms.views.sms', name="sms"),
    url(r'^sms/projects$', 'sms.views.projects', name="projects"),
    url(r'^sms/new_project$', 'sms.views.new_project', name="new_project"),
    url(r'^sms/save_project$', 'sms.views.save_project', name="save_project"),
    (r'^sms/delete_project/(?P<project_id>\d+)/$', 'sms.views.delete_project'),
    (r'^sms/project/(?P<project_id>\d+)/$', 'sms.views.project'),
    url(r'^sms/messages$', 'sms.views.messages', name="messages"),
    url(r'^sms/new_message$', 'sms.views.new_message', name="new_message"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True, }),
)
