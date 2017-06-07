import icaro.core.utils as utils
import os

#imlemtare cartella per ogni api

class Workarea:
    def __init__(self, virtualarea):
        self.folder_tree = {"apis": {},
                            "pages":{
                                "libraries":{
                                    "css":{},
                                    "js":{}
                                }
                            },
                            "sql": {}
                            }
        self.elements = virtualarea.get_all_elements()

    def gen_widget(self, name):
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

    def gen_tree(self, tree, key, prefix = ""):
        utils.mkDir(prefix + key)
        if len(tree) > 0:
            prefix += key + "/"
            for sub in tree:
                self.gen_tree(tree[sub], sub, prefix = prefix)

    def gen_folders(self):
        self.gen_widget("mywidget1")
	self.gen_widget("mywidget2")
        for folder in self.folder_tree:
            self.gen_tree(self.folder_tree[folder], folder)

    def gen_file(self, name, type, lang):
        path = type + "/" + name + "/" + name + ".py"
        if not os.path.isfile(path):
            utils.importer(os.path.abspath(os.path.join(utils.selfLocation(), os.pardir)) + "/prefactor/"+ lang +"/"+ type + ".py", path)

    def gen_files(self):
        for element in self.elements:
            self.gen_file(element.name, element.type, element.lang.name)

