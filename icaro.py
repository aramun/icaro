import os
import sys
import json
import settings
import socket
import re

port = 8000
apis = []
#creare sistema di include nel config nginx
def checkPort(port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex(('127.0.0.1', port))
	if result == 0:
		return True
	else:
		return False
		
def mkDir(path):
	if not os.path.exists(path):
		os.makedirs(path)

def readLines(path):
	file = open(path, "r")
	content = file.readlines()
	file.close()
	return "".join(content)

def fileWrite(file,content):
	file = open(file, "w")
	file.write(content)
	file.close()

def runApi(api, port):
	os.system("ruby run_apis.rb " + api + " " + str(port))

def runApis():
	global port
	global apis
	for api in settings.apis:
		if(api["addr"] == "local"):
			while (checkPort(port)):
				port += 1
			runApi(api["name"], port)
			api_obj = {}
			api_obj["name"] = api["name"]
			api_obj["addr"] = "http://127.0.0.1:"+str(port)
			apis.append(api_obj)
			port += 1
		else:
			api_obj["name"] = api["name"]
			api_obj["addr"] = api["addr"]

def createLocations(string):
	global apis
	for api in apis:
		string += "location /api/" + api["name"] + "/ {\r\n"
		string += "proxy_pass " + api["addr"] + "/;\r\n"
		string += "include " + settings.nginx_path + settings.project_name + "/proxy/" + api["name"] +";\r\n"
		string += "}"
	return string

def insertIntoFile(offset1, stringToInsert, file):
	content = readLines(file)
	n = content.find(offset1)
	if n != -1:
		while (content[n] != "{"):
			n += 1
		content = content[:n+1] + stringToInsert + content[n+1:]
		fileWrite(file, content)


def mkServer():
	server_dir = settings.nginx_path + settings.project_name
	mkDir(server_dir)
	file = open(server_dir+"/server" , "w")
	server = "server{\r\nlisten " + str(settings.listen_port) + " default_server;\r\n"
	server += "listen [::]:80 default_server;\r\n"
	server = createLocations(server)
	server += "}"
	file.write(server)
	file.close()
	insertIntoFile("http", "\r\ninclude "+settings.nginx_path + settings.project_name +"/server;", settings.nginx_path + "nginx.conf")


def proxyConf():
	proxy_dir = settings.nginx_path + settings.project_name + "/proxy/"
	mkDir(proxy_dir)
	for api in settings.apis:
		file = open(proxy_dir + api["name"], "w")
		config = ""
		for proxy_rule in api["config_profile"]:
			for rule in api["config_profile"][proxy_rule]:
				config += proxy_rule + " " + rule + ";"
		file.write(config)
		file.close()

runApis()
proxyConf()
mkServer()
