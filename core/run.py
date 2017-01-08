import os
import sys
import json
import socket
import re
import utils

port = 8000
	
def writeProxy(proxy_dir, obj, config_profiles):
	for elem in obj:
		config = ""
		for proxy_rule in config_profiles[elem["config_profile"]]:
			for rule in config_profiles[elem["config_profile"]][proxy_rule]:
				config += proxy_rule + " " + rule + ";"
		utils.fileWrite(proxy_dir + elem["name"], config)

def genWidget(name):
	utils.mkDir("widgets/" + name)
	utils.mkDir("widgets/" + name + "/css")
	utils.mkDir("widgets/" + name + "/js")
	utils.mkDir("widgets/" + name + "/images")
	if not os.path.isfile("widgets/" + name + "/index.html"):
		utils.fileWrite("widgets/" + name + "/index.html","<!-- Write your widget... -->")
	if not os.path.isfile("widgets/" + name + "/css/style.css"):
		utils.fileWrite("widgets/" + name + "/css/style.css","//widget css rules...")
	if not os.path.isfile("widgets/" + name + "/js/main.js"):
		utils.fileWrite("widgets/" + name + "/js/main.js","//widget javascript code...")

def genFolders():
	genWidget("mywidget1")
	genWidget("mywidget2")
	utils.mkDir("pages/libraries/css")
	utils.mkDir("pages/libraries/js")


def runApi(api, port, project_name):
	os.system("ruby " + utils.selfLocation() + "/start.rb " + api + " " + str(port) + " " + project_name + " " + "api " + "run")

def runPage(page, port, project_name):
	os.system("ruby " + utils.selfLocation() + "/start.rb " + page + " " + str(port) + " " + project_name + " " + "pages "+ "run")

def runApis(settingsApis, project_name):
	global port
	apis = []
	api_obj = {}
	utils.createFolder("api")
	for api in settingsApis:
		if(api["addr"] == "local"):
			while (utils.checkPort(port)):
				port += 1
			runApi(api["name"], port, project_name)
			api_obj = {}
			api_obj["name"] = api["name"]
			if not os.path.isfile("api/" + api["name"] + ".py"):
				utils.importer(os.path.abspath(os.path.join(utils.selfLocation(), os.pardir)) + "/prefactor/api.py", "api/" + api["name"] + ".py")
			api_obj["addr"] = "http://127.0.0.1:" + str(port)
			apis.append(api_obj)
			port += 1
		else:
			api_obj["name"] = api["name"]
			api_obj["addr"] = api["addr"]
	return apis

def runPages(settingsPages, project_name):
	global port
	pages = []
	utils.createFolder("pages")
	utils.createFolder("widgets")
	page_obj = {}
	for page in settingsPages:
		if(page["addr"] == "local"):
			while (utils.checkPort(port)):
				port += 1
			runPage(page["name"], port, project_name)
			page_obj = {}
			page_obj["name"] = page["name"]
			if not os.path.isfile("pages/" + page["name"] + ".py"):
				utils.importer(os.path.abspath(os.path.join(utils.selfLocation(), os.pardir)) + "/prefactor/page.py", "pages/" + page["name"] + ".py")
			page_obj["addr"] = "http://127.0.0.1:" + str(port)
			pages.append(page_obj)
			port += 1
		else:
			page_obj["name"] = page["name"]
			page_obj["addr"] = page["addr"]
	return pages

def portController(port):
	if utils.checkPort(int(port)):
		port = raw_input("Port " + port + " seems already in use...insert another port --> ")
		portController(port)


def createApisLocations(string, apis, settings):
	for api in apis:
		string += "\r\nlocation /api/" + api["name"] + "/ {\r\n"
		string += "\tproxy_pass " + api["addr"] + "/;\r\n"
		string += "\tinclude " + settings["nginx_path"] + settings["project_name"] + "/proxy/" + api["name"] +";\r\n"
		string += "}"
	return string

def createPagesLocations(string, pages, settings):
	for page in pages:
		string += "\r\nlocation /"
		if page["name"] != "index": 
			string += page["name"]
		string += " {\r\n"
		string += "\tproxy_pass " + page["addr"] + "/;\r\n"
		string += "\tinclude " + settings["nginx_path"] + settings["project_name"] + "/proxy/" + page["name"] +";\r\n"
		string += "}"
	return string

def insertIntoFile(offset1, stringToInsert, file):
	content = utils.readLines(file)
	if content.strip().find(stringToInsert.strip()) == -1:
		n = content.find(offset1)
		if n != -1:
			while (content[n] != "{"):
				n += 1
			content = content[:n+1] + stringToInsert + content[n+1:]
			utils.fileWrite(file, content)


def mkServer(settings, apis, pages):
	server_dir = settings["nginx_path"] + settings["project_name"]
	port = str(settings["listen_port"])
	utils.mkDir(server_dir)
	server = "server{\r\nlisten " + port + " default_server;\r\n listen [::]:" + port + " default_server;\r\n"
	server = createApisLocations(server, apis, settings)
	server = createPagesLocations(server, pages, settings)
	server += "}"
	utils.fileWrite(server_dir + "/server", server)
	insertIntoFile("http", "\r\ninclude " + settings["nginx_path"] + settings["project_name"] + "/server;", settings["nginx_path"] + "nginx.conf")


def proxyConf(settings):
	proxy_dir = settings["nginx_path"] + settings["project_name"] + "/proxy/"
	utils.mkDir(proxy_dir)
	writeProxy(proxy_dir, settings["apis"], settings["config_profiles"])
	writeProxy(proxy_dir, settings["pages"], settings["config_profiles"])

def init(settings):
	#portController(settings["listen_port"])-> funziona il controllo ma se ricarico il progetto rileva ovviamente che la porta e occupata
	proxyConf(settings)
	mkServer(settings, runApis(settings["apis"],settings["project_name"]), runPages(settings["pages"],settings["project_name"]))
	genFolders()
	os.system("service nginx restart")
	os.system("chmod -R 777 .")

def delete(settings):
	os.system("rm -r *")
	for api in settings["apis"]:
		os.system("ruby " + utils.selfLocation() + "/start.rb " + api["name"] + " " + str(settings["listen_port"]) + " " + settings["project_name"] + " api " + "terminate")
	for page in settings["pages"]:
		os.system("ruby " + utils.selfLocation() + "/start.rb " + page["name"] + " " + str(settings["listen_port"]) + " " + settings["project_name"] + " page " + "terminate")
	os.system("service nginx restart")