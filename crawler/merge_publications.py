import os
import util


JOURNAL_CRALWED_FOLDER = os.path.join('link', 'journal')
CONFERENCE_CRALWED_FOLDER = os.path.join('link', 'conference')


merged_data = {}
merged_data['jour'] = {}
merged_data['conf'] = {}

cnt = 0
files = util.listdir(JOURNAL_CRALWED_FOLDER)
for file_name in files:
	data = util.load_json(os.path.join(JOURNAL_CRALWED_FOLDER, file_name))
	short = data['short']
	del data[short]
	merged_data['jour'][short] = data
	print cnt, len(files)

cnt = 0
files = util.listdir(CONFERENCE_CRALWED_FOLDER)
for file_name in files:
	data = util.load_json(os.path.join(CONFERENCE_CRALWED_FOLDER, file_name))
	short = data['short']
	del data[short]
	merged_data['conf'][short] = data
	print cnt, len(files)


util.save_json('merged.json', merged_data)