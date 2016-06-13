import util

jour = util.load_json('jour_name.json')
conf = util.load_json('conf_name.json')

print len(jour), len(conf), len(jour) + len(conf)

for k, v in jour.items():
	conf[k] = v

print len(conf)
