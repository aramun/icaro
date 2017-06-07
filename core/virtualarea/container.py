import json
import os
import shutil
import subprocess
import docker
import uuid
import icaro.core.utils as utils
import sys

class Container:
    def __init__(self, project_name, virtualarea, container, node, machine):
        self.client = docker.from_env(version='auto')
        self.node = node
        self.project_name = project_name
        self.name = project_name + "-" + container["name"] + "-" + str(node)
        self.virtualarea = virtualarea
        self.path = self.virtualarea.path + container["name"] + "-" + str(node) + '/'
        self.mem_limit = container["memory_limit"]
        self.network_mode = "bridge"
        self.hostname = str(uuid.uuid4()) + "-host"
        self.machine = machine

    def build(self):
        print "Building " + self.name + "..."
        #os.system("docker rmi $(docker images | grep "+self.project_name+")")
        return self.client.images.build(path = self.path)

    def clean_image(self):
        print "Cleaning Image:" + self.name
        try:
            self.client.images.remove(self.name.lower()+":on-build", force=True)
        except(docker.errors.ImageNotFound):
            print "Image does not exits"

    def run(self):
        if self.machine == "local":
            return self.__local_run()
        else:
            return self.__remote_run()

    def __local_run(self):
        #self.clean_image()
        self.image = self.build()
        self.image.tag(self.name.lower(), "on-build")
        containerDocker = self.client.containers.run(self.image.id,
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

    def __remote_run(self):
        response = self.machine.send_file(self.path, "~/"+self.machine.name)["message"]
        if len(response) == 0:
            track = self.machine.run(os.path.basename(os.path.normpath(self.path)), self.hostname, self.mem_limit)
            if track["status"]:
                utils.jsonArrayUpdate(self.path + "config.icaro", "addr", track["message"]["addr"])
                return track["message"]
            else:
                print track["message"]
                sys.exit()
        else:
            print response
            sys.exit()

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
        container = self.client.containers.get(self.name)
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

