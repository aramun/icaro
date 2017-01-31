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
                if not element["name"] + "v" + element["version"] in struct[element["type"]]:
                    struct[element["type"]][element["name"] + "v" + element["version"]] = [element["addr"] + ":" + str(element["port"])]
                else:
                    struct[element["type"]][element["name"] + "v" + element["version"]].append(element["addr"] + ":" + str(element["port"]))
    return struct

def createApisLocations(string, apis, settings):
    for api in apis:
        apiName = api.split("v")[0]
        version = api.split("v")[1]
	string += "\r\nlocation /api/" + apiName + "/" + version + " {\r\n"
        string += "\tproxy_pass http://" + settings["project_name"] + "-" + api+ "/;\r\n"
	string += "\tinclude " + settings["nginx_path"] + settings["project_name"] + "/proxy/" + apiName +";\r\n"
	string += "}"
    return string

def clusterConf(config, settings):
	clusters_dir = settings["nginx_path"] + settings["project_name"] + "/clusters/"
	utils.mkDir(clusters_dir)
        elementsStruct = createElementsStruct(config, settings)
        clusters = {"apis": [], "pages": []}
        for api in elementsStruct["apis"]:
            upstream = writeUpstream(elementsStruct["apis"][api], settings["project_name"] + "-" + api)
            clusters["apis"].append(api)
	    utils.fileWrite(clusters_dir + settings["project_name"] + "-" + api, upstream)
        for page in elementsStruct["pages"]:
            upstream = writeUpstream(elementsStruct["pages"][page], settings["project_name"] + "-" + page)
	    utils.fileWrite(clusters_dir + settings["project_name"] + "-" + page, upstream)
            clusters["pages"].append(page)
        return clusters

def createPagesLocations(string, pages, settings):
    for page in pages:
        pageName = page.split("v")[0]
        version = page.split("v")[1]
	string += "\r\nlocation /"
	if pageName != "index" and version != "current":
	    string += pageName + "/" + version
        else:
            string += version
	string += " {\r\n"
        string += "\tproxy_pass http://" + settings["project_name"] + "-" + page + "/;\r\n"
	string += "\tinclude " + settings["nginx_path"] + settings["project_name"] + "/proxy/" + pageName+";\r\n"
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
    project_name = settings["project_name"]
    utils.fileWrite(server_dir + "/server", server)
    for api in clusters["apis"]:
        utils.insertIntoFile("http", "\r\ninclude " + settings["nginx_path"] + project_name + "/clusters/" + project_name + "-" + api  + ";", settings["nginx_path"] + "nginx.conf")
    for page in clusters["pages"]:
        utils.insertIntoFile("http", "\r\ninclude " + settings["nginx_path"] + project_name + "/clusters/" + project_name + "-" + page + ";", settings["nginx_path"] + "nginx.conf")
    utils.insertIntoFile("http", "\r\ninclude " + settings["nginx_path"] + project_name + "/server;", settings["nginx_path"] + "nginx.conf")
    
