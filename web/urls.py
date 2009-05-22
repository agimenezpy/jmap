from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'jma.main.views.default', {'page' : 'index.html'}),
    (r'^([^/]+.html)$', 'jma.main.views.default'),
    (r'^([^/]+.xhr)$', 'jma.main.views.xhr'),
)
