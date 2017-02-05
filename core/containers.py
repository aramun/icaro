import json
import os
import shutil
import subprocess
import docker
import uuid
import utils
import icaro.controller.packages as packages

virtualarea = utils.getHome() + "/icaro/"

def tracker(container, type, port, config):
    for element in container[type]:
        for version in element["versions"]:
            obj = {'type': type,
                   'port': port,
                   'name': element["name"],
                   'version': version,
                   'current_version': element["current_version"]}
            config.append(obj)
            port += 1
    return config

def createContainer(container, path, port):
    config = []
    dockerfile = "FROM ubuntu\nFROM python:2.7-onbuild\n"#FROM glatard/matlab-compiler-runtime-docker\n
    config = tracker(container, "apis", port, config)
    config = tracker(container, "pages", port+len(config), config)
    utils.fileWrite(path + "/config.icaro", json.dumps(config))
    dockerfile += packages.dockerfile(container["packages"])
    for element in config:
        dockerfile += "EXPOSE " + str(element["port"]) + "\n"
    dockerfile += "EXPOSE 10036\n"
    dockerfile += 'CMD ["uwsgi", "--enable-threads", "--http-socket", "0.0.0.0:10036", "--wsgi-file", "controller.py", "--callable", "api"]'
    return dockerfile

def cleanVersions(element, type, destination):
    destination = destination + "/" + type + '/' + element['name'] + '/'
    for folder in os.listdir(destination):
        if not folder in element["versions"]:
            shutil.rmtree(destination)

def createRequirements():
    return """falcon==1.1.0\r\n
            uwsgi==2.0.14\r\n
            requests==2.12.4\r\n
            python-magic==0.4.12\r\n
            jinja2==2.8.1\r\n"""

def controller(destination):
    key = str(uuid.uuid4())
    utils.importer(utils.selfLocation() + "/controller.py", destination + "/controller.py")
    utils.line_prepender(destination + "/controller.py", "p_key = '" + key +"'\r\n")
    utils.fileWrite(destination + "/controller.icaro", json.dumps({'key': key, 'addr':''}))

def genFolders(container, type, destination):
    print "Generating VirtualArea - " + container["name"] + "'s " + type
    for element in container[type]: 
        utils.mkDir(destination + "/" + type + '/' + element['name'] + '/' + element["current_version"])
        utils.importer(type + "/" + element["name"] + ".py", destination + "/" + type + '/' + element['name'] + '/' + element["current_version"] + "/" + element["name"] + ".py")
        packages.include(container["packages"], destination)
        cleanVersions(element, type, destination)
    if type == "pages":
        utils.copytree("widgets", destination + "/widgets")
        utils.copytree("pages/libraries", destination + "/pages/libraries")

def createMonitor(destination, containers):
    for container in containers:
        i=0
        for node in containers[container]:
            elements = json.loads(utils.readLines(destination + "/" + container + "-" + str(i) + "/config.icaro"))
            node["elements"] = elements
            i+=1
    utils.fileWrite(destination + "/monitor.icaro", json.dumps(containers))
    return containers

def genVirtualArea(settings):
    for container in settings["containers"]:
        for node in range(0, container["nodes"]):
            destination = virtualarea + settings['project_name'] + '/' + container["name"] + "-" + str(node)
            genFolders(container, "apis", destination)
            genFolders(container, "pages", destination)
            utils.fileWrite(destination + "/requirements.txt", createRequirements())
            utils.fileWrite(destination + "/Dockerfile", createContainer(container, destination, 8000))
            controller(destination)

def buildContainer(client, node, containerName, project_name):
    print "Building " + containerName + "..."
    return client.images.build(path = virtualarea + project_name + "/" + containerName + "-" + str(node))

def runContainer(container, project_name, node):
    client = docker.from_env()
    hostname = str(uuid.uuid4()) + "-host"
    containerDocker = client.containers.run(buildContainer(client, node, container["name"], project_name).id,
                                                           detach = True,
                                                           name = project_name + "-" + container["name"] + "-" + str(node), hostname = hostname, network_mode="bridge", mem_limit = container["memory_limit"])
    print "Running " + container["name"] + " - node" + str(node)  + "..."
    name = containerDocker.name
    addr = client.containers.get(containerDocker.id).attrs["NetworkSettings"]["IPAddress"]
    status = containerDocker.status
    utils.jsonArrayUpdate(virtualarea + project_name + "/" + container["name"] + "-"+ str(node) +"/config.icaro", "addr", addr)
    return {"addr": addr, "status": status}

def shutNode(container, node, project_name):
    client = docker.from_env()
    try:
        print "Stopping " + container + " node " + str(node) + "..."
        client.containers.get(project_name + "-" + container + "-" + str(node)).stop(timeout=1)
        print "Turning off " + container + " node " + str(node) + "..."
        client.containers.get(project_name + "-" + container + "-" + str(node)).remove(v=True)
    except(docker.errors.NotFound):
        print "Node not found"
    return project_name + "-" + container + "-" + str(node)

def runContainers(settings):
    containers = {}
    for container in settings["containers"]:
        containers[container["name"]] = []
        for node in range(0, container["nodes"]):
            shutNode(container["name"], node, settings["project_name"])
            containers[container["name"]].append(runContainer(container, settings["project_name"], node))
    createMonitor(virtualarea + settings["project_name"], containers)
    return containers

def shutNodes(settings):
    monitors = []
    config = json.loads(utils.readLines(virtualarea + settings["project_name"] + "/monitor.icaro"))
    for container in config:
        for node in range(0, len(config[container])):
            shutNode(container, node, settings["project_name"])
        if os.path.isfile(virtualarea + settings["project_name"] + "/monitor.icaro"):
            monitors = json.loads(utils.readLines(virtualarea + settings["project_name"] + "/monitor.icaro"))
            #for monitor in monitors:
            #    monitors.remove(monitor) if monitor["name"] == containerName else monitors
            #    utils.fileWrite(virtualarea + settings["project_name"] + "/monitor.icaro", json.dumps(monitors))"""
