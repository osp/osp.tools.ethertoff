from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from etherpadlite.models import *

urlpatterns = patterns(
    '',
    url(r'^$', 'django.contrib.auth.views.login',
        {'template_name': 'etherpad-lite/login.html'}, name='home'),
    url(r'^etherpad$', 'django.contrib.auth.views.login',
        {'template_name': 'etherpad-lite/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout',
        {'template_name': 'etherpad-lite/logout.html'}, name='logout'),
    url(r'^accounts/profile/$', 'relearn.views.profile'),
    url(r'^etherpad/(?P<pk>\d+)/$', 'relearn.views.pad'),
    url(r'^etherpad/create/(?P<pk>\d+)/$', 'relearn.views.padCreate', name='pad-create'),
    url(r'^etherpad/delete/(?P<pk>\d+)/$', 'relearn.views.padDelete', name='pad-delete'),
    url(r'^group/create/$', 'relearn.views.groupCreate'),
    
    # That needs to change to a special view for rendering:
    url(r'r/(?P<slug>[\w\.\-_\:]+)/$', 'relearn.views.pad', name='pad-read'),
    
    url(r'w/(?P<slug>[\w\.\-_\:]+)/$', 'relearn.views.pad', name='pad-write'),
    
    
    url(r'^admin/', include(admin.site.urls)),

    (r'^tracker/$', TemplateView.as_view(template_name="tracker.html")),
)

