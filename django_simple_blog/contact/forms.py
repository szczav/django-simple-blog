#-*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _


class ContactForm(forms.Form):
    subject = forms.CharField(label=_('Subject'), max_length=100)
    sender_name = forms.CharField(label=_('Name'), max_length=100, required=False)
    sender_email = forms.EmailField(label=_('Email'), required=False)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea(attrs={'rows':'5'}))
    cc_myself = forms.BooleanField(label=_('Send to myself'), required=False)
