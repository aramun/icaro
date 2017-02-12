import json
import os
import shutil
import subprocess
import docker
import uuid
import utils

class Container:
    def __init__(self, project_name, virtualarea, container, node):
        self.client = docker.from_env()
        self.node = node
        self.name = project_name + "-" + container["name"] + "-" + str(node)
        self.virtualarea = virtualarea
        self.path = virtualarea + container["name"] + "-" + str(node) + '/'
        self.mem_limit = container["memory_limit"]
        self.network_mode = "bridge"
        self.hostname = str(uuid.uuid4()) + "-host"

    def build(self):
        print "Building " + self.name + "..."
        print self.path
        print os.path.exists(self.path)
        return self.client.images.build(path = self.path)

    def run(self):
        containerDocker = self.client.containers.run(self.build().id,
                                                detach = True,
                                                name = self.name, 
                                                hostname = self.hostname, 
                                                network_mode = self.network_mode, 
                                                mem_limit = self.mem_limit)
        print "Running " + self.name + "..."
        addr = self.client.containers.get(containerDocker.id).attrs["NetworkSettings"]["IPAddress"]
        status = containerDocker.status
        utils.jsonArrayUpdate(self.virtualarea + "/" + self.name + "/config.icaro", "addr", addr)
        return {"addr": addr, "status": status}

    def shut(self):
        try:
            print "Stopping " + self.name + "..."
            self.client.containers.get(self.name).stop(timeout=1)
            print "Turning off " + self.name + "..."
            self.client.containers.get(self.name).remove(v=True)
        except(docker.errors.NotFound):
            print "Node not found"
        return self.name
