import utils

def writeProxy(proxy_dir, obj, config_profiles):
	for elem in obj:
		config = ""
		for proxy_rule in config_profiles[elem["config_profile"]]:
			for rule in config_profiles[elem["config_profile"]][proxy_rule]:
				config += proxy_rule + " " + rule + ";"
		utils.fileWrite(proxy_dir + elem["name"], config)

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

def proxyConf(settings):
	proxy_dir = settings["nginx_path"] + settings["project_name"] + "/proxy/"
	utils.mkDir(proxy_dir)
	for container in settings["containers"]:
		writeProxy(proxy_dir, container["apis"], settings["config_profiles"])
		writeProxy(proxy_dir, container["pages"], settings["config_profiles"])

def mkServer(settings, containers):
	server_dir = settings["nginx_path"] + settings["project_name"]
	port = str(settings["listen_port"])
	utils.mkDir(server_dir)
	server = "server{\r\nlisten " + port + " default_server;\r\n listen [::]:" + port + " default_server;\r\n"
	server = createApisLocations(server, apis, settings)
	server = createPagesLocations(server, pages, settings)
	server += "}"
	utils.fileWrite(server_dir + "/server", server)
	utils.insertIntoFile("http", "\r\ninclude " + settings["nginx_path"] + settings["project_name"] + "/server;", settings["nginx_path"] + "nginx.conf")