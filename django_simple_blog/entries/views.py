#-*- coding: utf-8 -*-
from django.views.generic import list_detail
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Count

from entries.models import Entry


def custom_list(request, option, slug, page, paginate_by=10, template_name='entries/entry_custom_list.html'):
    """
    List of entries with have entry field (option) value set to slug.
    Supports pagination.
    """
    model = Entry.__dict__[option].field.rel.to
    object_name = get_object_or_404(model, slug=slug).name
    model_verbose_name = model._meta.verbose_name.__unicode__()
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
                                                  'object_name': object_name,
                                                  'model_verbose_name': model_verbose_name,
                                                  'slug': slug})

def custom_list_index(request, option, template_name='entries/entry_custom_index.html'):
    """
    Index of custom entry field (option) leading to custom_list view for
    specified value.
    """
    model = Entry.__dict__[option].field.rel.to
    entries = model.objects.annotate(entries_count=Count('entry'))
    verbose_name = model._meta.verbose_name.lower()

    return render_to_response(template_name,
                              {'object_list': entries,
                               'option': option,
                               'verbose_name': verbose_name},
                               context_instance=RequestContext(request))
