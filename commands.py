import sys 
import json 
import os 
from core.run import build 
from core.run import shut
import monitor.monitor as monitor
import core.utils as utils 
import controller.main as controller
import controller.versioning as versioning
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
    build(settings)# --> quando abbiamo le opzioni di logging logghiamo qua
    print "Build Success!"
    os.system("chmod -R 777 .")
    os.system("service nginx restart")
    runAll("apis")
    runAll("pages")

def update(args): 
    type = args.split(",")[0]
    element = args.split(",")[1]
    settings = json.loads(utils.readLines("settings.json"))
    controller.update(settings, type, element)

def shutProject(): 
    settings = json.loads(utils.readLines("settings.json"))
    shut(settings)

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

def versions(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    settings = json.loads(utils.readLines("settings.json"))
    for version in versioning.versions(settings, type, element):
        print version + "\n\t"

def current(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    settings = json.loads(utils.readLines("settings.json"))
    print versioning.current_version(settings, type, element)

def checkout(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    version = args.split(",")[2]
    settings = json.loads(utils.readLines("settings.json"))
    print versioning.checkout(settings, type, element, version)

def addversion(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    version = args.split(",")[2]
    settings = json.loads(utils.readLines("settings.json"))
    print versioning.addversion(settings, type, element, version)

def htop(args):
    containerName = args.split(",")[0]
    print controller.htop(containerName)
    
def commandsManager(command): 
    command.pop(0)
    if len(command) > 1:
        return getattr(sys.modules[__name__], command[0])(",".join(command[1:]))
    else:
        return getattr(sys.modules[__name__], command[0])()

