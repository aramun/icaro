import json
import os
import shutil
import subprocess
import docker
import uuid
import utils

virtualarea = utils.getHome() + "/icaro/"

def tracker(container, type, port, config):
	for element in container[type]:
		obj = {'type': type, 'port': port, 'name': element["name"]} 
		config.append(obj)
		port += 1
	return config

def createContainer(container, path):
	port = 8000
	config = []
	dockerfile = "FROM ubuntu\nFROM python:2.7-onbuild\n"#FROM glatard/matlab-compiler-runtime-docker\n
	config = tracker(container, "apis", port, config)
	config = tracker(container, "pages", port+len(config)-1, config)
	utils.fileWrite(path + "/config.icaro", json.dumps(config))
	for element in config:
		dockerfile += "EXPOSE " + str(element["port"]) + "\n"
	dockerfile += "EXPOSE 10036\n"
	dockerfile += 'CMD ["apt-get", "install", "update"]\n'
	dockerfile += 'CMD ["apt-get", "install", "upgrade"]\n'
	dockerfile += 'CMD ["uwsgi", "--enable-threads", "--http-socket", "0.0.0.0:10036", "--wsgi-file", "controller.py", "--callable", "api"]'
	return dockerfile

def clearVersion(folder, versions):
	#versions is number of version from last to preserve
	if len(list(os.walk(folder))) > versions:
		shutil.rmtree(list(os.walk(folder))[0])

def createRequirements():
	return "falcon==1.1.0\r\nuwsgi==2.0.14"

def controller(destination):
	key = str(uuid.uuid4())
	utils.importer(utils.selfLocation() + "/controller.py", destination + "/controller.py")
	utils.line_prepender(destination + "/controller.py", "p_key = '" + key +"'\r\n")
	utils.fileWrite(destination + "/controller.icaro", json.dumps({'key': key, 'addr':''}))

def genVirtualArea(settings, type):
	for container in settings["containers"]:
		for element in container[type]:
			destination = virtualarea + settings['project_name'] + '/' + container["name"]
			utils.mkDir(destination + "/" + type + '/' + element['name'] + '/' + element['version'])
			#clearVersion(destination, 10)
			utils.fileWrite(destination + "/requirements.txt", createRequirements())
			utils.fileWrite(destination + "/Dockerfile", createContainer(container, destination))
			controller(destination)
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
													 detach = True,
													 name = project_name + "-" + container["name"],
													 hostname = hostname,
													 network_mode="bridge",
													 mem_limit = container["memory_limit"]
													)
	name = containerDocker.name
	addr = client.containers.get(containerDocker.id).attrs["NetworkSettings"]["IPAddress"]
	status = containerDocker.status
	content = json.loads(utils.readLines(virtualarea + project_name + "/" + container["name"] + "/controller.icaro"))
	content["addr"] = addr
	utils.fileWrite(virtualarea + project_name + "/" + container["name"] + "/controller.icaro", json.dumps(content))
	return {"name": name, "addr": addr, "status": status}

def shutContainer(container, project_name):
	client = docker.from_env()
	client.containers.get(project_name + "-" + container["name"]).stop(timeout=1)
	client.containers.get(project_name + "-" + container["name"]).remove(v=True)
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
		if os.path.isfile(virtualarea + settings["project_name"] + "/monitor.icaro"):
			monitors = json.loads(utils.readLines(virtualarea + settings["project_name"] + "/monitor.icaro"))
		for monitor in monitors:
			monitors.remove(monitor) if monitor["name"] == containerName else monitors
		utils.fileWrite(virtualarea + settings["project_name"] + "/monitor.icaro", json.dumps(monitors))