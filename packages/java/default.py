import os
import shutil

def include(destination):
    icaro_dir = "/usr/local/lib/python2.7/dist-packages/icaro"
    if not os.path.exists(destination + "/icaro/icaro"):
        os.makedirs(destination + "/icaro/icaro/core/")
        shutil.copyfile(icaro_dir + "/render/python/render.py", destination + "/icaro/icaro/render/java/render.java")
        shutil.copytree(icaro_dir + "/utils", destination + "/icaro/icaro/utils")
        shutil.copyfile(icaro_dir + "/core/utils.py", destination + "/icaro/icaro/core/utils.py")
        shutil.copyfile(icaro_dir + "/__init__.py", destination + "/icaro/icaro/__init__.py")
        shutil.copyfile(icaro_dir + "/core/__init__.py", destination + "/icaro/icaro/core/__init__.py")

def dockerfile():
    return "COPY icaro /usr/local/lib/python2.7/site-packages\n" 

def lib():
    return """falcon==1.1.0
              uwsgi==2.0.14
              requests==2.12.4
              python-magic==0.4.12
              jinja2==2.8.1
              cassandra-driver==3.8.1
	      psycopg2==2.7.1
	      sshtunnel==0.1.2"""

def commands():
    return [
        "uwsgi --enable-threads --http-socket 0.0.0.0:10036 --wsgi-file controller.py --callable api"]
