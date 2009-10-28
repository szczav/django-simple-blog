#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms.util import smart_unicode


class Link(models.Model):
    """
    Model for links to other websites.
    """
    title = models.CharField(_('Title'), max_length=50)
    url = models.URLField(_('URL'))

    def __unicode__(self):
        return smart_unicode(self.title)

    class Meta:
        ordering = ['title', 'url']
        verbose_name = _('Link')
        verbose_name_plural = _('Links')