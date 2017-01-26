import falcon
import json
import os
import sys

def run(element):
    os.system("ruby core.rb run " + element)

def prova(string):
    return string

def commandsManager(command):
    command = command.split(" ")
    return getattr(sys.modules[__name__], command[0])(",".join(command[1:]))

class Root:
    def on_post(self, req, resp):
        #global p_key
        #if req.get_header("sec_key") == p_key:
	resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        resp.body = commandsManager(req.stream.read())
	#else:
        #    resp.status = falcon.HTTP_403
	#    resp.body = "Permission Denied"

api = falcon.API()

api.add_route('/', Root())
