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
    url(r'^dynamic/style.less$', 'relearn.views.css', name='css'),
    url(r'^publish/$', 'relearn.views.publish', name='publish'),
    url(r'^dynamic/print.less$', 'relearn.views.cssprint', name='css-print'),
    url(r'^offset-print/$', 'relearn.views.offsetprint', name='offset-print'),
    url(r'^$', 'relearn.views.home', name='home'),
    url(r'^sorted/by/(?P<key>[^/]+)/$', 'relearn.views.home', name='sorted'),
    url(r'^(?P<slug>[^/]+)\.xhtml$', 'relearn.views.xhtml', name='xhtml'),
    url(r'^accounts/login$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout$', 'django.contrib.auth.views.logout',
        {'template_name': 'logout.html'}, name='logout'),
    url(r'^create/$', 'relearn.views.padCreate', name='pad-create'),
    url(r'(?P<mode>[r|p])/(?P<slug>[^/]+)$', 'relearn.views.pad_read', name='pad-read'),
    url(r'w/(?P<slug>[^/]+)$', 'relearn.views.pad', name='pad-write'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

