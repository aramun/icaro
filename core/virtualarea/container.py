import json
import os
import shutil
import subprocess
import docker
import uuid
import icaro.core.utils as utils

class Container:
    def __init__(self, project_name, virtualarea, container, node):
        self.client = docker.from_env(version='auto')
        self.node = node
        self.name = project_name + "-" + container["name"] + "-" + str(node)
        self.virtualarea = virtualarea
        self.path = self.virtualarea.path + container["name"] + "-" + str(node) + '/'
        self.mem_limit = container["memory_limit"]
        self.network_mode = "bridge"
        self.hostname = str(uuid.uuid4()) + "-host"

    def build(self):
        print "Building " + self.name + "..."
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
        utils.jsonArrayUpdate(self.path + "config.icaro", "addr", addr)
        return {"addr": addr, "status": status, "node": self.node}

    def shut(self):
        try:
            print "Stopping " + self.name + "..."
            self.client.containers.get(self.name).stop(timeout=1)
            print "Turning off " + self.name + "..."
            self.client.containers.get(self.name).remove(v=True)
        except(docker.errors.NotFound):
            print "Node not found"
        return self.name

    def htop(self):
        container = client.containers.get(self.name)
        top = container.top(ps_args="aux")
        processes = []
        for process in top["Processes"]:
            obj = {}
            i = 0
            for title in top["Titles"]:
                obj[title] = process[i] 
                i+=1
            processes.append(obj)
        return json.dumps(processes, indent=2)

