# coding: utf-8
import os
import re
import util
from HTMLParser import HTMLParser

JOURNAL_FOLDER = os.path.join('basic', 'journal')
CONFERENCE_FOLDER = os.path.join('basic', 'conference')
AUTHOR_FOLDER = os.path.join('basic', 'author')

def get_full_name(html):
	links = re.findall('<header class="headline noline"><h1>(.*?)</', html)
	try:
		return HTMLParser().unescape(links[0]).replace('/<br />', ' ')
	except:
		return ""


def get_journals():
	files = util.listdir(JOURNAL_FOLDER)
	cnt = 0
	jour = {}
	for file_name in files:
		data = util.load_json(os.path.join(JOURNAL_FOLDER, file_name))
		html = util.get_page(data['url'])
		full_name = get_full_name(html)
		cnt += 1
		print cnt, len(files), data['short'], '|', full_name
		if '404' not in full_name:
			jour[data['short']] = full_name
	util.save_json('jour_name.json', jour)


def get_conferences():
	files = util.listdir(CONFERENCE_FOLDER)
	cnt = 0
	conf = {}
	for file_name in files:
		data = util.load_json(os.path.join(CONFERENCE_FOLDER, file_name))
		html = util.get_page(data['url'])
		full_name = get_full_name(html)
		cnt += 1
		try:
			print cnt, len(files), data['short'], '|', full_name
			if '404' not in full_name:
				conf[data['short']] = full_name
		except:
			pass
	util.save_json('conf_name.json', conf)


if __name__ == '__main__':
    get_journals()
    get_conferences()
