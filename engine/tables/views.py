import json
from django.shortcuts import render
from django.http import HttpResponse

from . import models


def page(request):
    short = request.GET['short']
    if models.Page.objects.filter(short=short).count() > 0:
        return HttpResponse('')

    cat = request.GET['cat']
    name = request.GET['name']
    url = request.GET['url']

    page = models.Page(cat=cat, short=short, name=name, url=url)
    page.save()

    return HttpResponse('')


def pub(request):
    short = request.GET['short']
    name = request.GET['name']

    authors = json.loads(request.GET['authors'])

    page = models.Page.objects.get(short=short)
    pub = models.Publication(page=page, name=name)
    pub.save()

    for short in authors:
        author = models.Page.objects.get(short=short)
        relation = models.PublicationAuthor(pub=pub, author=author)
        relation.save()

    return HttpResponse('')
