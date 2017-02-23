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


class VersionController:
    def __init__(self, virtualarea, type, element):
        if virtualarea.get_element(type, element) != None:
            self.element = virtualarea.get_element(type, element)
        else:
            print "Element doesn' t exists!" 

    def versions(self):
        return self.element.versions

    def current_version(self):
        return self.element.current

    def checkout(self, version):
        if version in self.versions():
            self.element.update("current_version", version)
            self.element.virtual_to_work()
            print "Checkout to version " + version 
        else:
            if confirmation("Version doesn't exists do you want add it?"):
                self.addversion(version)

    def addversion(self, version):
        if not version in self.versions():
            self.element.update("versions", self.versions().append(version))
            if confirmation("Do you want checkout in the new version?"):
                self.checkout(version)
        else:
            if confirmation("Version already exists, do you wanna checkout?"):
                self.checkout(version)
