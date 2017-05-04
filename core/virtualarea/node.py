import json
import icaro.core.utils as utils
import shutil
import uuid
import icaro.controller.packages as packages
import icaro.controller.system as system
from element import Element

class Node:
    def __init__(self, virtualarea, container, node):
        self.id = node
        self.virtualarea = virtualarea
        self.counter = container["nodes"]
        self.dir = virtualarea.path
        self.settings = virtualarea.settings
        self.name = container["name"] + "-" + str(node)
        self.path = virtualarea.path + self.name + '/'
        self.container = container
        self.proxy = virtualarea.proxy
        self.packages = container["packages"]

    def get_index(self):
        """get node list index into "containers" settings """
        i = 0
        for container in self.settings["containers"]:
            if container["name"] == self.container["name"]:
                return i
            i += 1

    def update(self, key, value):
        self.settings["containers"][self.get_index()][key] = value
        utils.fileWrite("settings.json", json.dumps(self.settings.__dict__, indent = 4))

    def get_elements_by_type(self, type):
        elements = []
        for element in self.container[type]:
            element["type"] = type
            elements.append(element)
        return elements

    def get_nodes(self):
        nodes = []
        for node in range(0, self.counter):
            nodes.append(Node(self.virtualarea, self.container, node))
        return nodes

    def run_all_elements(self):
        for element in self.get_all_elements():
            Element(element, self).run_all_versions()

    def get_all_elements(self):
        elements = []
        elements = self.get_elements_by_type("apis")
        elements += self.get_elements_by_type("pages")
        return elements

    def get_all_obj_elements(self):
        elements = []
        for element in self.get_all_elements():
            elements.append(Element(self, element))
        return elements

    def assign_element_port(self, port):
        config = []
        try:
            for element in self.get_all_elements():
                element = Element(self, element).set_port_to_versions(port)
                config += element
                port += len(element)
        except Exception as e:
            print "Error assigning port: " + str(e)
        return config
        
    def create_container(self):
        config = []
        dockerfile = "FROM ubuntu\nFROM python:2.7-onbuild\n"
        config = self.assign_element_port(8000)
        utils.fileWrite(self.path + "config.icaro", json.dumps(config))
        dockerfile += system.set_proxy(self.proxy, self.path)
        dockerfile += "COPY apt.conf /etc/apt/apt.conf\n"
        dockerfile += packages.dockerfile(self.packages)
        for element in config:
            dockerfile += "EXPOSE " + str(element["port"]) + "\n"
        dockerfile += "EXPOSE 10036\n"
        dockerfile += packages.commands(self.packages)
        utils.fileWrite(self.path + "/Dockerfile", dockerfile)

    def create_requirements(self):
        utils.fileWrite(self.path + "requirements.txt", packages.pip_lib(self.packages))

    def controller(self):
        key = str(uuid.uuid4())
        utils.importer(utils.selfLocation() + "/controller.py", self.path + "/controller.py")
        utils.line_prepender(self.path + "/controller.py", "p_key = '" + key +"'\r\n")
        utils.fileWrite(self.path + "/controller.icaro", json.dumps({'key': key, 'addr':''}))

