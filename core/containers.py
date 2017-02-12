import json
import os
import shutil
import subprocess
import uuid
import utils
from container import Container
    
def runContainers(settings, virtualarea):
    containers = {}
    for container in settings["containers"]:
        containers[container["name"]] = []
        for node in range(0, container["nodes"]):
            container_obj = Container(settings["project_name"], virtualarea, container, node)
            container_obj.shut()
            containers[container["name"]].append(container_obj.run()) 
    return containers

def shutNodes(settings, virtualarea):
    monitors = []
    config = json.loads(utils.readLines(virtualarea + settings["project_name"] + "/monitor.icaro"))
    for container in config:
        for node in range(0, len(config[container])):
            shutNode(container, node, settings["project_name"])
        if os.path.isfile(virtualarea + settings["project_name"] + "/monitor.icaro"):
            monitors = json.loads(utils.readLines(virtualarea + settings["project_name"] + "/monitor.icaro"))
