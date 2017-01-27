import json
import sys
import os
import socket

command = sys.argv[1]
element = sys.argv[2]
element = json.loads(element)

def check_output(command):
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    out, err = p.communicate()
    return {"out": out, "err": err}


cmd = "uwsgi --enable-threads --http-socket 0.0.0.0:" + str(element["port"])  + " --wsgi-file " + element["type"] + "/" + element["name"] + "/" + element["version"] + "/" + element["name"] + ".py --callable api"
print cmd
print "done!"
if os.fork() == 0:   
    os.system(cmd)
