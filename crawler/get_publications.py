import os
import re
import util
from HTMLParser import HTMLParser

JOURNAL_FOLDER = os.path.join('basic', 'journal')
CONFERENCE_FOLDER = os.path.join('basic', 'conference')
AUTHOR_FOLDER = os.path.join('basic', 'author')

JOURNAL_CRALWED_FOLDER = os.path.join('link', 'journal')
CONFERENCE_CRALWED_FOLDER = os.path.join('link', 'conference')
AUTHOR_CRALWED_FOLDER = os.path.join('link', 'author')


def get_subs(prefix, html):
    journals = util.find_journals(html)
    conferences = util.find_conferences(html)
    links = []
    for j in journals:
        if j[0].startswith(prefix):
            links.append(j[0])
    for c in conferences:
        if c[0].startswith(prefix):
            links.append(c[0])
    links = list(set(links))
    return links


def get_publications(html):
    publications = []
    pubs = re.findall('<div class="data" itemprop="headline">(.*?)</div>', html)
    for pub in pubs:
        publication = {}
        title = re.findall('<span class="title" itemprop="name">(.*?)</span>', pub)[0]
        publication['title'] = title
        publication['author'] = []
        authors = re.findall('<a href="http://dblp.uni-trier.de/pers/hd/(.*?)" itemprop="url"><span itemprop="name">(.*?)</span></a>', pub)
        for author in authors:
            publication['author'].append({'short': author[0], 'name': author[1]})
        publications.append(publication)
    return publications


def get_journals():
    files = util.listdir(JOURNAL_FOLDER)
    util.mkdir(JOURNAL_CRALWED_FOLDER)
    cnt = 0
    jour = util.load_json('jour_name.json')
    for file_name in files:
        save_path = os.path.join(JOURNAL_CRALWED_FOLDER, file_name)
        if util.exists(save_path):
            continue
        data = util.load_json(os.path.join(JOURNAL_FOLDER, file_name))
        if data['short'] not in jour.keys():
            continue
        html = util.get_page(data['url'])
        subs = get_subs(data['short'], html)
        data['name'] = jour[data['short']]
        data['sub'] = {}
        for sub in subs:
            html = util.get_page('http://dblp.uni-trier.de/db/journals/' + sub)
            data['sub'][sub] = {}
            data['sub'][sub]['pub'] = get_publications(html)
            data['sub'][sub]['name'] = jour[sub]
        cnt += 1
        print cnt, len(files), data['short']
        util.save_json(save_path, data)


def get_conferences():
    files = util.listdir(CONFERENCE_FOLDER)
    util.mkdir(CONFERENCE_CRALWED_FOLDER)
    cnt = 0
    conf = util.load_json('conf_name.json')
    for file_name in files:
        save_path = os.path.join(CONFERENCE_CRALWED_FOLDER, file_name)
        if util.exists(save_path):
            continue
        data = util.load_json(os.path.join(CONFERENCE_FOLDER, file_name))
        if data['short'] not in conf.keys():
            continue
        html = util.get_page(data['url'])
        subs = get_subs(data['short'], html)
        data['name'] = conf[data['short']]
        data['sub'] = {}
        for sub in subs:
            if sub not in conf.keys():
                continue
            html = util.get_page('http://dblp.uni-trier.de/db/conf/' + sub)
            data['sub'][sub] = {}
            data['sub'][sub]['pub'] = get_publications(html)
            data['sub'][sub]['name'] = conf[sub]
        cnt += 1
        print cnt, len(files), data['short']
        util.save_json(save_path, data)


if __name__ == '__main__':
    #get_journals()
    get_conferences()
