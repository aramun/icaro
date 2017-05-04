import os
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
        self.remote_path = self.element.workarea + self.element.name + "/" + self.version + "/"

    def run(self):
        """Run element version"""
        client = docker.from_env(version='auto')
        print "Runnning " + self.element.name + "v" + self.version + " node " + self.node.name + "..."
        cmd = "uwsgi --enable-threads --http-socket 0.0.0.0:" + str(self.get_port()) + " --wsgi-file " + self.remote_path + self.element.name + ".py --callable api --logto 172.17.0.1:1717"
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
        client = docker.from_env(version='auto')
        print "Shuting " + self.element.name + "v" + self.version + " node " + self.node.name + "..."
        container = client.containers.get(self.node_name)
        container.exec_run('pkill -9 -f "' + cmd + '"', stream = True, detach=True)

    def clean(self):
        """Remove version"""
        try:
            shutil.rmtre(self.virtual_path)
        except Exception as e:
            print "Version already deleted"

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
        shutil.rmtree(dir)
        copy_tree(self.virtual_path, dir)
        copy_tree(self.node.path + "/sql", "sql")
        if self.element.type == "pages":
            copy_tree(self.node.path + "/widgets", "widgets")
            copy_tree(self.node.path + "/pages/libraries", "pages/libraries")

    def work_to_virtual(self):
        """Upload version to virtual area"""
        dir = self.element.workarea + self.element.name + "/"
        copy_tree(dir, self.virtual_path)
        copy_tree("sql", self.node.path + "/sql")
        if self.element.type == "pages":
            copy_tree("widgets", self.node.path + "/widgets")
            copy_tree("pages/libraries", self.node.path + "/pages/libraries")

    def upgrade(self):
        """Upload version runtime on container"""
        print('Upgrading ' + self.element.name + ' on ' + self.node.name)
        container_endpoint = self.node_name + ":/usr/src/app/" + self.element.internal_path + self.version
        self.work_to_virtual()
        if self.element.type == "pages":
            os.system("sudo docker cp widgets " + self.node_name + ":/usr/src/app")
            os.system("sudo docker cp pages/libraries " + self.node_name + ":/usr/src/app/pages")
        os.system("sudo docker cp " + self.virtual_path + " " + container_endpoint)
