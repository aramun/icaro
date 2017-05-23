import os
import json
import subprocess
from icaro.core.virtualarea.element import Element
from icaro.core.nginx.main import Nginx

def Test:
    def __init__(self, controller):
        self.controller = controller
        self.test_report = []

    def _run(self):
        port = 8000
        for element in self.controller.virtualarea.get_all_elements():
            config = {}
            config["port"] = str(port)
            config["type"] = element.type
            config["id"] = 0
            config["addr"] = "127.0.0.1"
            config["version"] = "1.0"
            config["current_version"] = "1.0"
            config["name"] = element.name
            self.test_report.append(config)
            element.test(port)
            port += 1

    def start():
        self.run()
        Nginx(self.controller.virtualarea, self.test_report).build()

