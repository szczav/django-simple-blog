#-*- coding: utf-8 -*-
from django import template
from django.db.models import Count
from django.core.urlresolvers import reverse

from entries.models import Tag, Entry

register = template.Library()


@register.inclusion_tag('tags.html')
def show_tags(tag_num):
    tags = Tag.objects.annotate(entries_count=Count('entry')).order_by('-entries_count')[:tag_num]
    entries_count = tags.values_list('entries_count', flat=True)
    if entries_count.count() == 0:
        return {'tags': {}}

    all_entries_count = max(entries_count)
    tags_dict = tags.values('name', 'slug', 'entries_count')

    for tag in tags_dict:
        try:
            tag['font'] = float(tag['entries_count']) / all_entries_count * 200
        # if there aren't any entries connected with this tag
        except ZeroDivisionError:
            del tag
    return {'tags': tags_dict}

@register.inclusion_tag('entries/archive_bymonth.html')
def show_archive_bymonth(month_num):
    months = Entry.objects.all().dates('creation_time', 'month', 'DESC')[:month_num]
    return {'months': months}

@register.simple_tag
def show_feeds(option=None, slug=None, object_name=None):
    if option is not None and slug is not None:
        if option == 'categories':
            return ', <a href="%s">%s</a>' % (reverse('entries-feeds', args=['category/%s' % slug]), object_name)
        elif option == 'tags':
            return ', <a href="%s">%s</a>' % (reverse('entries-feeds', args=['tag/%s' % slug]), object_name)
    return ''
