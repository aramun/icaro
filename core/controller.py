import falcon
import json
import os
import sys
import subprocess


def check_output(command):
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    return {"out": out, "err": err}


def run(element):
    command = 'python core.py run ' + element
    out = check_output(command)["out"]
    return out


def commandsManager(command):
    command = command.split(" ")
    return getattr(sys.modules[__name__], command[0])(",".join(command[1:]))


class Root:
    def on_post(self, req, resp):
#       global p_key
#       if req.get_header("sec_key") == p_key:
        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        resp.body = commandsManager(req.stream.read())
#       else:
#           resp.status = falcon.HTTP_403
#           resp.body = "Permission Denied"

api = falcon.API()

api.add_route('/', Root())
