import web, os, sys
import json
import ConfigParser
import utils

ROOT = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(ROOT, 'templates')
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_DIR)

import fit

urls = (
	'/', 'Index', 
	'/test-results', 'TestResult'
)

render = web.template.render(TEMPLATES_DIR)

class Index:
	def GET(self):
		return render.index()

	def get_test_results(self):
		pass

class TestResult:
	def GET(self):
		params = web.input(reflash='true')
		res = {'actual_on': None, 'tests': []}
		
		if params.reflash == 'true':
			results = fit.check_results(team=params.team)
			utils.write_cache(results)
			res['tests'] = results
		elif params.reflash == 'false' and utils.has_cache():
			res['tests'] = json.loads(utils.read_cache())

		actual_on = utils.cache_time()
		res['actual_on'] = actual_on
		return json.dumps(res)

application = web.application(urls, globals()).wsgifunc()

if __name__ == '__main__':
	app = web.application(urls, globals())
	app.run()