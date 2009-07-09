from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^$', 'web.main.views.default', {'page' : 'index.html'}),
    (r'^([^/]+.html)$', 'web.main.views.default'),
    (r'^([^/]+.xhr)$', 'web.main.views.xhr'),
    (r'^(?P<method>\w+)/(?P<engine>\w+)/(.*)$', 'web.tiles.views.tiles_dispatcher'),
)
