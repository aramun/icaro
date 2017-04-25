import os
import icaro.core.utils as utils
from random import randint
import icaro.core.utils as utils
import requests
import base64
import json

def generate_hash():
    code = ""
    for i in range(0, 2047):
        rand = randint(32,127)
        code += chr(rand)
    return code.replace("\r", "y").replace("\n", "r").replace(" ", "a").replace("\\","//")

class Machine:
    def __init__(self, machine, machine_name, node=0):
        self.name = machine_name
        self.details = machine
        self.hash = self.__get_key()
        self.node = node

    def __get_key(self):
        try:
            return utils.bin_readLines(".connections/"+self.name)
        except Exception as e:
            print "Can't get key, machine not configured, details:"+str(e)

    def __export(self, cleanup=True):
        """Effective export to machine"""
        utils.ssh_execute(self.details, "rm -r "+self.name)
        if len(utils.ssh_send(self.details, "./"+self.name, "~/"+self.name)["message"]) == 0:
            print self.name+" exported"
        if cleanup:
            os.system("rm -rf ./"+self.name)

    def configure(self, myip):
        """configure security connector"""
        self.hash = generate_hash()
        os.system("rm .connections/"+self.name)
        utils.fileWrite(".connections/"+self.name, self.hash)
        utils.copytree(utils.selfLocation()+"/connectors/connector", "./"+self.name)
        connector = utils.readLines(self.name+"/connector.py")
        utils.fileWrite(self.name+"/connector.py", 'central_ip="'+myip+'"\np_key="""'+self.hash+'"""\n'+connector)
        self.__export()

    def check(self):
        url = "http://"+self.details["addr"]+":10036/check"
        headers = {'sec_key': self.hash}
        r = requests.get(url, headers=headers)
        return json.loads(r.text)["status"]

    def run(self, container, hostname, mem_limit):
        url = "http://"+self.details["addr"]+":10036/run/"+container
        headers = {'sec_key': self.hash, 'node': str(self.node), 'hostname': hostname, 'mem_limit': mem_limit}
        r = requests.get(url, headers=headers)
        return json.loads(r.text)

    def exec_bash(self, command):
        print self.details
        return utils.ssh_execute(self.details, command)

    def send_file(self, file, destination):
        print self.details
        return utils.ssh_send(self.details, file, destination)
        
