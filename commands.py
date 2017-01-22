import sys
import json
import os
from core.run import build
from core.run import shut
import core.utils as utils
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
	utils.fileWrite(selfLocation() + "/monitor/monitor.icaro", json.dumps(json.loads(utils.readLines(selfLocation() + "/monitor/monitor.icaro")).append("/etc/icaro/" + settings["project_name"])))

def shutProject():
	settings = json.loads(utils.readLines("settings.json"))
	shut(settings)

def rebuildProject():
	settings = json.loads(utils.readLines("settings.json"))
	shut(settings)
	build(settings)

def startMonitor():
	monitor.start()

def deleteProject():
	ans = raw_input("This action will delete all project are you sure?: (y/n)")
	if ans == "y" or ans == "yes":
		settings = json.loads(utils.readLines("settings.json"))
		delete(settings)
		return
	elif ans == "n" or ans == "no":
		return
	else:
		print "Invalid answer!"
		deleteProject()

def commandsManager(command):
	getattr(sys.modules[__name__], command)()