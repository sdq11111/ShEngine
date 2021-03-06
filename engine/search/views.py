import re
import math
import time
import random
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
    start = time.time()
    if 'q' not in request.GET.keys():
        return render(request, 'index.html')
    query = request.GET['q']
    query = ' '.join(split_to_words(query))
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
                print word, len(indice['pubs'])
                if len(indice['pubs']) > 100000:
                    continue
                idf = math.log(1.0 * total_num / len(indice['pubs']))
                for pub in indice['pubs']:
                    if pub not in scores:
                        scores[pub] = 0.0
                    scores[pub] += idf

        score_list = []
        for key, val in scores.items():
            score_list.append((val, key))
        score_list.sort(reverse=True)
        #if len(score_list) > 5000:
        #    score_list = score_list[:5000]
        #for i in xrange(len(score_list)):
        #    pub = db_pubs.find_one({'_id': score_list[i][1]})
        #    word_count = len(split_to_words(pub['title']))
        #    score_list[i] = (score_list[i][0] / word_count, score_list[i][1])
        #score_list.sort(reverse=True)
        pubs = map(lambda x: x[1], score_list)
        db_query.insert_one({'query': query, 'result': pubs})
        result = db_query.find_one({'query': query})

    result = result['result'][page*20:][:20]
    for i in xrange(len(result)):
        result[i] = db_pubs.find_one({'_id': result[i]})

    next_page = page + 2
    elapsed = time.time() - start
    print elapsed, 's'
    return render(request, 'result.html', locals())
