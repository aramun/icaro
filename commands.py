import sys
import json
import os
from core.run import init
from core.run import delete
import icaro.utils as utils

sys.path.append(utils.selfLocation())

def createProject():
	project_name = raw_input("Please insert project name: ")
	file = utils.selfLocation() + "/prefactor/settings.json"
	content = json.loads(utils.readLines(file))
	content["project_name"] = project_name
	utils.createFolder(project_name)
	utils.fileWrite(project_name + "/settings.json", json.dumps(content, indent=4, sort_keys=True))

def startProject():
	settings = json.loads(utils.readLines("settings.json"))
	init(settings)
	os.system("service nginx restart")

def restartProject():
	settings = json.loads(utils.readLines("settings.json"))
	init(settings)
	os.system("service nginx restart")

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