from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.http import HttpResponse

from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# This is to allow the website to work under a subfolder
# i.e. http://relearn.be/2015/
# Define SUBFOLDER in your local_settings.py
BASE_URL = '^'
try:
    BASE_URL = r'^' + settings.SUBFOLDER
    if BASE_URL and not BASE_URL.endswith(r'/'):
        BASE_URL += r'/'
except AttributeError:
    pass

base_urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^all/$', TemplateView.as_view(template_name = 'all.html'), name='all'),
    url(r'^css/$', 'relearn.views.css', name='css'),
    url(r'^publish/$', 'relearn.views.publish', name='publish'),
    url(r'^css-print/$', 'relearn.views.cssprint', name='css-print'),
    url(r'^offset-print/$', 'relearn.views.offsetprint', name='offset-print'),
    url(r'^css-slide/$', 'relearn.views.css_slide', name='css-slide'),
    url(r'^$', 'relearn.views.home', name='home'),
    url(r'^(?P<slug>[^/]+)\.xhtml$', 'relearn.views.xhtml', name='xhtml'),
    url(r'^accounts/login$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout$', 'django.contrib.auth.views.logout',
        {'template_name': 'logout.html'}, name='logout'),
    url(r'^create/$', 'relearn.views.padCreate', name='pad-create'),
    url(r'(?P<mode>[r|p])/(?P<slug>[^/]+)$', 'relearn.views.pad_read', name='pad-read'),
    url(r'w/(?P<slug>[^/]+)$', 'relearn.views.pad', name='pad-write'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = patterns('',
    url(BASE_URL , include(base_urlpatterns)),
)
