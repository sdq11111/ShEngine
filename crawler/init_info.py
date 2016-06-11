import os
import re
import util

AUTHOR_URL = 'http://dblp.uni-trier.de/pers?pos='
CONFERENCE_URL = 'http://dblp.uni-trier.de/db/conf/?pos='
JOURNAL_URL = 'http://dblp.uni-trier.de/db/journals/?pos='

JOURNAL_FOLDER = os.path.join('basic', 'journal')

def get_journals():
    pos = 1
    util.mkdir(JOURNAL_FOLDER)
    while True:
        html = util.get_page(JOURNAL_URL + str(pos))
        links = re.findall('<a href="http://dblp.uni-trier.de/db/journals/(.*?)">(.*?)</a>', html)
        for link in links:
            if link[0] == '':
                continue
            data = {}
            data['type'] = 'journal'
            data['short'] = link[0]
            data['name'] = link[1]
            data['url'] = 'http://dblp.uni-trier.de/db/journals/' + data['short']
            print data
            util.save_json(os.path.join(JOURNAL_FOLDER, data['short']), data)
        pos += 100
        break

if __name__ == '__main__':
    get_journals()
