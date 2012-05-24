from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from django.http import HttpResponseRedirect
from adminplus import AdminSitePlus
from django.conf import settings
from django.conf.urls.static import static

#admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$',  lambda x: HttpResponseRedirect('/treeroad/')),
    url(r'^treeroad/', include('area13.treeroad.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
