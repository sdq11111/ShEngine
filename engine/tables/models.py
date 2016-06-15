from __future__ import unicode_literals

from django.db import models


class Page(models.Model):
    short = models.TextField(db_index=True)
    name = models.TextField()
    url = models.TextField()


class Publication(models.Model):
    page = models.ForeignKey(Page)
    name = models.TextField()
    authors = models.TextField()
