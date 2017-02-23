import sys 
import json 
import os
from controller.main import Controller
from controller.versioning import VersionController

controller = Controller()

def selfLocation():
    return os.path.dirname(os.path.realpath(__file__))

def createProject(): 
    project_name = raw_input("Please insert project name: ")
    file = selfLocation() + "/prefactor/settings.json" 
    content = json.loads(utils.readLines(file))
    content["project_name"] = project_name
    utils.createFolder(project_name)
    utils.fileWrite(project_name + "/settings.json", json.dumps(content, indent=4, sort_keys=True))

def buildAll(): 
    controller.build_all()
    print "Build Success!"
    os.system("chmod -R 777 .")
    os.system("service nginx restart")
    controller.run_all()

def build(containerName):
    controller.build(containerName)
    print "Build Success!"
    os.system("chmod -R 777 .")
    os.system("service nginx restart")
    controller.run(containerName)

def upgrade(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    controller.upgrade(type, element)

def shutAll(): 
    core.shut(settings)

def startMonitor(): 
    pass

def runAll(args):
    type = args.split(",")[0] 
    controller.runAll(settings, type)

def run(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    controller.run(type, element)

def whereismyelement(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    print controller.whereismyelement(type, element)

def versions(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    print VersionController(controller.virtualarea, type, element).versions()

def current(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    print VersionController(controller.virtualarea, type, element).current_version()

def checkout(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    version = args.split(",")[2]
    print VersionController(controller.virtualarea, type, element).checkout(version)

def addversion(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    version = args.split(",")[2]
    print VersionController(controller.virtualarea, type, element).addversion(version)

def test(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    print testing.test(type, element)

def htop(args):
    containerName = args.split(",")[0]
    print controller.htop(containerName)
    
def commandsManager(command): 
    command.pop(0)
    if len(command) > 1:
        return getattr(sys.modules[__name__], command[0])(",".join(command[1:]))
    else:
        return getattr(sys.modules[__name__], command[0])()

