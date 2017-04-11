import icaro.core.utils as utils


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

