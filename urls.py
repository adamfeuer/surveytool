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
    url(r'^signup/(?P<surveys>[\.\w]+)/$', 'sms.views.one_page_signup'),
    url(r'^$',
        direct_to_template,
        {'template': 'static/home.html'},
        name='home'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^sms/',      include('sms.urls')),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True, }),
)
