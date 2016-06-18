import os
import math
import json
import random
from HTMLParser import HTMLParser
import pymongo
from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse

#from . import util


def init(request):
    client = MongoClient()
    db = client['sh-engine']
    engine = db['sh-engine']

    JOURNAL_CRALWED_FOLDER = os.path.join('link', 'journal')
    CONFERENCE_CRALWED_FOLDER = os.path.join('link', 'conference')

    pub_cnt = 0

    cnt = 0
    files = util.listdir(JOURNAL_CRALWED_FOLDER)
    for file_name in files:
        data = util.load_json(os.path.join(JOURNAL_CRALWED_FOLDER, file_name))
        for short, sub in data['sub'].items():
            for pub_data in sub['pub']:
                authors = []
                for author_data in pub_data['author']:
                    author = {
                        'name': author_data['name'],
                        'url': 'http://dblp.uni-trier.de/pers/hd/' + author_data['short']
                    }
                    authors.append(author)
                try:
                    pub_data['title'] = HTMLParser().unescape(pub_data['title']).replace('/<br />', ' ')
                except:
                    pass
                pub = {
                    'name': sub['name'],
                    'url': 'http://dblp.uni-trier.de/db/journals/' + short,
                    'title': pub_data['title'],
                    'authors': authors
                }
                engine.insert_one(pub)
                pub_cnt += 1
        cnt += 1
        print cnt, len(files), pub_cnt

    cnt = 0
    files = util.listdir(CONFERENCE_CRALWED_FOLDER)
    for file_name in files:
        data = util.load_json(os.path.join(CONFERENCE_CRALWED_FOLDER, file_name))
        for short, sub in data['sub'].items():
            for pub_data in sub['pub']:
                authors = []
                for author_data in pub_data['author']:
                    author = {
                        'name': author_data['name'],
                        'url': 'http://dblp.uni-trier.de/pers/hd/' + author_data['short']
                    }
                    authors.append(author)
                try:
                    pub_data['title'] = HTMLParser().unescape(pub_data['title']).replace('/<br />', ' ')
                except:
                    pass
                pub = {
                    'name': sub['name'],
                    'url': 'http://dblp.uni-trier.de/db/conf/' + short,
                    'title': pub_data['title'],
                    'authors': authors
                }
                engine.insert_one(pub)
                pub_cnt += 1
        cnt += 1
        print cnt, len(files), pub_cnt
    return HttpResponse("")


def split_to_words(s):
    words = []
    last_word = ''
    s = s.lower()
    for c in s:
        if 'a' <= c and c <= 'z':
            last_word += c
        else:
            if len(last_word) > 0:
                words.append(last_word)
            last_word = ''
    if len(last_word) > 0:
        words.append(last_word)
    return words


def words(request):
    client = MongoClient()
    db = client['sh-engine']
    engine = db['sh-engine']
    #db.drop_collection('words')
    db_words = db['words']
    db_words.create_index([('word', pymongo.ASCENDING)], unique=True)
    word_dict = {}
    cnt = 0
    seg = 10000
    for i in xrange(0, engine.count() // seg * seg + seg, seg):
        pub_data = []
        for pub in engine.find(skip=i, limit=seg):
            pub_data.append(pub)
        temp_dict = {}
        for pub in pub_data:
            if cnt < 2390000:
                cnt += 1
                continue
            pub_id = pub['_id']
            title = pub['title']
            words = set(split_to_words(title))
            for word in words:
                if word not in temp_dict:
                    temp_dict[word] = []
                temp_dict[word].append(pub_id)
            cnt += 1
            if cnt % 10 == 0:
                print cnt, len(temp_dict), db_words.count()
        for word, pubs in temp_dict.items():
            temp = db_words.find_one({'word': word})
            if temp is None:
                db_words.insert_one({'word': word, 'pubs': pubs})
            else:
                try:
                    db_words.update_one({'word': word}, {"$pushAll": {'pubs': pubs}})
                except:
                    pass
    return HttpResponse("")


def shrink():
    client = MongoClient()
    db = client['sh-engine']
    db.drop_collection('shrink')
    engine = db['sh-engine']
    db_words = db['words']
    db_shrink = db['shrink']
    seg = 10000
    total_num = engine.count()
    cnt = 0
    for i in xrange(0, db_words.count() // seg * seg + seg, seg):
        for word_data in db_words.find(skip=i, limit=seg):
            word = word_data['word']
            pubs = word_data['pubs']
            if len(pubs) >= 100000:
                pubs = []
            elif len(pubs) > 5000:
                pubs = random.sample(pubs, 5000)
            idf = math.log(1.0 * total_num / (len(pubs) + 1))
            db_shrink.insert_one({'word': word, 'pubs': pubs, 'idf': idf})
            cnt += 1
            print cnt, db_words.count(), word


if __name__ == "__main__":
    shrink()

