import json
import utils

class Monitor:
    def __init__(self, virtualarea):
        self.path = virtualarea.path
        
    def create(self, built):
        for container in built:
            for node in built[container]:
                elements = json.loads(utils.readLines(self.path + container + "/config.icaro"))
                node["elements"] = elements
        utils.fileWrite(self.path + "monitor.icaro", json.dumps(containers))
        return containers

    def update(self):
        pass

    def get(self):
        return json.loads(utils.readLines(self.path + "monitor.icaro"))

