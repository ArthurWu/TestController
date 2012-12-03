from urllib2 import urlopen
import os
from runner import get_config
import const
try:
	import json
except:
	import simplejson as json

DEFAULT_ROOT = get_config().get('fitnesse', 'rooturl')

def get_tests(root=DEFAULT_ROOT):
	''' 
	root is a fitnesse url, this function returns all tests under this url
	'''
	properties = get_properties(root)
	is_normal = not properties['Suite'] and not properties['Test']
	is_suite = properties['Suite'] and not properties['Test']
	is_test = not properties['Suite'] and properties['Test']

	test_url = root
	test_list = []
	if is_test:
		test_list.append(test_url)
	elif is_normal or is_suite:
		urls = get_subtest_urls(test_url)
		subtests = map(get_tests, urls)
		for tests in subtests:
			if isinstance(tests, list): 
				test_list.extend(tests)
	else:
		return

	return test_list

def check_results(test_root = DEFAULT_ROOT, team=const.WARRIOR, tests = None):
	result_dir = get_config().get('pools', 'testresult') % team
	tests = get_tests(test_root) if not tests else tests

	results = []
	for test in tests:
		result_folder = result_dir.rstrip('\\') + '\\' + test.split('/')[-1]

		for root, dirs, files in os.walk(result_folder):
			files.sort()
			#result file name formart: 20120202171855_424_0_26_0.xml
			latest_result = files and files[-1].split('.')[0].split('_')
			result, date = convert_result([int(i) for i in latest_result])
			result.setdefault('url', test)
			result.setdefault('latest_hostory', const.FIT_HISTORY % (test, date))
			results.append(result)
	
	return sort_by_status(results)

def get_properties(url):
	print const.FIT_PROPERTIES % url
	return json.loads(urlopen(const.FIT_PROPERTIES % url).read())

def get_subtest_urls(url):
	# call api result formart: ["PageFooter 0","ErrorLogs 2","FitNesse 9"]
	print const.FIT_NAME % url
	result = json.loads(urlopen(const.FIT_NAME % url).read())
	url = url.endswith('/') and url or url + '.'
	return [url + r.split(" ")[0] for r in result]

def convert_result(result):
	date, right, wrong, igone, exception = result
	
	red = green = gray = False
	if wrong > 0 or exception > 0:
		red = True
	elif right == 0 and wrong == 0 and igone == 0 and exception == 0:
		gray = True
	else:
		green = True

	return {'red': red, 'gray': gray, 'green': green}, date

def sort_by_status(results):
	reds = []
	grays = []
	greens = []
	for r in results:
		if r['red']: reds.append(r)
		if r['gray']: grays.append(r)
		if r['green']: greens.append(r)
	reds.sort()
	grays.sort()
	greens.sort()
	return reds+grays+greens

if __name__ == '__main__':
	print DEFAULT_ROOT
	print check_results()