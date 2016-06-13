import os
import re
import md5
import json

CRAWLED_FOLDER = '../crawler/data'


PAGE_TYPE_JOURNAL = 0
PAGE_TYPE_JOURNAL_SUB = 1
PAGE_TYPE_CONF = 2
PAGE_TYPE_CONF_SUB = 3
PAGE_TYPE_AUTHOR = 4


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


def listdir(path):
    path = os.path.join(CRAWLED_FOLDER, path)
    return os.listdir(path)


def hex_hash(name):
    m = md5.new()
    m.update(name)
    return m.hexdigest()
