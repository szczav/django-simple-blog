#-*- coding: utf-8 -*-
from django.views.generic import list_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.db.models import Count

from entries.models import Entry


def custom_list(request, option, slug, page, paginate_by=10, template_name='entries/entry_custom_list.html'):
    model = Entry.__dict__[option].field.rel.to
    title = get_object_or_404(model, slug=slug).name
    verbose_name = model._meta.verbose_name.__unicode__()
    title = "%s: %s" % (verbose_name, title)
    entries = Entry.objects.filter(**{str(option+'__slug') : slug})

    try:
        page = int(page)
    except ValueError:
        page = 1

    return list_detail.object_list(request, 
                                   entries,
                                   paginate_by=paginate_by,
                                   page=page,
                                   template_name=template_name,
                                   extra_context={'option': option,
                                                  'title' : title,
                                                  'slug'  : slug})

def custom_list_index(request, option, template_name='entries/entry_custom_index.html'):
    model = Entry.__dict__[option].field.rel.to
    entries = model.objects.annotate(entries_count=Count('entry'))
    verbose_name = model._meta.verbose_name.lower()
    title = _('Entries by %s' % verbose_name)

    return render_to_response(template_name,
                              {'object_list': entries,
                               'option'     : option,
                               'title'      : title},
                               context_instance=RequestContext(request))
