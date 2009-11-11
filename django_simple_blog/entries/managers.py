#-*- coding: utf-8 -*-
from django.db import models


class EntryRelatedManager(models.Manager):
    def get_query_set(self):
        return super(EntryRelatedManager, self).get_query_set().select_related()
