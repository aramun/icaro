import sys
import json
import os
import icaro.core.utils as utils
from controller.main import Controller
from controller.versioning import VersionController

controller = Controller()


def buildAll():
    controller.build_all()
    print("Build Success!")
    os.system("chmod -R 777 .")
    os.system("service nginx restart")
    if os.fork() != 0:
        os.system("uwsgi --udp 0.0.0.0:1717")
    controller.run_all()


def build(containerName):
    controller.build(containerName)
    print("Build Success!")
    os.system("chmod -R 777 .")
    os.system("service nginx restart")
    os.system("uwsgi --udp 0.0.0.0:1717")
    controller.run(containerName)


def upgrade(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    controller.upgrade(type, element)


def shutAll():
    pass
    #controller.shut(settings)


def startMonitor():
    pass


def runAll(args):
    type = args.split(",")[0]
    controller.run_all()


def run(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    controller.run(type, element)


def whereismyelement(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    print(controller.whereismyelement(type, element))


def check_machines():
    print(controller.check_machines())

def versions(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    print(VersionController(controller.virtualarea, type, element).versions())


def current(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    print(VersionController(controller.virtualarea, type, element).current_version())


def checkout(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    version = args.split(",")[2]
    print(VersionController(controller.virtualarea, type, element).checkout(version))


def addversion(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    version = args.split(",")[2]
    print(VersionController(controller.virtualarea, type, element).addversion(version))


def test(args):
    type = args.split(",")[0]
    element = args.split(",")[1]
    print(controller.test(type, element))


def htop(args):
    containerName = args.split(",")[0]
    print(controller.htop(containerName))

def config_machines():
    print(controller.config_machines())

def update():
    print(controller.update())


def clean(args):
    type = args.split(",")[0]
    controller.clean(type)

def commandsManager(command):
    command.pop(0)
    if len(command) > 1:
        return getattr(sys.modules[__name__], command[0])(",".join(command[1:]))
    else:
        return getattr(sys.modules[__name__], command[0])()

