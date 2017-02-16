import utils

class Proxy:
    def __init__(self, nginx, element, proxy_config):
        self.path = nginx.path + nginx.project_name + "/proxy/"
        self.element = element
        self.name = element["name"]
        self.config = proxy_config

    def write(self):
	config = ""
	for proxy_rule in self.config:
	    for rule in self.config[proxy_rule]:
	        config += proxy_rule + " " + rule + ";"
	    utils.fileWrite(self.path + self.name, config)


class Server:
    def __init__(self, nginx, port, clusters):
        self.path = nginx.path + nginx.project_name
        self.port = str(port)
        self.clusters = clusters
        self.nginx = nginx

    def __location_configuration(self, element):
        string = "\tproxy_pass http://" + self.nginx.project_name + "-" + element["name"] + "~~" + element["version"] + "/;\r\n"
	string += "\tinclude " + self.path + "/proxy/" + element["name"] +";\r\n"
        return string

    def __create_apis_locations(self, apis):
        string = ""
        for api in apis:
	    string += "\r\nlocation /api/" + api["name"] + "/" + api["version"] + " {\r\n"
            string += self.__location_configuration(api)
	    string += "}"
        return string

    def __create_pages_locations(self, pages):
        string = ""
        for page in pages:
	    string += "\r\nlocation /"
	    if page["name"] != "index" and page["version"] != "current":
	        string += page["name"] + "/" + page["version"]
            else:
                string += page["version"]
	    string += " {\r\n"
            string += self.__location_configuration(page)
	    string += "}"
        return string

    def create(self):
        utils.mkDir(self.path)
        server = "server{\r\nlisten " + self.port + " default_server;\r\n listen [::]:" + self.port + " default_server;\r\n"
        server += self.__create_apis_locations(self.clusters["apis"])
        server += self.__create_pages_locations(self.clusters["pages"])
        server += "}"
        utils.fileWrite(self.path + "/server", server)
        for type in ["apis", "pages"]:
            for element in self.clusters[type]:
                utils.insertIntoFile("http", "\r\ninclude " + self.path + "/clusters/" + self.nginx.project_name + "-" + element["name"] + "~~" + element["version"] + ";", self.nginx.path + "nginx.conf")
        utils.insertIntoFile("http", "\r\ninclude " + self.path + "/server;", self.nginx.path + "nginx.conf")


class Cluster:
    def __init__(self, nginx, element):
        self.path = nginx.path + nginx.project_name + "/clusters/"
        self.name = element["name"] + "~~" + str(element["version"])
        self.addrs = element["addrs"]
        self.element = element 
        self.nginx = nginx

    def write(self):
        upstream = "upstream " + self.nginx.project_name + "-" + self.name + " { \r\n" 
        for addr in self.addrs:
            upstream += "server " + addr + ";"
        upstream += "}"
        utils.fileWrite(self.path + self.nginx.project_name + "-" + self.name, upstream)

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
                                                         "name": name.split("~~")[0]}
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
    
