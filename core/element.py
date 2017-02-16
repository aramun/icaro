import os
import shutil
import utils
import icaro.controller.packages as packages

class Element:
    def __init__(self, node, element):
        self.type = element["type"]
        self.name = element["name"]
        self.current = element["current_version"]
        self.node = node
        self.dir = node.path + self.type + '/' + self.name + "/"
        self.virtualarea = self.dir + self.current + '/'
        self.container = node.container
        self.workarea = self.type + "/"
        self.versions = element["versions"]
        self.packages = node.container["packages"]

    def work_to_virtual(self):
        utils.importer(self.workarea + self.name + ".py", self.virtualarea + self.name + ".py")

    def virtual_to_work(self):
        utils.importer(self.virtualarea + self.name + ".py", self.workarea + self.name + ".py")

    def set_port_to_version(self, port, version):
        return {
                'id': self.node.id, 
                'type': self.type,
                'port': port,
                'name': self.name,
                'version': version,
                'current_version': self.current
              }

    def set_port_to_versions(self, port):
        config = []
        for version in self.versions:
            config.append(self.set_port_to_version(port, version))
            port += 1
        return config

    def clean_versions(self):
        for folder in os.listdir(self.dir):
            if not folder in self.versions:
                shutil.rmtree(self.dir + folder)

    def gen_folders(self):
        print "Generating VirtualArea's element - " + self.name 
        utils.mkDir(self.dir)
        self.work_to_virtual()
        packages.include(self.packages, self.node.path)
        self.clean_versions()
        if self.type == "pages":
            utils.copytree("widgets", self.node.path + "/widgets")
            utils.copytree("pages/libraries", self.node.path + "/pages/libraries")

