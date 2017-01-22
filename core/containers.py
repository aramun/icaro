import json
import os
import shutil
import subprocess
import docker
import uuid
import utils

virtualarea = "/etc/icaro/"

def tracker(container, type, port, config):
	for element in container[type]:
		obj = {'type': type, 'port': port, 'name': element["name"]} 
		config.append(obj)
		port += 1
	return config

def createContainer(container):
	port = 8000
	config = []
	dockerfile = "FROM ubuntu:latest\n\rFROM python:2.7-onbuild\n\rFROM ruby:latest\n\r"
	config = tracker(container, "apis", port, config)
	config = tracker(container, "pages", port+len(config)-1, config)
	for element in config:
		dockerfile += "EXPOSE " + str(element["port"]) + "\r\n"
	dockerfile += "EXPOSE 10036\r\n"
	dockerfile += 'CMD ["apt-get", "install", "update"]\r\n'
	dockerfile += 'CMD ["apt-get", "install", "upgrade"]\r\n'
	dockerfile += 'CMD ["apt-get", "install", "uwsgi"]\r\n'
	return dockerfile

def clearVersion(folder, versions):
	#versions is number of version from last to preserve
	if len(list(os.walk(folder))) > versions:
		shutil.rmtree(list(os.walk(folder))[0])

def createRequirements():
	return "falcon==1.1.0\r\nuWSGI==2.0.14"

def genVirtualArea(settings, type):
	for container in settings["containers"]:
		for element in container[type]:
			destination = virtualarea + settings['project_name'] + '/'+ container["name"]
			utils.mkDir(destination + "/" + type + '/' + element['name'] + '/' + element['version'])
			#clearVersion(destination, 10)
			utils.fileWrite(destination + "/requirements.txt", createRequirements())
			utils.fileWrite(destination + "/Dockerfile", createContainer(container))
			utils.importer(utils.selfLocation() + "/controller.py", destination + "/controller.py")
			utils.line_prepender(destination + "/controller.py", "p_key = '"+ str(uuid.uuid4()) +"'\r\n")
			utils.importer(type + "/" + element["name"] + ".py", destination + "/" + type + '/' + element['name'] + '/' + element['version'] + "/" + element["name"] + ".py")
			utils.importer(utils.selfLocation() + "/core.rb", destination + "/" + "core.rb")
			if type == "pages":
				utils.copytree("widgets", destination + "/widgets")
				utils.copytree("pages/libraries", destination+"/pages/libraries")

def buildContainer(client, containerName, project_name):
	return client.images.build(path = virtualarea + project_name + "/" + containerName)

def runContainer(container, project_name):
	client = docker.from_env()
	hostname = str(uuid.uuid4()) + "-host"
	containerDocker = client.containers.run(buildContainer(client, container["name"], project_name).id,
													 command = "uwsgi --enable-threads --http-socket 0.0.0.0:10036 --wsgi-file controller.py --callable api", 
													 detach = True,
													 name = project_name + "-" + container["name"],
													 hostname = hostname,
													 mem_limit = container["memory_limit"],
													 network_mode = "host"
													)
	name = containerDocker.name
	addr = hostname
	status = containerDocker.status
	return {"name": name, "addr": addr, "status": status}

def shutContainer(container, project_name):
	client = docker.from_env()
	containerDocker = client.containers.get(project_name + "-" + container["name"]).remove(v=True)
	return project_name + "-" + container["name"]

def runContainers(settings):
	containers = []
	for container in settings["containers"]:
		containers.append(runContainer(container, settings["project_name"]))
	utils.fileWrite(virtualarea + settings["project_name"] + "/monitor.icaro", json.dumps(containers))
	return containers

def shutContainers(settings):
	for container in settings["containers"]:
		containerName = shutContainer(container, settings["project_name"])
		monitors = json.loads(utils.readLines(virtualarea + settings["project_name"] + "/monitor.icaro"))
		for monitor in monitors:
			monitors.remove(monitor) if monitor["name"] == containerName else monitors
		utils.fileWrite(virtualarea + settings["project_name"] + "/monitor.icaro", json.dumps(monitors))