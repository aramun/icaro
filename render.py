import jinja2
import icaro.security.page as security
import os

def build_head(template, libraries, page):
	template += '<html><head>'
	for library in libraries:
		template += '<link rel="stylesheet" href="lib/css/' + library + '">'
	for section in page:
		template += '<link rel="stylesheet" href="static/' + section["widget"] + '/css/style.css">'
	template += '</head><body>'
	return template

def build_footer(template, libraries, page):
	for library in libraries:
		template += '<script src="lib/js/' + library + '"></script>'
	for section in page:
		template += '<script src="static/' + section["widget"] + '/js/main.js"></script>'
	template += '</body></html>'
	return template

def load_template(role, page, libraries):
	template = ""
	body = ""
	template = build_head(template, libraries["css"], page)
	for section in page:
		for section_role in section["roles"]:
			if role == section_role:
				path = os.path.join('widgets', section["widget"] + "/index.html")
				with open(os.path.abspath(path), 'r') as fp:
					body += fp.read()
	template += body
	template = build_footer(template, libraries["js"], page)
	return jinja2.Template(template)