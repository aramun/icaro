import json
import icaro.core.utils as utils

class Monitor:
    def __init__(self, virtualarea):
        self.path = virtualarea.path

    def __fill_elements(self, built):
        for container in built:
            for node in built[container]:
                elements = json.loads(utils.readLines(self.path + container + "-" + str(node["node"]) + "/config.icaro"))
                node["elements"] = elements
        return built

    def create(self, built):
        built = self.__fill_elements(built)
        utils.fileWrite(self.path + "monitor.icaro", json.dumps(built))
        return built

    def update(self, built):
        built = self.__fill_elements(built)
        monitor = self.get()
        for containerName in built:
            monitor[containerName] = built[containerName]
        utils.fileWrite(self.path + "monitor.icaro", json.dumps(monitor))
        return self.get()

    def get(self):
        try:
            return json.loads(utils.readLines(self.path + "monitor.icaro"))
        except Exception as e:
            return None

    def find_element(self, containerName, elementName):
        elements = []
        monitor = self.get()
        print monitor
        for node in monitor[containerName]:
            for element in node["elements"]:
                if elementName == element["name"]:
                    elements.append(element)
        return elements
