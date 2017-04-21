import json
import requests
import os
import shutil
import icaro.core.utils as utils
import versioning
import tarfile
import distutils.dir_util as dir_util
import testing
from icaro.core.virtualarea.workarea import Workarea
from icaro.core.virtualarea.main import Virtualarea
from icaro.core.virtualarea.container import Container
from icaro.core.virtualarea.monitor import Monitor
from icaro.core.nginx.main import Nginx


class Controller:
    def __init__(self):
        self.settings = json.loads(utils.readLines("settings.json"))
        self.virtualarea = Virtualarea(self.settings)
        self.monitor = Monitor(self.virtualarea)
        self.workarea = Workarea(self.virtualarea)

    def run_containers(self):
        containers = {}
        for container in self.virtualarea.containers:
            containers = self.run_container(container,track = containers)
        return containers

    def run_container(self, container, track = {}):
        track[container["name"]] = []
        for node in range(0, container["nodes"]):
            container_obj = Container(self.settings["project_name"], self.virtualarea, container, node)
            container_obj.shut()
            track[container["name"]].append(container_obj.run())
        return track

    def __tree_build(self):
        """
        Scope:
            Build virtualarea and workarea folder
        """
        self.workarea.gen_folders()
        self.workarea.gen_files()
        self.virtualarea.create()

    def build_all(self):
        """
        Output -> json built
        Scope:
            Build all containers creating monitor and building nginx
        """
        self.__tree_build()
        built = self.run_containers()
        self.monitor.create(built)
        Nginx(self.virtualarea, built).build()
        return built

    def build(self, container):
        """
        Input -> Node obj
        Output -> json built
        Scope:
            Build a single container creating monitor and building nginx
        """
        self.__tree_build()
        built = self.run_container()
        self.run(container)
        self.monitor.update(built)
        Nginx(self.virtualarea, self.monitor.get()).build()
        return built

    def whereismyelement(self, type, elementName):
        """Return list of node name"""
        containers = self.virtualarea.get_element(type, elementName).where_am_i()
        return json.dumps(containers)

    def run(self, type, elementName, version):
        element = self.virtualarea.get_element(type, elementName)
        if version == "current":
            element.run(element.current)
        elif version == "all":
            element.run_all_versions()
        else:
            element.run(version)

    def update(self):
        """
        Update workarea if settings it's been changed
        """
        self.workarea.gen_folders()
        self.workarea.gen_files()
        return "Update -> OK"

    def clean(self, type):
        """
        Hard => clean virtual area and all containers
        Soft => clean virtual area
        """
        if type == "hard":
            os.system("rm -rf "+self.virtualarea.path)
        elif type == "soft":
            os.system("rm -rf "+self.virtualarea.path)

    def run_all(self):
        for element in self.virtualarea.get_all_elements():
            element.run_all_versions()

    def test(self, type, elementName):
        testing.test(self, type, elementName)

    def upgrade(self, type, elementName):
        """Upgrade element current version"""
        self.virtualarea.get_element(type, elementName).upgrade()
