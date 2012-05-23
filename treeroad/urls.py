from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from treeroad.models import node, service, graph

urlpatterns = patterns('',
    url(r'^$', 'treeroad.views.overView'),
    url(r'^servInfo$', 'treeroad.views.servInfo'),
    url(r'^nodes$', ListView.as_view(model=node), name='nodeList'),#IGNORE:E1120
    url(r'^node/(?P<pk>\d+)$', DetailView.as_view(model=node), name='nodeDetail'),#IGNORE:E1120
    url(r'^services$', ListView.as_view(model=service), name='serviceList'),#IGNORE:E1120
    url(r'^service/(?P<pk>\d+)$', DetailView.as_view(model=service), name='serviceDetail'),#IGNORE:E1120
    url(r'^graphs$', ListView.as_view(model=graph), name='graphList'),#IGNORE:E1120
    url(r'^graph/(?P<pk>\d+)$', DetailView.as_view(model=graph), name='graphDetail'),#IGNORE:E1120
)
