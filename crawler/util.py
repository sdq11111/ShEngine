import os
import time
import requests

CRAWLED_FOLDER = 'data'

if not os.path.exists(CRAWLED_FOLDER):
    os.makedirs(CRAWLED_FOLDER)


def get_page(url):
    retry_int = 0.1
    while True:
        try:
            time.sleep(retry_int)
            r = requests.get(url)
            return r.text.replace('\n', '').replace('\r', '')
        except:
            retry_int += 0.1

if __name__ == '__main__':
    print get_page('http://dblp.uni-trier.de/db/')
