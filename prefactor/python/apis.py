import falcon
import json
import os
import sys
import requests
import icaro.utils.security as security
import icaro.core.utils as utils
import uuid

def get_mac():
    return {"mac_addr":':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])}

class Root:
	def on_get(self, req, resp):
		if security.api(req, None):
			role = "all"
			resp.status = falcon.HTTP_200
			resp.content_type = 'plain/text'
			resp.body = json.dumps(get_mac()) 
		else:
			falcon.HTTP_403
			resp.body = "Access Denied"

api = falcon.API()

api.add_route('/', Root())
#you can add subpages
