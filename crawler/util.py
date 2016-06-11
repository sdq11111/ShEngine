import os
import md5
import json
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


def save_json(path, value):
    path = os.path.join(CRAWLED_FOLDER, path)
    with open(path, 'w') as writer:
        writer.write(json.dumps(value))


def load_json(path):
    path = os.path.join(CRAWLED_FOLDER, path)
    with open(path, 'r') as reader:
        return json.loads(reader.read())


def exists(path):
    path = os.path.join(CRAWLED_FOLDER, path)
    return os.path.exists(path)


def mkdir(path):
    path = os.path.join(CRAWLED_FOLDER, path)
    if not os.path.exists(path):
        os.makedirs(path)


def hex_hash(name):
    m = md5.new()
    m.update(name)
    return m.hexdigest()


if __name__ == '__main__':
    print get_page('http://dblp.uni-trier.de/db/')
