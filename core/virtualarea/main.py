import icaro.core.utils as utils
from node import Node
from element import Element

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

    def get_element(self, type, elementName):
        for container in self.get_containers():
            for element in container.get_elements_by_type(type):
                if elementName == element["name"]:
                    return Element(container, element)
        return None
    
    def get_containers_by_element(self, element):
        """Input -> element obj
            ....
        """
        nodes = []
        for container in self.get_containers():
            for element_dict in container.get_elements_by_type(element.type):
                if element.name == element_dict["name"]:
                    nodes += Node(self, container.container, 0).get_nodes()
        return nodes

    def get_container_by_name(self, containerName, nodes = False):
        nodes_struct = None
        for container in self.containers:
            if container["name"] == containerName:
                if nodes:
                    for node in range(0, container["nodes"]):
                        nodes_struct = []
                        nodes_struct.append(Node(self, container, node))
                else:
                    nodes_struct = Node(self, container, 0)
        return nodes_struct

    def get_all_elements(self):
        """Returns all element's object in the project """
        elements = []
        for container in self.get_containers():
            elements += container.get_all_obj_elements()
        return elements

    def create(self):
        for container in self.containers:
            for node in range(0, container["nodes"]):
                node = Node(self, container, node)
                for element in node.get_all_elements():
                    Element(node, element).gen_folders()
                node.create_container()
                node.create_requirements()
                node.controller()
