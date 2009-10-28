#-*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _

from contact.forms import ContactForm


def contact(request, contact_form=ContactForm, template_name='contact/form.html'):
    """
    Create contact form or send message (after proper validation) to admin's
    email (set in settings.py).
    """
    if request.method == 'POST':
        form = contact_form(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender_name = form.cleaned_data['sender_name']
            sender_email = form.cleaned_data['sender_email']
            cc_myself = form.cleaned_data['cc_myself']

            admin_email = settings.ADMINS[0][1]
            recipients = [admin_email,]
            if cc_myself:
                recipients.append(sender_email)

            site_name = Site.objects.get(pk=settings.SITE_ID).name

            try:
                send_mail(subject, _("Mail from %s %s\n\n %s" % (site_name, message, sender_name)), sender_email, recipients)
            except BadHeaderError:
                return HttpResponseRedirect(reverse('contact-error'))
            return HttpResponseRedirect(reverse('contact-confirmation'))
    else:
        form = contact_form()

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))
