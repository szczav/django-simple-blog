#-*- coding: utf-8 -*-
from django import template
from links.models import Link

register = template.Library()


@register.inclusion_tag('links/links.html')
def show_links():
    """
    Show links.
    """
    return {'links': Link.objects.all()}
