from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from treeroad.models import node, service, graph

urlpatterns = patterns('',
    url(r'^servInfo/$', 'treeroad.views.servInfo'),
    url(r'^overView$', 'treeroad.views.overView'),
    
    url(r'^nodes/$', ListView.as_view(model=node)),
    url(r'^nodes/(?P<pk>\d+)$', DetailView.as_view(model=node)),
    
    url(r'^services/$', ListView.as_view(model=service)),
    url(r'^services/(?P<pk>\d+)$', DetailView.as_view(model=service)),
    
    url(r'^graphs/$', ListView.as_view(model=graph)),
    url(r'^graphs/(?P<pk>\d+)$', DetailView.as_view(model=graph)),
)
