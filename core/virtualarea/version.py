import docker
import shutil
from monitor import Monitor
from distutils.dir_util import copy_tree

class Version:
    def __init__(self, element, version):
        self.element = element
        self.node = self.element.node
        self.node_name = self.node.virtualarea.project_name + "-" + self.node.name
        self.version = version
        self.virtual_path = self.element.dir + self.version + '/'

    def run(self):
        """Run element version"""
        client = docker.from_env()
        print "Runnning " + self.element.name + "v" + self.version + " node " + self.node.name + "..."
        cmd = "uwsgi --enable-threads --http-socket 0.0.0.0:" + str(self.get_port()) + " --wsgi-file " + self.virtual_path + self.element.name + ".py --callable api"
        container = client.containers.get(self.node_name)
        self.shut(cmd)
        container.exec_run(cmd, stream = True, detach=True)

    def set_port(self, port):
        """
        Input -> port (int)
        Output -> element (dict)
                             |
                    {id, type, port, name, version}
        Scope:
            Set port to version
        """
        return {
                'id': self.node.id, 
                'type': self.element.type,
                'port': port,
                'name': self.element.name,
                'version': self.version,
                'current_version': self.element.current
              }
    
    def shut(self, cmd):
        """Shut version"""
        client = docker.from_env()
        print "Shuting " + self.element.name + "v" + self.version + " node " + self.node.name + "..."
        container = client.containers.get(self.node_name)
        container.exec_run('pkill -9 -f "' + cmd + '"', stream = True, detach=True)

    def clean(self):
        """Remove version"""
        shutil.rmtre(self.virtual_path)

    def get_port(self):
        """Get version port from monitor"""
        monitor = Monitor(self.element.node.virtualarea)
        for node in monitor.find_element(self.element.container["name"], self.element.name):
            if node["version"] == self.version:
                return node["port"]
        print "Monitor not created yet"

    def virtual_to_work(self):
        """Download version to workarea"""
        dir = self.element.workarea + self.element.name + "/"
        copy_tree(self.virtual_path, dir)
        if self.type == "pages":
            copy_tree(self.node.path + "/widgets", "widgets")
            copy_tree(self.node.path + "/pages/libraries", "pages/libraries")

    def work_to_virtual(self):
        """Upload version to virtual area"""
        dir = self.element.workarea + self.element.name + "/"
        copy_tree(dir, self.virtual_path)
        if self.element.type == "pages":
            copy_tree("widgets", self.node.path + "/widgets")
            copy_tree("pages/libraries", self.node.path + "/pages/libraries")

    def upgrade(self):
        """Upload version runtime on container"""
        container_endpoint = self.node.name + ":/usr/src/app/" + self.element.internal_path + self.version
        self.work_to_virtual()
        if self.element.type == "pages":
            os.system("sudo docker cp widgets " + node.name + ":/usr/src/app")
            os.system("sudo docker cp pages/libraries " + node.name + ":/usr/src/app/pages")
        os.system("sudo docker cp " + self.virtualarea + " " + container_endpoint)
 
