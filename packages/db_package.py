import os
import shutil
import icaro.core.utils as utils

def include(destination):
    if not os.path.exists(destination + "/db_package"):
        shutil.copytree(utils.getHome() + "/db_packages", destination + "db_package")

def dockerfile:
    return "COPY db_package /usr/"

def pip_lib():
    return ""

def commands():
    return []
