import json
import os
import shutil
import subprocess
import docker
import uuid
import icaro.core.utils as utils

virtualarea = "/etc/icaro/"

def tracker(container, type, port, config):
	for element in container[type + "s"]:
		obj = {type: type, port: port, name: element["name"]} 
		config.append(obj)
		port++
	return config

def createContainer(container):
	port = 8000
	config = []
	dockerfile = "FROM ubuntu:latest\n\rFROM python:2.7-onbuild\n\rFROM ruby:latest\n\r"
	tracker = tracker(container, dockerfile, "api", port)
	config.append(tracker(container, "api", port, config))
	config.append(tracker(container, "page", port+len(config), config))
	for element in config:
		dockerfile += "EXPOSE " + str(element["port"]) 
		dockerfile += "CMD core.rb run " + json.dumps(element)
	return dockerfile

def clearVersion(folder, versions):
	#versions is number of version from last to preserve
	if len(list(os.walk(folder))) > versions:
		shutil.rmtree(list(os.walk(folder))[0])

def createRequirements():
	return "falcon"

def genVirtualArea(settings, type):
	type = "apis" if type == "api" else type
	for container in containers:
		for element in container[type]:
			type = "api" if type == "apis" else type
			destination = virtualarea + settings['project_name'] + '/'+ container["name"]
			utils.mkDir(destination + "/" + type + '/' + element['name'] + '/' + element['version'])
			clearVersion(destination, 10)
			utils.importer(destination + "/requirements.txt", createRequirements())
			utils.fileWrite(destination + "/Dockerfile", createContainer(container))
			utils.importer(type + "/" + element["name"] + ".py", destination + "/" + type + "/" + element["name"] + ".py")
			utils.importer(utils.selfLocation() + "/core.rb", destination + "/" + "core.rb")
			if type == "pages":
				shutil.copytree("widgets/", destination)
				shutil.copytree("pages/libraries", destination+"/pages")

def buildContainer(containerName, project_name):
	client = docker.from_env()
	return client.images.build(path = virtualarea + project_name + "/" + containerName)

def runContainer(container, project_name):
	hostname = uuid.uuid4() + "-host"
	containerDocker = client.containers.run(buildContainer(container["name"], project_name).id, 
													 detach = True,
													 name = container["name"],
													 hostname = hostname,
													 mem_limit = container["memory_limit"],
													 network_mode = "host"
													 )#cpu_limit da implemetare
	name = containerDocker.name
	addr = container["name"] + "-host"
	status = containerDocker.status
	return {"name": name, "addr": addr, "status": status}