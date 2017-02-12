import json
import icaro.core.utils as utils
import main as controller
import os

def confirmation(message):
    ans = raw_input(message + " (Y/N)")
    if ans == "y" or ans == "yes":
        return True
    elif ans == "n" or ans == "no":
        return False
    else:
        print "You have to say yes or no"
        confirmation(message)

def getElement(settings, type, elementName):
    for container in settings["containers"]:
        for element in container[type]:
            if element["name"] == elementName:
                return element

def current_version(settings, type, element):
    node = getElement(settings, type, element)
    return node["current_version"]

def versions(settings, type, element):
    element = getElement(settings, type, element)
    return element["versions"]

def checkout(settings, type, element, version):
    versions_arr = versions(settings, type, element)
    if version in versions_arr:
        virtualarea = settings["virtualarea"].replace("~", utils.getHome()) + settings["project_name"]
        for container in settings["containers"]:
            for elem in container[type]:
                if elem["name"] == element:
                    elem["current_version"] = version
                    virtual_path = virtualarea + "/" + container["name"] + "-0/" + type + "/" + element + "/" + version + "/" + element + ".py"
                    if os.path.isfile(virtual_path):
                        utils.importer(virtual_path, type + "/" + element + ".py")
        utils.fileWrite("settings.json", json.dumps(settings, indent = 4))
        return "Checkout to version " + version
    else:
        if confirmation("Version doesn't exists do you want add it?"):
            addversion(settings, type, element, version)

def addversion(settings, type, element, version):
    versions_arr = versions(settings, type, element)
    if not version in versions_arr:
        virtualarea = settings["virtualarea"].replace("~", utils.getHome()) + settings["project_name"]
        elem = getElement(settings, type, element)
        elem["versions"].append(version)
        utils.fileWrite("settings.json", json.dumps(settings, indent = 4))
        commit(settings, type, element, version)
        if confirmation("Do you want checkout in the new version?"):
            checkout(settings, type, element, version)
    else:
        if confirmation("Version already exists, do you wanna checkout?"):
            checkout(settings, type, element, version)

def commit(settings, type, element):
    versions_arr = versions(settings, type, element)
    virtualarea = settings["virtualarea"].replace("~", utils.getHome()) + settings["project_name"]
    commit_message = raw_input("Version " + version + "'s commit message: ") #bisogna far aprire il tuo editor predefinito e creare un linuaggio di markup per i messaggi di commit
    utils.fileWrite(virtualarea + "/" + type + "/" + element + "/" + version + "/commit.icaro", commit_message)

