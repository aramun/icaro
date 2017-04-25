import falcon
import json
import os
import sys
import subprocess
import docker

def sec_check(req):
    global central_ip
    global p_key
    return req.get_header("sec_key")==p_key and req.remote_addr == central_ip

def binary_stream(file_path):
    file = open(file_path, "rb")
    try:
        return file.read()
    except Exception as e:
        print e
    finally:
        file.close

def build(client, container):
    print "Building " + container + "..."
    #os.system("docker rmi $(docker images | grep "+self.project_name+")")
    return client.images.build(path = container)

def clean_image(client, container):
        print "Cleaning Image:" + container
        try:
            client.images.remove(self.name.lower()+":on-build", force=True)
        except(docker.errors.ImageNotFound):
            print "Image does not exits"

def run_container(client, container, node, hostname, mem_limit):
    image = build(client, container)
    image.tag(container.lower(), "on-build")
    print "Running "+container+"..."
    containerDocker = client.containers.run(image.id,
                                            detach = True,
                                            name = container, 
                                            hostname = hostname, 
                                            network_mode = "bridge",
                                            mem_limit = mem_limit)
    addr = client.containers.get(containerDocker.id).attrs["NetworkSettings"]["IPAddress"]
    status = containerDocker.status
    return {"addr": addr, "status": status, "node": node}

class Check:
    def on_get(self, req, resp):
        if sec_check(req):
            resp.status = falcon.HTTP_200
            resp.content_type = 'application/json'
            resp.body = json.dumps({"status":True})
        else:
            resp.status = falcon.HTTP_403

class Run:
    def on_get(self, req, resp, container):
        if sec_check(req):
            client = docker.from_env(version='auto')
            resp.content_type = 'application/json'
            try:
                resp.status = falcon.HTTP_200
                resp.body = json.dumps({"status": True, "message": run_container(client, container, req.get_header('node'), req.get_header('hostname'), req.get_header('mem_limit'))})
            except Exception as e:
                resp.status = falcon.HTTP_500
                resp.body = json.dumps({"status": False, "message":"Invalid container, details: "+str(e)})
        else:
            resp.status = falcon.HTTP_403

class Root:
    def on_get(self, req, resp):
        if sec_check(req):
            resp.status = falcon.HTTP_200
            resp.content_type = 'application/json'
            resp.body = sys.platform()
        else:
            resp.status = falcon.HTTP_403

api = falcon.API()

api.add_route('/', Root())
api.add_route('/check', Check())
api.add_route('/run/{container}', Run())
