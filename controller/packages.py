import shutil
import os
import sys
import icaro.core.utils as utils


def oracle_include(destination):
    if not os.path.exists(destination + "/oracle"):
        shutil.copytree("/usr/lib/oracle", destination + "/oracle/lib/oracle")
        shutil.copytree("/usr/share/oracle", destination + "/oracle/share/oracle")
        shutil.copytree("/usr/include/oracle", destination + "/oracle/include/oracle")

def oracle_dockerfile():
    return """
            COPY oracle /usr/\n
            RUN echo "/usr/lib/oracle/12.1/client64/lib" > /etc/ld.so.conf.d/oracle.conf\n
            ENV ORACLE_HOME /usr/lib/oracle/12.1/client64\n
            ENV LD_LIBRARY_PATH /usr/lib/oracle/12.1/client64/lib\n
            RUN ldconfig\n
            RUN apt-get -y update\n
            RUN apt-get -y install libaio-dev\n
            RUN pip install cx_Oracle\n
            """ 

def icaro_include(destination):
    icaro_dir = "/usr/local/lib/python2.7/dist-packages/icaro"
    if not os.path.exists(destination + "/icaro/icaro"):
        os.makedirs(destination + "/icaro/icaro/core/")
        shutil.copyfile(icaro_dir + "/render.py", destination + "/icaro/icaro/render.py")
        shutil.copytree(icaro_dir + "/utils", destination + "/icaro/icaro/utils")
        shutil.copyfile(icaro_dir + "/core/utils.py", destination + "/icaro/icaro/core/utils.py")
        shutil.copyfile(icaro_dir + "/__init__.py", destination + "/icaro/icaro/__init__.py")
        shutil.copyfile(icaro_dir + "/core/__init__.py", destination + "/icaro/icaro/core/__init__.py")

def icaro_dockerfile():
    return "COPY icaro /usr/local/lib/python2.7/site-packages\n" 


def dockerfile(packages):
    result = ""
    for package in packages:
        result += getattr(sys.modules[__name__], package+"_dockerfile")()
    return result

def include(packages, destination):
    for package in packages:
        getattr(sys.modules[__name__], package+"_include")(destination)
