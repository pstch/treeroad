from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from adminplus import AdminSitePlus

#admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^treeroad/', include('area13.treeroad.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
