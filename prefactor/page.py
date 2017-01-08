import falcon
import json
import os
import jinja2
import requests
import magic
import icaro.security.page as security
import icaro.render as render
import icaro.core.utils as utils

#import icaro.session as session

#role is the value that exit from your custom auth api
# a role can be static assigned
page = [
	{"roles": ["all"], "widget": "mywidget1"},
	{"roles": ["all"], "widget": "mywidget2"}
]

libraries = {
	"js": [
		"mylibrary.js"
		],
	"css": [
		"mylibrary.css"
		]
}

def getData():
	data = {}
	data["role"] = "all"#-> call at auth api
	data["username"] = "all"
	return data


class Static:
	def on_get(self, req, resp, widget, type, file):
		role = "principal"
		if security.static(req, page, role, widget):
			file = "widgets/" + widget + "/" + type + "/" +file
			resp.status = falcon.HTTP_200
			mime = magic.Magic(mime=True)
			resp.content_type = mime.from_file(file)
			resp.body = utils.readLines(file)
		else:
			falcon.HTTP_403
			resp.body = "Access Denied"

class Lib:
	def on_get(self, req, resp, type, file):
		if security.lib(req):
			file = "pages/libraries/" + type + "/" + file
			resp.status = falcon.HTTP_200
			mime = magic.Magic(mime=True)
			resp.content_type = mime.from_file(file)
			resp.body = utils.readLines(file)
		else:
			falcon.HTTP_403
			resp.body = "Access Denied"

class Root:
	def on_get(self, req, resp):
		if security.page(req):
			data = getData()
			template = render.load_template(data["role"], page, libraries)
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