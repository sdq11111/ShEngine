import os
import re
import md5
import json
import time
import requests

CRAWLED_FOLDER = '../crawler/data'

if not os.path.exists(CRAWLED_FOLDER):
    os.makedirs(CRAWLED_FOLDER)


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
