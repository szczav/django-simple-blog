#-*- coding: utf-8 -*-
from django.contrib import admin
from models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_time', 'modification_time', 'author')
    list_display_links = ('title',)
    search_fields = ['title', 'content']
    list_filter = ('creation_time', 'modification_time')
    filter_horizontal = ('tags',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Entry, EntryAdmin)
