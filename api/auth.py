import falcon
import json
 
class Try:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body="HELLO"
                                      
api = falcon.API()
api.add_route('/try', Try())

