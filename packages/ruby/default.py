import os
import shutil

def include(destination):
    icaro_dir = "/usr/local/lib/python2.7/dist-packages/icaro"
    if not os.path.exists(destination + "/icaro/icaro"):
        os.makedirs(destination + "/icaro/icaro/core/")
        shutil.copyfile(icaro_dir + "/render/ruby/render.rb", destination + "/icaro/icaro/render/ruby/render.rb")
        shutil.copytree(icaro_dir + "/utils", destination + "/icaro/icaro/utils")
        shutil.copyfile(icaro_dir + "/core/utils.py", destination + "/icaro/icaro/core/utils.py")
        shutil.copyfile(icaro_dir + "/__init__.py", destination + "/icaro/icaro/__init__.py")
        shutil.copyfile(icaro_dir + "/core/__init__.py", destination + "/icaro/icaro/core/__init__.py")

def dockerfile():
    return "COPY icaro /usr/local/lib/python2.7/site-packages\nRUN apt-get update\nRUN apt-get install -y ruby-rack\nRUN gem install nancy\n"

def lib():
    return "source 'https://rubygems.org'\ngem 'nancy'"

def commands():
    return []
