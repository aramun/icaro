import shutil
import os
import sys
import json
import icaro.core.utils as utils
import importlib

def pack_libs(libs):
    for lib in libs:
        os.system("sudo apt-get -y -f install " + lib)

def dockerfile(packages):
    result = ""
    for package in packages:
        module = importlib.import_module('icaro.packages.' + package)
        result += module.dockerfile()
    return result

def include(packages, destination):
    print destination
    for package in packages:
        module = importlib.import_module('icaro.packages.' + package)
        module.include(destination)

def pip_lib(packages):
    result = ""
    for package in packages:
        module = importlib.import_module('icaro.packages.' + package)
        result += module.pip_lib()
    return result

def commands(packages):
    result = ""
    for package in packages:
        module = importlib.import_module('icaro.packages.' + package)
        for command in module.commands():
            result += "CMD " + json.dumps(command.split(" ")) + "\r\n"
    return result
