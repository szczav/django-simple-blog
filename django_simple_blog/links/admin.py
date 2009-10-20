#-*- coding: utf-8 -*-
from django.contrib import admin
from models import Link


class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    list_display_links = ('title', 'url')
    search_fields = ('title', 'url')


admin.site.register(Link, LinkAdmin)