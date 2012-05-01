from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^parseTree/$', 'treeroad.views.parseTree'), # View for parsing the /var/lib/collectd/rrd/* path tree. Should be included into the Admin website later, however it has been implemented earlier for debug purposes.
    url(r'^parseTree/noTest$', 'treeroad.views.parseTree', { 'test' : 0 }), # View for parsing the /var/lib/collectd/rrd/* path tree. Should be included into the Admin website later, however it has been implemented earlier for debug purposes.
    url(r'^servInfo/$', 'treeroad.views.servInfo'),
)
