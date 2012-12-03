import os
try:
	import json
except:
	import simplejson as json

WORK_DIR = os.path.dirname(__file__)
CACHE_DIR = os.path.abspath(os.path.join(WORK_DIR, 'cache'))

CACHE_FILE = CACHE_DIR+'\\'+'testresult.json'

def write_cache(data):
	try:
		file = open(CACHE_FILE, 'w')
		file.write(json.dumps(data))
		file.close()
	except:
		raise Exception('Can not find the cache file: %s' % CACHE_FILE)

def read_cache():
	try:
		file = open(CACHE_FILE, 'r')
		data = file.read()
		file.close()
		return data
	except Exception, e:
		raise e

def has_cache():
	return os.path.exists(CACHE_FILE)

def cache_time():
	if not has_cache(): return
	return os.path.getmtime(CACHE_FILE)

if __name__ == '__main__':
	d = range(10)
	dstr = 'what are you doing?'
	write_cache(dstr)

	print read_cache()