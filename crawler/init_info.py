import os
import re
import util

AUTHOR_URL = 'http://dblp.uni-trier.de/pers?pos='
CONFERENCE_URL = 'http://dblp.uni-trier.de/db/conf/?pos='
JOURNAL_URL = 'http://dblp.uni-trier.de/db/journals/?pos='

JOURNAL_FOLDER = os.path.join('basic', 'journal')
CONFERENCE_FOLDER = os.path.join('basic', 'conference')
AUTHOR_FOLDER = os.path.join('basic', 'author')


def get_journals():
    pos, cnt = 1, 0
    util.mkdir(JOURNAL_FOLDER)
    while True:
        html = util.get_page(JOURNAL_URL + str(pos))
        links = re.findall('<a href="http://dblp.uni-trier.de/db/journals/(.*?)">(.*?)</a>', html)
        once_cnt = 0
        for link in links:
            if link[0] == '' or '?' in link[0]:
                continue
            data = {}
            data['type'] = 'journal'
            data['short'] = link[0]
            data['name'] = link[1]
            data['url'] = 'http://dblp.uni-trier.de/db/journals/' + data['short']
            util.save_json(os.path.join(JOURNAL_FOLDER, util.hex_hash(data['short'])), data)
            cnt += 1
            once_cnt += 1
        if once_cnt == 0:
        	break
        pos += 100
        print 'Journal', cnt


def get_conference():
    pos, cnt = 1, 0
    util.mkdir(CONFERENCE_FOLDER)
    while True:
        html = util.get_page(CONFERENCE_URL + str(pos))
        links = re.findall('<a href="http://dblp.uni-trier.de/db/conf/(.*?)">(.*?)</a>', html)
        once_cnt = 0
        for link in links:
            if link[0] == '' or '?' in link[0]:
                continue
            data = {}
            data['type'] = 'conference'
            data['short'] = link[0]
            data['name'] = link[1]
            data['url'] = 'http://dblp.uni-trier.de/db/conf/' + data['short']
            util.save_json(os.path.join(CONFERENCE_FOLDER, util.hex_hash(data['short'])), data)
            cnt += 1
            once_cnt += 1
        if once_cnt == 0:
        	break
        pos += 100
        print 'Conference', cnt


def get_author():
    pos, cnt = 1, 0
    util.mkdir(AUTHOR_FOLDER)
    while True:
        html = util.get_page(AUTHOR_URL + str(pos))
        links = re.findall('<a href="http://dblp.uni-trier.de/pers/hd/a/(.*?)">(.*?)</a>', html)
        once_cnt = 0
        for link in links:
            if link[0] == '' or '?' in link[0]:
                continue
            data = {}
            data['type'] = 'author'
            data['short'] = link[0]
            data['name'] = link[1]
            data['url'] = 'http://dblp.uni-trier.de/pers/hd/a/' + data['short']
            util.save_json(os.path.join(AUTHOR_FOLDER, util.hex_hash(data['short'])), data)
            cnt += 1
            once_cnt += 1
        if once_cnt == 0:
        	break
        pos += 300
        print 'Author', cnt


if __name__ == '__main__':
    get_journals()
    get_conference()
    get_author()
