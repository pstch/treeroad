from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from treeroad.models import node, service, graph

urlpatterns = patterns('',
    url(r'^$', 'treeroad.views.overView'),
    url(r'^servInfo$', 'treeroad.views.servInfo'),
    
    url(r'^nodes$', ListView.as_view(model=node), name='nodeList'),
    url(r'^node/(?P<pk>\d+)$', DetailView.as_view(model=node), name='nodeDetail'),
    
    url(r'^services$', ListView.as_view(model=service), name='serviceList'),
    url(r'^service/(?P<pk>\d+)$', DetailView.as_view(model=service), name='serviceDetail'),
    
    url(r'^graphs$', ListView.as_view(model=graph), name='graphList'),
    url(r'^graph(?P<pk>\d+)$', DetailView.as_view(model=graph), name='graphDetail'),
)
