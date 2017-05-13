import falcon
import json
import os
import requests
import icaro.utils.security as security
import icaro.core.utils as utils

def my_action():
	return {var:"mydata"}

class Root:
	def on_get(self, req, resp):
		if security.api(req, "127.0.0.1"):
			role = "all"
			template = render.load_template(role, page, libraries)
			resp.status = falcon.HTTP_200
			resp.content_type = 'application/json'
			resp.body = json.dumps(my_action())
		else:
			falcon.HTTP_403
			resp.body = "Access Denied"

api = falcon.API()

api.add_route('/', Root())
#you can add subpages
