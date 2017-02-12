import json
import utils
import os
import uuid
import shutil
import icaro.controller.packages as packages
import icaro.controller.system as system 


class Element:
    def __init__(self, node, element):
        self.node = node
        self.type = element["type"]
        self.name = element["name"]
        self.current = element["current_version"]
        self.dir = node.path + "/" + self.type + '/' + self.name + "/"
        self.container = node.container 
        self.virtualarea = self.dir + '/' + self.current + '/'
        self.workarea = self.type + "/"
        self.versions = element["versions"] 
        self.packages = node.container["packages"]

    def work_to_virtual(self):
        utils.importer(self.workarea + self.name + ".py", self.virtualarea + self.name + ".py")

    def virtual_to_work(self):
        utils.importer(self.virtualarea + self.name + ".py", self.workarea + self.name + ".py")

    def set_port_to_version(self, port):
        self.port = port
        return self.__dict__

    def set_port_to_versions(self, port):
        config = []
        for version in self.versions:
            config.append(self.set_port_to_version(port))
            port += 1

    def clean_versions(self):
        for folder in os.listdir(self.dir):
            if not folder in self.versions:
                shutil.rmtree(self.dir + folder)

    def gen_folders(self):
        print "Generating VirtualArea' s element - " + self.name
        utils.mkDir(self.virtualarea)
        self.work_to_virtual()
        packages.include(self.packages, self.node.dir)
        self.clean_versions()
        if self.type == "pages":
            utils.copytree("widgets", self.node.path + "/widgets")
            utils.copytree("pages/libraries", self.node.path + "/pages/libraries")
 

class Node:
    def __init__(self, virtualarea, container, node):
        self.id = node
        self.dir = virtualarea.path
        self.name = container["name"] + "-" + str(node)
        self.path = virtualarea.path + virtualarea.project_name + '/' + self.name + '/'
        self.container = container
        self.proxy = virtualarea.proxy
        self.packages = container["packages"]

    def get_elements_by_type(self, type):
        elements = []
        for element in self.container[type]:
            element["type"] = type
            elements.append(element)
        return elements

    def get_all_elements(self):
        elements = self.get_elements_by_type("apis")
        elements += self.get_elements_by_type("pages")
        return elements

    def assign_element_port(self, port):
        config = []
        try:
            for element in self.get_all_elements():
                config += Element(self, element).set_port_to_versions(port)
        except Exception as e:
            print "Error assigning port: " + str(e)
        return config
        
    def create_container(self):
        config = []
        dockerfile = "FROM ubuntu\nFROM python:2.7-onbuild\n"
        config = self.assign_element_port(8000)
        utils.fileWrite(self.path + "/config.icaro", json.dumps(config))
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


class Virtualarea:
    def __init__(self, settings):
        self.project_name = settings["project_name"]
        self.path = settings["virtualarea"].replace("~", utils.getHome()) + self.project_name + '/'
        self.containers = settings["containers"] 
        self.proxy = settings["proxy"]

    def create(self):
        for container in self.containers:
            for node in range(0, container["nodes"]):
                node = Node(self, container, node)
                for element in node.get_all_elements():
                    Element(node, element).gen_folders()
                node.create_container()
                node.create_requirements()
                node.controller()

    def set_monitor(self, built):
        for container in built:
            for node in built[container]:
                node_obj = Node(self, container, node)
                elements = json.loads(utils.readLines(node_obj.path + "config.icaro"))
                node["elements"] = elements
        utils.fileWrite(self.path + "/monitor.icaro", json.dumps(containers))
        return containers

    def get_monitor(self):
        return json.loads(utils.readLines(self.path + "/config.icaro"))

    def update_monitor(self, destination, container):
        pass #da sviluppare
