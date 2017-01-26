import os
import sys
import json
import socket
import re
import nginx
import containers
import workarea


def build(settings):
	#portController(settings["listen_port"])-> funziona il controllo ma se ricarico il progetto rileva ovviamente che la porta e occupata
	nginx.proxyConf(settings)
	workarea.genFolders()
	for container in settings["containers"]:
	    workarea.genFiles(container, "apis")
	    workarea.genFiles(container, "pages")
	containers.genVirtualArea(settings)
	containers.genVirtualArea(settings)
	built = containers.runContainers(settings)
        nginx.clusterConf(built, settings)
        #nginx.mkServer(settings)
	print "Build Succes! Details: " + json.dumps(built)
	os.system("chmod -R 777 .")

def shut(settings):
	containers.shutNodes(settings)

def start(settings, container):
	nginx.mkServer(settings, apis, pages)
	os.system("service nginx restart")
