import utils
import os

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
	utils.mkDir("apis")

def genFiles(container, type):
	for element in container[type]:
		if(element["addr"] == "local"):
			if not os.path.isfile(type + "/" + element["name"] + ".py"):
				utils.importer(os.path.abspath(os.path.join(utils.selfLocation(), os.pardir)) + "/prefactor/"+ type +".py", type + "/" + element["name"] + ".py")

def portController(port):
	if utils.checkPort(int(port)):
		port = raw_input("Port " + port + " seems already in use...insert another port --> ")
		portController(port)
