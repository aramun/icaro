import sys
import os
import icaro.core.utils as utils

class EnvController:
    def __init__(self, controller, action, name, secondEnv = None):
        self.name = name
        self.controller = controller
        self.secondEnv = envName
        getattr(sys.modules[__name__], "self."+action)()
        self.controller.commit_settings()

    def checkout(self):
        if self.name in self.controller.settings["envs"]:
            self.controller.settings["current_env"] = self.name
        else:
            print("Enviroment doesn't exists, you can create it with command 'icaro env create <envName>'")

    def create(self):
        if not self.name in self.controller.settings["envs"]:
            self.controller.settings["envs"].append(self.name)
        else:
            print("Enviroment already exitst!")

    def delete(self):
        if not self.name in self.controller.settings["envs"]:
            print("Enviroment doesn't exists")
            return

        if len(self.controller.settings["envs"]) <= 1:
            print("You must have at least 1 enviroment")
            return

        self.controller.settings["envs"].remove(self.name)
        if self.name == self.controller.settings["current_env"]:
            self.checkout()

    def replicate(self):
        #delete envName except for settings.json and add all sources of current env
        if(self.secondEnv):
            pass
        else:
            print("You must specify a second enviroment name")
