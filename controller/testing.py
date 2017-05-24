import os
import json
import subprocess
from icaro.core.virtualarea.element import Element
import icaro.core.utils as utils

class Test:
    def __init__(self, controller):
        self.controller = controller
        self.test_report = []
        utils.mkDir("logs")
        os.system("pkill uwsgi")

    def _run(self):
        port = 8000
        for element in self.controller.virtualarea.get_all_elements():
            config = {}
            config["port"] = str(port)
            config["type"] = element.type
            config["addr"] = "127.0.0.1"
            config["version"] = element.current
            config["name"] = element.name
            self.test_report.append(config)
            element.test(str(port))
            port += 1

    def _config_local_server(self,config, port):
        server = "server{\n"
        server += """
        listen """+port+""" default_server\n;
        listen [::]:"""+port+""" default_server\n;
        """
        for element in config:
            if element["type"] == "apis":
                server += "location /api/"+element["name"]+"/"+element["version"]+" {\n"
            else:
                server += "location /"+element["name"]+" {"
            server += "\nproxy_pass http://"+element["addr"]+":"+element["port"]+"/;\n"
            server += """proxy_set_header Host $http_host;proxy_set_header X-Real-IP $remote_addr;\nproxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\nproxy_set_header X-Forwarded-Proto $scheme;"""
            server += "}\n"
        server += "}"
        return server
            

    def nginx_config(self):
        settings = self.controller.settings
        port = raw_input("Insert port test: ")
        config = self._config_local_server(self.test_report, port)
        utils.fileWrite(settings["nginx_path"]+"/sites-enabled/test-"+settings["project_name"], config)

    def start(self):
        self._run()
        print self.test_report
        self.nginx_config()
        os.system("service nginx restart")
