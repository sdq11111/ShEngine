import os
import json
import requests
import util

BASE_URL = 'http://127.0.0.1:8000/tables/'
PAGE_URL = BASE_URL + 'page/'
PUB_URL = BASE_URL + 'pub/'

JOURNAL_CRALWED_FOLDER = os.path.join('link', 'journal')
CONFERENCE_CRALWED_FOLDER = os.path.join('link', 'conference')

cnt = 0
files = util.listdir(JOURNAL_CRALWED_FOLDER)
for file_name in files:
    data = util.load_json(os.path.join(JOURNAL_CRALWED_FOLDER, file_name))
    payload = {
        'cat': 'J',
        'short': 'J_' + data['short'],
        'name': data['name'],
        'url': data['url']
    }
    requests.get(PAGE_URL, params=payload)
    for short, sub in data['sub'].items():
        payload = {
            'cat': 'JS',
            'short': 'J_' + short,
            'name': sub['name'],
            'url': 'http://dblp.uni-trier.de/db/journals/' + short
        }
        requests.get(PAGE_URL, params=payload)
        for pub in sub['pub']:
            authors = []
            for author in pub['author']:
                payload = {
                    'cat': 'A',
                    'short': 'A_' + author['short'],
                    'name': author['name'],
                    'url': 'http://dblp.uni-trier.de/pers/hd/' + author['short']
                }
                requests.get(PAGE_URL, params=payload)
                authors.append('A_' + author['short'])
            payload = {
                'short': 'J_' + short,
                'name': pub['title'],
                'authors': json.dumps(authors)
            }
            requests.get(PUB_URL, params=payload)
    exit(0)
    cnt += 1
    print cnt, len(files)
