import os
import sys
import json
import socket
import re
import nginx
import containers
import workarea
from virtualarea.main import Virtualarea
from virtualarea.container import Container
from virtualarea.monitor import Monitor
from nginx.main import Nginx


def buildAll(settings):
    #portController(settings["listen_port"])-> funziona il controllo ma se ricarico il progetto rileva ovviamente che la porta e occupata 
    virtualarea = Virtualarea(settings)
    workarea.genFolders()
    for container in settings["containers"]:
	workarea.genFiles(container, "apis")
	workarea.genFiles(container, "pages")
    virtualarea.create()
    built = containers.runContainers(settings, virtualarea.path)
    monitor = Monitor(virtualarea)
    monitor.create(built)
    Nginx(virtualarea, built).build()
    return built

def build(settings, containerName):
    containers = {}
    for container in settings["containers"]:
        if container["name"] == containerName:
            for node in range(0, container["nodes"]):
                containers.shutNode(containerName, node, settings["project_name"])
                containers.runContainer(container, settings["project_name"], node)
            return

def shut(settings):
    containers.shutNodes(settings)

def start(settings, container):
    nginx.mkServer(settings, apis, pages)
    os.system("service nginx restart")
