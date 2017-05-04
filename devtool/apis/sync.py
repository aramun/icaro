import falcon
import os
import json
import icaro.utils.security as security
import icaro.core.utils as utils



class Sync(resource):
    def on_get(self, req, resp, api, format = "json"):
        if security.api(request, "127.0.0.1"):
            resp.status = falcon.HTTP_200
            if os.fork() == 0:
                session.set(api.name + "_result")
            resp.content_type = 'text/plain'
            resp.body = "OK"
        else:
            falcon.HTTP_403
            resp.body = "Access Denied"        



