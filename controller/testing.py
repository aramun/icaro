import os
import subprocess

def test(type, api):
    port = raw_input("Insert port to run: ")
    command = "uwsgi --enable-threads --http-socket 127.0.0.1:" + port  + " --wsgi-file " + type + "/" + api + ".py --callable api"
    return subprocess.Popen(command.split(" "), stdout=subprocess.PIPE).communicate()[0]

