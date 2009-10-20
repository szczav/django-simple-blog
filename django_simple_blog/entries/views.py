#-*- coding: utf-8 -*-
from django.views.generic import list_detail
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.db.models import Count

from models import Entry


def custom_list(request, option, slug, page, paginate_by=10, template_name='entries/entry_custom_list.html'):
    page = int(page) if page else 1

    model = Entry.__dict__[option].field.rel.to
    title = get_object_or_404(model, slug=slug).name
    verbose_name = model._meta.verbose_name.__unicode__()
    title = "%s: %s" % (verbose_name, title)

    entries = Entry.objects.filter(**{str(option+'__slug') : slug})
    paginator = Paginator(entries, paginate_by)

    try:
        page_entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page_entries = paginator.page(paginator.num_pages)

    return list_detail.object_list(request, 
                                   page_entries.object_list,
                                   paginate_by=paginate_by,
                                   template_name=template_name,
                                   extra_context={'has_next'    : page_entries.has_next(),
                                                  'next'        : page+1,
                                                  'has_previous': page_entries.has_previous(),
                                                  'previous'    : page-1,
                                                  'option'      : option,
                                                  'title'       : title,
                                                  'slug'        : slug })

def custom_list_index(request, option, template_name='entries/entry_custom_index.html'):
    model = Entry.__dict__[option].field.rel.to
    queryset = model.objects.annotate(entries_count=Count('entry'))
    verbose_name = model._meta.verbose_name.lower()
    title = _('Entries by %s' % verbose_name)
    return render_to_response(template_name,
                              {'object_list' : queryset,
                               'option'      : option,
                               'title'       : title},
                               context_instance=RequestContext(request))
