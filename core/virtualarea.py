import utils
from node import Node

class Virtualarea:
    def __init__(self, settings):
        self.project_name = settings["project_name"]
        self.path = settings["virtualarea"].replace("~", utils.getHome()) + self.project_name + '/'
        self.settings = settings
        self.containers = settings["containers"] 
        self.proxy = settings["proxy"]

    def get_containers(self, nodes = False):
        """Get all virtualarea' containers
            nodes = True -> [[container1-0, container1-1],[...]]
            nodes = False -> [container1-0, container2-0] 
        """
        containers = []
        for container in self.containers:
            if nodes:
                nodes_arr = []
                for node in range(0, container["nodes"]):
                    nodes_arr.append(Node(self, container, node))
                containers.append(nodes_arr)
            else:
                containers.append(Node(self, container, 0))
        return containers

    def create(self):
        from element import Element
        for container in self.containers:
            for node in range(0, container["nodes"]):
                node = Node(self, container, node)
                for element in node.get_all_elements():
                    Element(node, element).gen_folders()
                node.create_container()
                node.create_requirements()
                node.controller()
