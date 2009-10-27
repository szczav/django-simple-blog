#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *

import contact.views as custom_views


urlpatterns = patterns('',
    url(r'^confirmation/$', 'django.views.generic.simple.direct_to_template', {'template': 'contact/confirmation.html'}, 'contact-confirmation'),
    url(r'^error/$', 'django.views.generic.simple.direct_to_template', {'template': 'contact/error.html'}, 'contact-error'),
    url(r'', custom_views.contact, name='contact-form'),
)