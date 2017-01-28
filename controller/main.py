import json
import requests
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
        print node
        cmd = "uwsgi --enable-threads --http-socket 0.0.0.0:" + str(node["port"])  + " --wsgi-file " + node["type"] + "/" + node["name"] + "/" + node["version"] + "/" + node["name"] + ".py --callable api"
        container = client.containers.get(node["container"])
        print container.exec_run(cmd, stream = True)
