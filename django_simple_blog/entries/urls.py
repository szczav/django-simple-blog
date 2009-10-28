#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *

from entries.models import Entry
import entries.views as custom_views
from entries.feeds import *


mainpage_entries = 10   # number of pages on main page
entries_per_page = 20   # number of pages per page (without main page)


custom_list_fields = 'categories|tags'

mainpage_entries_list_dict = {'queryset'   : Entry.objects.all(),
                              'paginate_by': mainpage_entries}
entries_list_dict = {'queryset'   : Entry.objects.all(),
                     'paginate_by': entries_per_page}
entries_custom_list_dict = {'paginate_by': entries_per_page}
entries_archive_month_dict = {'queryset'    : Entry.objects.all(),
                              'date_field'  : 'creation_time',
                              'month_format': '%B',
                              'allow_empty' : True}
entry_detail_dict = {'queryset': Entry.objects.all()}

feed_dict = {'latest'  : LatestEntries,
             'category': LatestEntriesByCategory,
             'tag'     : LatestEntriesByTag}


urlpatterns = patterns('',
    # entries list
    url(r'^/?$', 'django.views.generic.list_detail.object_list', mainpage_entries_list_dict, 'entries-main'),
    url(r'^entries/(?P<page>\d+)/$', 'django.views.generic.list_detail.object_list', entries_list_dict, name='entries-archive'),

    # entries list by custom field
    url(r'^entries/(?P<option>%s)/index/$' % custom_list_fields, custom_views.custom_list_index, name='entries-index-custom'),
    url(r'^entries/(?P<option>%s)/(?P<slug>[^\.]+)/(?P<page>\d+)/$' % custom_list_fields, custom_views.custom_list, entries_custom_list_dict, 'entries-archive-custom'),

    # entries list by month
    url(r'^entries/(?P<year>\w{4})/(?P<month>\w+)/$', 'django.views.generic.date_based.archive_month', entries_archive_month_dict, 'entries-archive-bymonth'),

    # entry detail
    url(r'^entries/(?P<slug>[^\.]+)/$', 'django.views.generic.list_detail.object_detail', entry_detail_dict, 'entries-detail'),

    # comments
    url(r'^comments/', include('django.contrib.comments.urls')),

    # rss
    url(r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feed_dict}, 'entries-feeds'),
)