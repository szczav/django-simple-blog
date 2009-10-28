#-*- coding: utf-8 -*-
from django.contrib.syndication.feeds import Feed
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.conf import settings

from entries.models import Entry, Category, Tag


site_name = Site.objects.get(pk=settings.SITE_ID).name


class LatestEntries(Feed):
    """
    Main feed - shows latest entries in blog (doesn't matter from which
    category).
    """
    title = site_name
    description = _("Latest entries")
    link = "/"
    title_template = "feeds/latest_title.html"
    description_template = "feeds/latest_description.html"

    def items(self):
        return Entry.objects.all()[:10]

class LatestEntriesByCategory(Feed):
    """
    Show latest entries from chosen category.
    """
    title = site_name
    link = "/"
    title_template = "feeds/latest_title.html"
    description_template = "feeds/latest_description.html"

    def description(self, obj):
        return _("Latest entries from category %s" % obj.name)

    def get_object(self, extra_params):
        if len(extra_params) != 1:
            raise ObjectDoesNotExist
        category_slug = extra_params[0]
        return Category.objects.get(slug=category_slug)

    def items(self, obj):
        return Entry.objects.filter(categories=obj)[:10]

class LatestEntriesByTag(Feed):
    """
    Show latest entries which were conected with chosen tag.
    """
    title = site_name
    link = "/"
    title_template = "feeds/latest_title.html"
    description_template = "feeds/latest_description.html"

    def description(self, obj):
        return _("Latest entries from tag %s" % obj.name)

    def get_object(self, extra_params):
        if len(extra_params) != 1:
            raise ObjectDoesNotExist
        tag_slug = extra_params[0]
        return Tag.objects.get(slug=tag_slug)

    def items(self, obj):
        return Entry.objects.filter(tags=obj)[:10]
