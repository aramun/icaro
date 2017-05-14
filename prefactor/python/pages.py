import falcon
import json
import os
import requests
from icaro.render import Lib
import icaro.render as render
from icaro.session.manager import Session
import icaro.utils.security as security
import icaro.core.utils as utils
import magic
#import icaro.session as session

#role is the value that exit from your custom auth api
# a role can be static assigned

head = """
   <title>Title page</title> 
   ....
"""

page = [
    {"roles": ["all"], "widget":"mywidget1"},
    {"roles": ["all"], "widget":"mywidget2"},
]

libraries = {
	"js": [
                "jquery.min.js",
                "bootstrap.min.js"
    ],
	"css": [
                "font-awesome.min.css",
                "bootstrap.min.css"
    ]
}

def getData():
    data = {}
    data["role"] = "all"#-> call at auth api
    data["username"] = "all"
    return data

class Static:
    def on_get(self, req, resp, widget, type, file):
        data = get_data(Session(req, resp))
        if security.static(req, page, data["role"], widget, None):
            file = "widgets/" + widget + "/" + type + "/" +file
            resp.status = falcon.HTTP_200
            mime = magic.Magic(mime=True)
            resp.content_type = mime.from_file(file)
            resp.body = utils.readLines(file)
        else:
            falcon.HTTP_403
            resp.body = "Access Denied"

class Page:
    def on_get(self, req, resp):
        if security.page(req, None):
            data = get_data(Session(req, resp))
            template = render.load_template(data["role"], page, libraries, head = head)
            resp.status = falcon.HTTP_200
            resp.content_type = 'text/html'
            resp.body = template.render(data = data)
        else:
            falcon.HTTP_403
            resp.body = "Access Denied"


api = falcon.API()
api.add_route('/static/{widget}/{type}/{file}', Static())
api.add_route('/lib/{type}/{file}', Lib(None))

api.add_route('/', Page())
#you can add subpages

