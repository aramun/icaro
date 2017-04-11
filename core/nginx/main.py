import icaro.core.utils as utils
from cluster import Cluster
from proxy import Proxy
from server import Server


class Nginx:
    def __init__(self, virtualarea, built):
        self.path = virtualarea.settings["nginx_path"]
        self.config_profiles = virtualarea.settings["config_profiles"]
        self.project_name = virtualarea.project_name
        self.containers = virtualarea.containers
        self.virtualarea = virtualarea
        self.built = built

    def __createElementsStruct(self, built):
        struct = {"apis": {}, "pages": {}}
        for container in built:
            for node in built[container]:
                for element in node["elements"]:
                    name = element["name"] + "~~" + str(element["version"]) 
                    if not name in struct[element["type"]]:
                        struct[element["type"]][name] = {"addrs":[element["addr"] + ":" + str(element["port"])],
                                                         "version": element["version"],
                                                         "name": name.split("~~")[0],
                                                         "current": element["current_version"]}
                    else:
                        struct[element["type"]][name]["addrs"].append(element["addr"] + ":" + str(element["port"]))
        return struct
        
    def proxy_conf(self):
        for container in self.virtualarea.get_containers():
	    for element in container.get_all_elements():
                Proxy(self, element, self.config_profiles[element["config_profile"]]).write()

    def cluster_conf(self):
        elementsStruct = self.__createElementsStruct(self.built)
        clusters = {"apis": [], "pages": []}
        for type in clusters:
            for element in elementsStruct[type]:
                print elementsStruct[type][element]
                Cluster(self, elementsStruct[type][element]).write()
                clusters[type].append(elementsStruct[type][element])
        return clusters

    def build(self):
        self.proxy_conf()
        Server(self, self.virtualarea.settings["listen_port"], self.cluster_conf()).create()
    
