import falcon
import json
import os
import jinja2
import requests
import magic
import icaro.utils.security as security
import icaro.core.utils as utils

#import icaro.session as session

#role is the value that exit from your custom auth api
# a role can be static assigned
virtualarea = utils.getHome() + '/icaro/'
page = [
	{"roles": ["all"], "widget": "projects"},
	{"roles": ["all"], "widget": "containers"}
]

libraries = {
	"js": [
		"bootstrap.min.js"
		],
	"css": [
		"bootstrap.min.css"
		]
}
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
				path = os.path.join(parentDir(selfLocation()) + '/widgets', section["widget"] + "/index.html")
				with open(os.path.abspath(path), 'r') as fp:
					body += fp.read()
	template += body
	template = build_footer(template, libraries["js"], page)
	return jinja2.Template(template)

def selfLocation():
	return os.path.dirname(os.path.realpath(__file__))

def parentDir(mypath):
    return os.path.abspath(os.path.join(mypath, os.pardir))

def getProjects():
	return json.loads(utils.readLines(parentDir(selfLocation()) + "/monitor.icaro"))

def getElements(project, type):
	element = json.loads(utils.readLines(virtualarea + project + "/monitor.icaro"))
	if element["type"] == type:
		return element


def getData():
	data = {}
	data["role"] = "all"
	data["projects"] = getProjects()
	return data

class Static:
	def on_get(self, req, resp, widget, type, file):
		role = "all"
		if security.static(req, page, role, widget, "127.0.0.1"):
			file = "widgets/" + widget + "/" + type + "/" +file
			resp.status = falcon.HTTP_200
			mime = magic.Magic(mime = True)
			resp.content_type = mime.from_file(file)
			resp.body = utils.readLines(file)
		else:
			falcon.HTTP_403
			resp.body = "Access Denied"

class Lib:
	def on_get(self, req, resp, type, file):
		if security.lib(req, "127.0.0.1"):
			file = "pages/libraries/" + type + "/" + file
			resp.status = falcon.HTTP_200
			mime = magic.Magic(mime = True)
			resp.content_type = mime.from_file(file)
			resp.body = utils.readLines(file)
		else:
			falcon.HTTP_403
			resp.body = "Access Denied"

class Root:
    def on_get(self, req, resp):
        if security.page(req, "127.0.0.1"):
            data = getData()
            template = load_template(data["role"], page, libraries)
            resp.status = falcon.HTTP_200
            resp.content_type = 'text/html'
            resp.body = template.render(data = data)
        else:
            falcon.HTTP_403
            resp.body = "Access Denied"

api = falcon.API()
api.add_route('/static/{widget}/{type}/{file}', Static())
api.add_route('/lib/{type}/{file}', Lib())

api.add_route('/', Root())
    #you can add subpages
