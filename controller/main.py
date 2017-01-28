import json
import requests
import os
import icaro.core.utils as utils
import docker

def getElement(settings, type, element):
    elements = []
    virtualarea = settings["virtualarea"].replace("~", utils.getHome())
    containers = json.loads(utils.readLines(virtualarea + settings["project_name"] + "/monitor.icaro"))
    for container in containers:
        i = 0
        for node in containers[container]:
            for nodeElement in node["elements"]:
                if type == nodeElement["type"] and element == nodeElement["name"]:
                    nodeElement["container"] = settings["project_name"] + "-" + container + "-" + str(i)
                    elements.append(nodeElement)
            i+=1
    return elements


def run(settings, type, element):
    element = getElement(settings, type, element)
    client = docker.from_env()
    for node in element:
        cmd = "uwsgi --enable-threads --http-socket 0.0.0.0:" + str(node["port"]) + " --wsgi-file " + node["type"] + "/" + node["name"] + "/" + node["version"] + "/" + node["name"] + ".py --callable api"
        container = client.containers.get(node["container"])
        print container.exec_run(cmd, stream = True, detach=True)

def runAll(settings, type):
    virtualarea = settings["virtualarea"].replace("~", utils.getHome())
    destination = virtualarea + settings["project_name"]
    containers = json.loads(utils.readLines(destination + "/monitor.icaro"))
    for container in containers:
        for element in containers[container][0]["elements"]:
            run(settings, type, element["name"])

def whereismyelement(settings, type, element):
    element = getElement(settings, type, element)
    client = docker.from_env()
    containers = []
    for node in element:
        container = client.containers.get(node["container"])
        if not container.name in containers:
            containers.append(container.name)
    return json.dumps(containers)

def htop(containerName):
    client = docker.from_env()
    container = client.containers.get(containerName)
    top = container.top()
    processes = []
    for process in top["Processes"]:
        obj = {}
        i = 0
        for title in top["Titles"]:
            obj[title] = process[i] 
            i+=1
        processes.append(obj)
    return json.dumps(processes, indent=2)

def update(settings, type, element):
    element = getElement(settings, type, element)
    client = docker.from_env()
    for node in element:
        cmd = "uwsgi --enable-threads --http-socket 0.0.0.0:" + str(node["port"]) + " --wsgi-file " + node["type"] + "/" + node["name"] + "/" + node["version"] + "/" + node["name"] + ".py --callable api"
        container = client.containers.get(node["container"])
        print container.exec_run(cmd, stream = True)
