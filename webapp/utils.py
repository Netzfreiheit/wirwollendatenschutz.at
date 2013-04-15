from flask import render_template
from flask.views import View
from webapp import (app, cache)


class TemplateView(View):
	methods = ['GET']
	
	def __init__(self, template):
		self.template = template
		
	@cache.memoize(app.config['VIEW_CACHE_TIME'])
	def dispatch_request(self):
		return render_template(self.template)
		
	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, self.template)

def add_template_rules(templatelist):
	for rule in templatelist:
		(url, template) = rule[0:2]
		name = rule[2] if len(rule)>2 else template
		view = TemplateView.as_view(name, template=template)
		app.add_url_rule(url, view_func=view)



