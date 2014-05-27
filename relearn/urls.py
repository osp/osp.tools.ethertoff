from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.http import HttpResponse

from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^all/$', TemplateView.as_view(template_name = 'all.html'), name='all'),
    url(r'^css/$', 'relearn.views.css', name='css'),
    url(r'^$', 'relearn.views.home', name='home'),
    url(r'^accounts/login$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout$', 'django.contrib.auth.views.logout',
        {'template_name': 'logout.html'}, name='logout'),
    url(r'^accounts/profile$', 'relearn.views.profile', name='profile'),
    url(r'^etherpad/create/(?P<pk>\d+)/$', 'relearn.views.padCreate', name='pad-create'),
    url(r'^etherpad/delete/(?P<pk>\d+)/$', 'relearn.views.padDelete', name='pad-delete'),
    url(r'^group/create$', 'relearn.views.groupCreate'),
    url(r'r/(?P<slug>[\w\.\-_\:]+)$', 'relearn.views.pad_read', name='pad-read'),
    url(r'w/(?P<slug>[\w\.\-_\:]+)$', 'relearn.views.pad', name='pad-write'),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

