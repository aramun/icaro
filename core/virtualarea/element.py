import os
import shutil
import icaro.core.utils as utils
import icaro.controller.packages as packages
import docker
import subprocess
import json
from monitor import Monitor
from version import Version
from icaro.core.langs_manager.lang import Lang

class Element:
    def __init__(self, node, element):
        self.settings = node.settings
        self.type = element["type"]
        self.name = element["name"]
        self.lang = Lang(element["language"])
        self.dict = element
        self.current = element["current_version"]
        self.node = node
        self.internal_path = self.type + '/' + self.name + "/"
        self.dir = node.path + self.internal_path
        self.container = node.container
        self.workarea = self.type + "/"
        self.versions = element["versions"]
        self.packages = node.container["packages"]

    def __get_index(self):
        """get node list index into "type" settings """
        i = 0
        for element in self.settings["containers"][self.node.get_index()][self.type]:
            if element["name"] == self.name:
                return i
            i += 1

    def get_nodes(self):
        """Get all nodes object of my element's container"""
        return self.node.virtualarea.get_containers_by_element(self)

    def get_element_in_nodes(self):
        """Return elements obj array contained in all nodes"""
        elements = []
        for node in self.get_nodes():
            elements.append(Element(node, self.dict))
        return elements

    def get_version(self, version):
        """Get versions obj of this element"""
        return Version(self, version)

    def where_am_i(self):
        """Get all container names where is my element"""
        nodes_name = []
        for node in self.get_nodes():
            nodes_name.append(node.name)
        return nodes_name

    def update(self, key, value):
        """Update attribute in settings container -> element"""
        self.settings["containers"][self.node.get_index()][self.type][self.__get_index()][key] = value
        utils.fileWrite("settings.json", json.dumps(self.settings, indent = 4))

    def work_to_virtual(self):
        """Upload element's current version to virtual area"""
        for element in self.get_element_in_nodes():
            element.get_version(self.current).work_to_virtual()

    def virtual_to_work(self):
        """Download element's current version to workarea"""
        for element in self.get_element_in_nodes():
            element.get_version(self.current).virtual_to_work()

    def upgrade(self):
        """Upgrade all element's versions"""
        for element in self.get_element_in_nodes():
            element.get_version(self.current).upgrade()

    def set_port_to_versions(self, port):
        """set port to all versions"""
        config = []
        for version in self.versions:
            version = Version(self, version)
            config.append(version.set_port(port))
            port += 1
        return config

    def clean_versions(self):
        """Clean all versions, that are not present in settings, from virtualarea """
        for folder in os.listdir(self.dir):
            if not folder in self.versions:
                Version(self, folder).clean()

    def run(self, version):
        for element in self.get_element_in_nodes():
            element.get_version(version).run()

    def run_all_versions(self):
        """Run all version of this element"""
        for version in self.versions:
            self.run(version)

    def shut_all_versions(self):
        """Shut all version of this element"""
        for version in self.versions:
            self.get_version(version).shut()

    def test(self, port):
        """Run in localhost my version"""
        command = "uwsgi --enable-threads --http-socket 0.0.0.0:" + port + " --wsgi-file " + self.type + "/"+ self.name + "/" + self.name + ".py --callable api --daemonize logs/"+self.name+".log"
        return subprocess.Popen(command.split(" "), stdout=subprocess.PIPE).communicate()[0]

    def gen_folders(self):
        print "Generating VirtualArea's element - " + self.name
        utils.mkDir(self.dir)
        self.work_to_virtual()
        packages.include(self.packages, self.node.path)
        import icaro.session as session
        icaro_dir = os.path.dirname(session.__file__)
        utils.mkDir(self.node.path+"icaro/icaro/session")
        shutil.copyfile(icaro_dir+"/"+self.settings["session_engine"]+".py", self.node.path+"icaro/icaro/session/manager.py")
        utils.fileWrite(self.node.path + "/icaro/icaro/session/__init__.py", "")
        self.clean_versions()
        if self.type == "pages":
            utils.copytree("widgets", self.node.path + "/widgets")
            utils.copytree("pages/libraries", self.node.path + "/pages/libraries")

