import sys
import json
import os
from core.run import build
from core.run import shut
import core.utils as utils
import controller.main as controller
import monitor.monitor as monitor

def selfLocation():
	return os.path.dirname(os.path.realpath(__file__))

def createProject():
	project_name = raw_input("Please insert project name: ")
	file = selfLocation() + "/prefactor/settings.json"
	content = json.loads(utils.readLines(file))
	content["project_name"] = project_name
	utils.createFolder(project_name)
	utils.fileWrite(project_name + "/settings.json", json.dumps(content, indent=4, sort_keys=True))

def buildProject():
	settings = json.loads(utils.readLines("settings.json"))
	build(settings)
        if utils.readLines(selfLocation() + "/monitor/monitor.icaro") == "null":
            utils.fileWrite(selfLocation() + "/monitor/monitor.icaro","["+settings['project_name']+"]")
	#utils.fileWrite(selfLocation() + "/monitor/monitor.icaro", json.dumps(json.loads(utils.readLines(selfLocation() + "/monitor/monitor.icaro")).append("~/icaro/" + settings["project_name"])))

def shutProject():
    settings = json.loads(utils.readLines("settings.json"))
    shut(settings)

def rebuildProject():
    settings = json.loads(utils.readLines("settings.json"))
    shut(settings)
    build(settings)

def startMonitor():
    monitor.start()

def runAll(args):
    type = args.split(",")[0]
    settings = json.loads(utils.readLines("settings.json"))
    controller.runAll(settings, type)

def run(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    settings = json.loads(utils.readLines("settings.json"))
    controller.run(settings, type, element)

def whereismyelement(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    settings = json.loads(utils.readLines("settings.json"))
    print controller.whereismyelement(settings, type, element)

def htop(args):
    containerName = args.split(",")[0]
    print controller.htop(containerName)

def commandsManager(command): 
    command.pop(0)
    if len(command) > 1:
        return getattr(sys.modules[__name__], command[0])(",".join(command[1:]))
    else:
        return getattr(sys.modules[__name__], command[0])()

