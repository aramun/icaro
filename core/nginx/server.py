import icaro.core.utils as utils


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

