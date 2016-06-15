import os
import json
from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse

from . import models
from . import util


def init(request):
    client = MongoClient()
    db = client['sh-engine']
    engine = db['sh-engine']

    JOURNAL_CRALWED_FOLDER = os.path.join('link', 'journal')
    CONFERENCE_CRALWED_FOLDER = os.path.join('link', 'conference')

    cnt = 0
    files = util.listdir(JOURNAL_CRALWED_FOLDER)
    for file_name in files:
        data = util.load_json(os.path.join(JOURNAL_CRALWED_FOLDER, file_name))
        print cnt, len(files), data['name']
        for short, sub in data['sub'].items():
            print '\t', sub['name']
            for pub_data in sub['pub']:
                authors = []
                for author_data in pub_data['author']:
                    author = {
                        'name': author_data['name'],
                        'url': 'http://dblp.uni-trier.de/pers/hd/' + author_data['short']
                    }
                    authors.append(author)
                pub = {
                    'name': sub['name'],
                    'url': 'http://dblp.uni-trier.de/db/journals/' + short,
                    'title': pub_data['title'],
                    'authors': authors
                }
                engine.insert_one(pub)
        cnt += 1
        print cnt, len(files)

    cnt = 0
    files = util.listdir(CONFERENCE_CRALWED_FOLDER)
    for file_name in files:
        data = util.load_json(os.path.join(CONFERENCE_CRALWED_FOLDER, file_name))
        print cnt, len(files), data['name']
        for short, sub in data['sub'].items():
            print '\t', sub['name']
            for pub_data in sub['pub']:
                authors = []
                for author_data in pub_data['author']:
                    author = {
                        'name': author_data['name'],
                        'url': 'http://dblp.uni-trier.de/pers/hd/' + author_data['short']
                    }
                    authors.append(author)
                pub = {
                    'name': sub['name'],
                    'url': 'http://dblp.uni-trier.de/db/conf/' + short,
                    'title': pub_data['title'],
                    'authors': authors
                }
                engine.insert_one(pub)
        cnt += 1
        print cnt, len(files)


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
