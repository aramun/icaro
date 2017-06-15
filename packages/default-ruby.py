import os
import shutil

def include(destination):
    icaro_dir = "/usr/local/lib/python2.7/dist-packages/icaro"
    if not os.path.exists(destination + "/icaro/icaro"):
        os.makedirs(destination + "/icaro/icaro/core/")
        shutil.copyfile(icaro_dir + "/render.py", destination + "/icaro/icaro/render.py")
        shutil.copytree(icaro_dir + "/utils", destination + "/icaro/icaro/utils")
        shutil.copyfile(icaro_dir + "/core/utils.py", destination + "/icaro/icaro/core/utils.py")
        shutil.copyfile(icaro_dir + "/__init__.py", destination + "/icaro/icaro/__init__.py")
        shutil.copyfile(icaro_dir + "/core/__init__.py", destination + "/icaro/icaro/core/__init__.py")

def dockerfile():
    return "COPY icaro /usr/local/lib/python2.7/site-packages\n" 

def lib():
    return """
            gem "nancy"
           """

def commands():
    return []
