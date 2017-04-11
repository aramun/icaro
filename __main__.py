import sys
import core.utils as utils
import os
import json

def selfLocation():
    return os.path.dirname(os.path.realpath(__file__))

def createProject():
    project_name = raw_input("Please insert project name: ")
    file = selfLocation() + "/prefactor/settings.json"
    content = json.loads(utils.readLines(file))
    content["project_name"] = project_name
    utils.createFolder(project_name)
    utils.fileWrite(project_name + "/settings.json", json.dumps(content, indent=4))

if(sys.argv[1] == "createProject"):
    createProject()
else:
    import commands
    commands.commandsManager(sys.argv)
