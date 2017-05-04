import os
import shutil

def include(destination):
    if not os.path.exists(destination + "/oracle"):
        shutil.copytree("/usr/lib/oracle", destination + "/oracle/lib/oracle")
        shutil.copytree("/usr/share/oracle", destination + "/oracle/share/oracle")
        shutil.copytree("/usr/include/oracle", destination + "/oracle/include/oracle")
        #shutil.copyfile("/usr/oracle_pack.deb", destination + "/oracle/oracle_pack.deb")


def dockerfile():
    return """
            COPY oracle /usr/
            RUN echo "/usr/lib/oracle/12.1/client64/lib" > /etc/ld.so.conf.d/oracle.conf
            ENV ORACLE_HOME /usr/lib/oracle/12.1/client64\n
            ENV LD_LIBRARY_PATH /usr/lib/oracle/12.1/client64/lib\n
            RUN ldconfig
            RUN apt-get -y update
            RUN apt-get -y install libaio-dev libaio1
            RUN pip install cx_Oracle==5.2.1
            """ 

def pip_lib():
    return ""

def commands():
    return []
 
