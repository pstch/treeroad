from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^servInfo/$', 'treeroad.views.servInfo'),
    url(r'^graphTask/$', 'treeroad.views.graphTaskView'),
)
