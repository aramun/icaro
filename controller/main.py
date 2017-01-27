import json
import requests
import icaro.core.utils as utils

def getElement(settings, type, element):
    elements = []
    virtualarea = settings["virtualarea"].replace("~", utils.getHome())
    containers = json.loads(utils.readLines(virtualarea + settings["project_name"] + "/monitor.icaro"))
    for container in containers:
        for node in containers[container]:
            for nodeElement in node["elements"]:
                if type == nodeElement["type"] and element == nodeElement["name"]:
                    elements.append(nodeElement)
    return elements


def run(settings, type, element):
    element = getElement(settings, type, element)
    for node in element:
        r = requests.post("http://" + node["addr"] + ":10036", data="run " + json.dumps(node).replace(" ", ""))
        print(r.text)

