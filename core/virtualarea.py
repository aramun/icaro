import utils


class Virtualarea:
    def __init__(self, settings):
        self.project_name = settings["project_name"]
        self.path = settings["virtualarea"].replace("~", utils.getHome()) + self.project_name + '/'
        self.containers = settings["containers"] 
        self.proxy = settings["proxy"]

    def create(self):
        from node import Node
        from element import Element
        for container in self.containers:
            for node in range(0, container["nodes"]):
                node = Node(self, container, node)
                for element in node.get_all_elements():
                    Element(node, element).gen_folders()
                node.create_container()
                node.create_requirements()
                node.controller() 
