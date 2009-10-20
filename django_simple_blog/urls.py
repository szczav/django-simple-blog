#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap, FlatPageSitemap

from entries.models import Entry

admin.autodiscover()


sitemaps_dict = {'articles': GenericSitemap({'queryset'  : Entry.objects.all(),
                                             'date_field': 'modification_time'}, priority=0.7),
                 'flatpages': FlatPageSitemap}


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps_dict}),
    url(r'^contact/', include('contact.urls')),
    url(r'', include('entries.urls')),
)
