import os
import util

JOURNAL_FOLDER = os.path.join('basic', 'journal')
CONFERENCE_FOLDER = os.path.join('basic', 'conference')
AUTHOR_FOLDER = os.path.join('basic', 'author')

JOURNAL_CRALWED_FOLDER = os.path.join('link', 'journal')
CONFERENCE_CRALWED_FOLDER = os.path.join('link', 'conference')
AUTHOR_CRALWED_FOLDER = os.path.join('link', 'author')


def get_links(prefix, html):
	journals = util.find_journals(html)
	conferences = util.find_conferences(html)
	authors = util.find_authors(html)
	links = []
	for j in journals:
		if j[0].startswith(prefix):
			print '\t', j[0]
			inner_url = 'http://dblp.uni-trier.de/db/journals/' + j[0]
			inner = util.get_page(inner_url)
			links += get_links('###', inner)
		else:
			links.append(('journal', j[0].split('/')[0].split('#')[0]))
	for c in conferences:
		if c[0].startswith(prefix):
			print '\t', c[0]
			inner_url = 'http://dblp.uni-trier.de/db/conf/' + c[0]
			inner = util.get_page(inner_url)
			links += get_links('###', inner)
		else:
			links.append(('conference', c[0].split('/')[0].split('#')[0]))
	for a in authors:
		links.append(('author', a[0].split('#')[0]))
	links = list(set(links))
	return links


def get_journals():
	files = util.listdir(JOURNAL_FOLDER)
	util.mkdir(JOURNAL_CRALWED_FOLDER)
	for file_name in files:
		save_path = os.path.join(JOURNAL_CRALWED_FOLDER, file_name)
		if util.exists(save_path):
			continue
		data = util.load_json(os.path.join(JOURNAL_FOLDER, file_name))
		html = util.get_page(data['url'])
		print data['short']
		data['links'] = get_links(data['short'], html)
		util.save_json(save_path, data)


def get_conferences():
	files = util.listdir(CONFERENCE_FOLDER)
	util.mkdir(CONFERENCE_CRALWED_FOLDER)
	for file_name in files:
		save_path = os.path.join(CONFERENCE_CRALWED_FOLDER, file_name)
		if util.exists(save_path):
			continue
		data = util.load_json(os.path.join(CONFERENCE_FOLDER, file_name))
		html = util.get_page(data['url'])
		print data['short']
		data['links'] = get_links(data['short'], html)
		util.save_json(save_path, data)


def get_authors():
	files = util.listdir(AUTHOR_FOLDER)
	util.mkdir(AUTHOR_CRALWED_FOLDER)
	for file_name in files:
		save_path = os.path.join(AUTHOR_CRALWED_FOLDER, file_name)
		if util.exists(save_path):
			continue
		data = util.load_json(os.path.join(AUTHOR_FOLDER, file_name))
		html = util.get_page(data['url'])
		print data['short']
		data['links'] = get_links(data['short'], html)
		util.save_json(save_path, data)


if __name__ == '__main__':
    get_journals()
    get_conferences()
    get_authors()
