from urllib import urlopen
import os
try:
	import json
except:
	import simplejson as json

TEST_ROOT = 'http://arthur10:8080/'
PARAMS_PROPERTIES = '?properties&format=json'
PARAMS_NAME = '?names&format=json&ShowChildCount'
RESULT_DIR = 'C:\\AT4Forks\\FitNesse\\FitNesseRoot\\files\\testResults\\'

def get_properties(url):
	return json.loads(urlopen(url+PARAMS_PROPERTIES).read())

def get_subtest_urls(url):
	# result formart: ["PageFooter 0","ErrorLogs 2","FitNesse 9"]
	result = json.loads(urlopen(url+PARAMS_NAME).read())
	url = url == TEST_ROOT and url or url + '.'
	return [url + r.split(" ")[0] for r in result]

def get_tests(root):
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
				test_list += tests
	else:
		return

	return test_list

def check_results(path, tests = None):
	if not tests:
		tests = get_tests(TEST_ROOT)

	results = []
	for test in tests:
		result_folder = RESULT_DIR + test.replace(TEST_ROOT, '')

		for root, dirs, files in os.walk(result_folder):
			files.sort()
			#20120202171855_424_0_26_0.xml
			latest_result = files and files[0].split('.')[0].split('_')
			result = convert_result([int(i) for i in latest_result])
			result.setdefault('url', test)
			results.append(result)
	
	return sort_by_status(results)

def convert_result(result):
	date, right, wrong, igone, exception = result
	
	red = green = gray = False
	if wrong > 0 or exception > 0:
		red = True
	elif right == 0 and wrong == 0 and igone == 0 and exception == 0:
		gray = True
	else:
		green = True

	return {'red': red, 'gray': gray, 'green': green}

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