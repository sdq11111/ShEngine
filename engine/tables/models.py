from __future__ import unicode_literals

from django.db import models


class Page(models.Model):
    CATEGORIES = (
        ('A', 'Author'),
        ('J', 'Journal'),
        ('JS', 'Journal-Sub'),
        ('C', 'Conference'),
        ('CS', 'Conference-Sub')
    )
    cat = models.CharField(max_length=2, choices=CATEGORIES)
    short = models.TextField()
    name = models.TextField()
    url = models.TextField()


class Publication(models.Model):
    page = models.ForeignKey(Page)
    name = models.TextField()


class PublicationAuthor(models.Model):
    pub = models.ForeignKey(Publication)
    author = models.ForeignKey(Page)
