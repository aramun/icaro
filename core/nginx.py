import utils

def writeProxy(proxy_dir, obj, config_profiles):
    for elem in obj:
	config = ""
	for proxy_rule in config_profiles[elem["config_profile"]]:
	    for rule in config_profiles[elem["config_profile"]][proxy_rule]:
		config += proxy_rule + " " + rule + ";"
	utils.fileWrite(proxy_dir + elem["name"], config)

def writeUpstream(addrs, elementName):
    upstream = "upstream " + elementName +" { \r\n" 
    for addr in addrs:
        upstream += "server " + addr+";"
    upstream += "}"
    return upstream

def createElementsStruct(config, settings):
    struct = {"apis": {}, "pages":{}}
    for container in config:
        for node in config[container]:
            for element in node["elements"]:
                if not element["name"] in struct[element["type"]]:
                    struct[element["type"]][element["name"]] = [element["addr"] + ":" + str(element["port"])]
                else:
                    struct[element["type"]][element["name"]].append(element["addr"] + ":" + str(element["port"]))
    return struct

def createApisLocations(string, apis, settings):
	for api in apis:
		string += "\r\nlocation /api/" + api + "/ {\r\n"
                string += "\tproxy_pass http://" + api + "/;\r\n"
		string += "\tinclude " + settings["nginx_path"] + settings["project_name"] + "/proxy/" + api +";\r\n"
		string += "}"
	return string

def clusterConf(config, settings):
	clusters_dir = settings["nginx_path"] + settings["project_name"] + "/clusters/"
	utils.mkDir(clusters_dir)
        elementsStruct = createElementsStruct(config, settings)
        clusters = {"apis": [], "pages": []}
        for api in elementsStruct["apis"]:
            upstream = writeUpstream(elementsStruct["apis"][api], api)
            clusters["apis"].append(api)
	    utils.fileWrite(clusters_dir + api, upstream)
        for page in elementsStruct["pages"]:
            upstream = writeUpstream(elementsStruct["pages"][page], page)
	    utils.fileWrite(clusters_dir + page, upstream)
            clusters["pages"].append(page)
        return clusters

def createPagesLocations(string, pages, settings):
    for page in pages:
	string += "\r\nlocation /"
	if page != "index":
	    string += page
	string += " {\r\n"
        string += "\tproxy_pass http://" + page + ";\r\n"
	string += "\tinclude " + settings["nginx_path"] + settings["project_name"] + "/proxy/" + page+";\r\n"
	string += "}"
    return string

def proxyConf(settings):
    proxy_dir = settings["nginx_path"] + settings["project_name"] + "/proxy/"
    utils.mkDir(proxy_dir)
    for container in settings["containers"]:
	writeProxy(proxy_dir, container["apis"], settings["config_profiles"])
	writeProxy(proxy_dir, container["pages"], settings["config_profiles"])

def mkServer(settings, clusters):
    server_dir = settings["nginx_path"] + settings["project_name"]
    port = str(settings["listen_port"])
    utils.mkDir(server_dir)
    server = "server{\r\nlisten " + port + " default_server;\r\n listen [::]:" + port + " default_server;\r\n"
    server = createApisLocations(server, clusters["apis"], settings)
    server = createPagesLocations(server, clusters["pages"], settings)
    server += "}"
    utils.fileWrite(server_dir + "/server", server)
    utils.insertIntoFile("http", "\r\ninclude " + settings["nginx_path"] + settings["project_name"] + "/server;", settings["nginx_path"] + "nginx.conf")
