import cmd
import sys
import json
import os
from core.run import build
from core.run import shut
import core.utils as utils
import controller.main as controller
import controller.versioning as versioning
import monitor.monitor as monito

class IcaroShell(cmd.Cmd):
    intro = "Welcome to Icaro Framework"
    prompt = "Icaro: "

    def do_createProject(self, command):
        project_name = raw_input("Please insert project name: ")
        file = selfLocation() + "/prefactor/settings.json"
        content = json.loads(utils.readLines(file))
        #utils.importer(selfLocation() + "/manager.py", "manager.py")#--> da implementare
        content["project_name"] = project_name
        utils.createFolder(project_name)
        utils.fileWrite(project_name + "/settings.json", json.dumps(content, indent=4, sort_keys=True))

    def do_buildProject(self, command):
        settings = json.loads(utils.readLines("settings.json"))
        build(settings)
        os.system("sudo service nginx restart")

    def do_shutProject(self, command):
        settings = json.loads(utils.readLines("settings.json"))
        shut(settings)

    def do_rebuildProject(self, command):
        settings = json.loads(utils.readLines("settings.json"))
        shut(settings)
        build(settings)

    def do_startMonitor(self, command):
        monitor.start()

    def do_runAll(self, type):
        settings = json.loads(utils.readLines("settings.json"))
        controller.runAll(settings, type)

    def do_run(self, type, element):
        settings = json.loads(utils.readLines("settings.json"))
        controller.run(settings, type, element)

    def do_whereismyelement(self, type, element):
        settings = json.loads(utils.readLines("settings.json"))
        print controller.whereismyelement(settings, type, element)

    def do_versions(self, type, element):
        settings = json.loads(utils.readLines("settings.json"))
        for version in versioning.versions(settings, type, element):
            print version + "\n\t"

    def do_checkout(self, type, element, version):
        settings = json.loads(utils.readLines("settings.json"))
        print versioning.checkout(settings, type, element, version)

    def do_addversion(self, type, element, version):
        settings = json.loads(utils.readLines("settings.json"))
        print versioning.addversion(settings, type, element, version)

    def do_htop(self, containerName):
        print controller.htop(containerName)

def selfLocation():
    return os.path.dirname(os.path.realpath(__file__))
