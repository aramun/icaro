import icaro.core.utils as utils

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


