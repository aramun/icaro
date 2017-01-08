import falcon
import json
import os
import jinja2
import requests
import magic
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

class Static:
	def on_get(self, req, resp, widget, type, file):
		role = "all"
		for section in page:
			for section_role in section["roles"]:
				print section["widget"] +" "+section_role
				if section["widget"] == widget and section_role == role: 
					file = "widgets/" + widget + "/" + type + "/" +file
					resp.status = falcon.HTTP_200
					mime = magic.Magic(mime=True)
					resp.content_type = mime.from_file(file)
					resp.body = utils.readLines(file)
					return
		falcon.HTTP_403
		resp.body = "Access Denied"


class Lib:
	def on_get(self, req, resp, type, file):
		file = "pages/libraries/" + type + "/" + file
		resp.status = falcon.HTTP_200
		mime = magic.Magic(mime=True)
		resp.content_type = mime.from_file(file)
		resp.body = utils.readLines(file)

class Root:
	def on_get(self, req, resp):
		role = "all"
		template = render.load_template(role, page, libraries)
		resp.status = falcon.HTTP_200
		resp.content_type = 'text/html'
		resp.body = template.render(projects = projects)

class Monitor:
	def on_get(self, req, resp):
		role = "all"
		template = render.load_template(role, page, libraries)
		resp.status = falcon.HTTP_200
		resp.content_type = 'text/html'
		resp.body = template.render(processes = processes)

api = falcon.API()
api.add_route('/static/{widget}/{type}/{file}', Static())
api.add_route('/lib/{type}/{file}', Lib())

api.add_route('/', Root())
api.add_route('/project/{project}', Monitor())
#you can add subpages