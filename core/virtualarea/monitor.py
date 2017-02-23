import json
import icaro.core.utils as utils

class Monitor:
    def __init__(self, virtualarea):
        self.path = virtualarea.path
        
    def create(self, built):
        for container in built:
            for node in built[container]:
                elements = json.loads(utils.readLines(self.path + container + "-" + str(node["node"]) + "/config.icaro"))
                node["elements"] = elements
        utils.fileWrite(self.path + "monitor.icaro", json.dumps(built))
        return built

    def update(self):
        pass

    def get(self):
        return json.loads(utils.readLines(self.path + "monitor.icaro"))

    def find_element(self, containerName, elementName):
        elements = []
        for node in self.get()[containerName]:
            for element in node["elements"]:
                if elementName == element["name"]:
                    elements.append(element)
        return elements
