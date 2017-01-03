import jinja2
import os

def build_head(template, libraries):
	template += '<html><head>'
	for library in libraries:
		template += '<link rel="stylesheet" href="lib/css/' + library + '">'
	template += '</head><body>'
	return template

def build_footer(template, libraries):
	for library in libraries:
		template += '<script src="lib/js/' + library + '"></script>'
	template += '</body></html>'
	return template

def load_template(role, page, libraries):
	template = ""
	template += build_head(template, libraries["css"])
	for section in page:
		if role == section["role"]:
			path = os.path.join('widgets', section["widget"] + "/index.html")
			with open(os.path.abspath(path), 'r') as fp:
				template += fp.read()
	template += build_footer(template, libraries["js"])
	return jinja2.Template(template)