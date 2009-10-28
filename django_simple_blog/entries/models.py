#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms.util import smart_unicode
from django.contrib.auth.models import User
from django.contrib.sitemaps import ping_google
from django.db.models import permalink


class Category(models.Model):
    """
    Entries categories.
    """
    name = models.CharField(_('Category'), max_length=50, unique=True)
    slug = models.SlugField(_('Slug'), unique=True)

    def __unicode__(self):
        return smart_unicode(self.name)

    @permalink
    def get_absolute_url(self):
        return ('entries-archive-custom', None, {'option': 'categories',
                                                 'slug'  : self.slug,
                                                 'page'  : '1'})

    class Meta:
        ordering = ['name',]
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Tag(models.Model):
    name = models.CharField(_('Tag'), max_length=30, unique=True)
    slug = models.SlugField(_('Slug'), max_length=30, unique=True)

    def __unicode__(self):
        return smart_unicode(self.name)

    @permalink
    def get_absolute_url(self):
        return ('entries-archive-custom', None, {'option': 'tags',
                                                 'slug'  : self.slug,
                                                 'page'  : '1'})

    class Meta:
        ordering = ['name',]
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

class Entry(models.Model):
    title = models.CharField(_('Topic'), max_length=100)
    slug = models.SlugField(_('Slug'), max_length=100, unique=True)
    categories = models.ManyToManyField(Category, verbose_name=_('Category'))
    tags = models.ManyToManyField(Tag, verbose_name=_('Tags'))
    content = models.TextField(_('Content'))
    author = models.ForeignKey(User, verbose_name=_('Author'))
    creation_time = models.DateTimeField(_('Creation time'), auto_now_add=True)
    modification_time = models.DateTimeField(_('Modification time'), auto_now=True)

    # ping google (works only if website is registered on Google Webmaster Tools)
    def save(self, force_insert=False, force_update=False):
        super(Entry, self).save(force_insert, force_update)
        try:
            ping_google()
        except Exception:
            pass

    def __unicode__(self):
        return smart_unicode(self.title)

    @permalink
    def get_absolute_url(self):
        return ('entries-detail', None, {'slug' : self.slug})

    class Meta:
        ordering = ['-creation_time', '-modification_time', 'title']
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')


