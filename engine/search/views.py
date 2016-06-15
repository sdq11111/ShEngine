import re
import math
from pymongo import MongoClient
from django.shortcuts import render
from django.http import HttpResponse

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

def search(request):
    if 'q' not in request.GET.keys():
        return render(request, 'index.html')
    query = request.GET['q']
    page = 0
    if 'p' in request.GET.keys():
        page = int(request.GET['p']) - 1

    client = MongoClient()
    db = client['sh-engine']
    #db.drop_collection('query')
    db_pubs = db['sh-engine']
    db_words = db['words']
    db_query = db['query']

    result = db_query.find_one({'query': query})
    if result is None:
        words = split_to_words(query)
        scores = {}
        total_num = db_pubs.count()
        for word in words:
            indice = db_words.find_one({'word': word})
            if indice is not None:
                idf = math.log(1.0 * total_num / len(indice['pubs']))
                for pub in indice['pubs']:
                    if pub not in scores.keys():
                        scores[pub] = 0.0
                    scores[pub] += idf
        score_list = []
        for key, val in scores.items():
            pub = db_pubs.find_one({'_id': key})
            word_count = len(split_to_words(pub['title']))
            score_list.append((val / word_count, key))
        score_list.sort(reverse=True)
        pubs = map(lambda x: x[1], score_list)
        db_query.insert_one({'query': query, 'result': pubs})
        result = db_query.find_one({'query': query})

    result = result['result'][page*20:][:20]
    for i in xrange(len(result)):
        result[i] = db_pubs.find_one({'_id': result[i]})

    next_page = page + 2
    return render(request, 'result.html', locals())
