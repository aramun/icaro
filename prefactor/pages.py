import falcon
import json
import os
import requests
from icaro.render import Static
from icaro.render import Lib
from icaro.render import Page
import icaro.core.utils as utils

#import icaro.session as session

#role is the value that exit from your custom auth api
# a role can be static assigned
page = [
	{"roles": ["all"], "widget": "menu"},
        {"roles": ["admin", "superadmin"], "widget":"grid"},
        {"roles": ["admin", "superadmin"], "widget":"footer"}
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


data = getData()

api = falcon.API()
api.add_route('/static/{widget}/{type}/{file}', Static(None, data["role"], page))
api.add_route('/lib/{type}/{file}', Lib(None))

api.add_route('/', Page(None, data["role"], page, libraries, data))
#you can add subpages

