import crypt
import falcon
import uuid
import icaro.core.utils as utils
import os
import json

class Cache:
    def __init__(self, id, path="/tmp/caching/", partition_size="5000 B"):
        self.path = path+id
        self.data = []
        self.__create()
        self.partition_size = int(partition_size.split(" ")[0])

    def __create(self):
        utils.mkDir(self.path)
        if os.listdir(self.path):
            self.data = os.listdir(self.path)

    def __search(self, key):
        for partition in self.data:
            path = self.path+"/"+partition
            data = json.loads(utils.readLines(path))
            if key in data:
                return data[key]
        return "Key "+key+" not found"

    def get(self, key):
        return self.__search(key)

    def set(self, key, value):
        for partition in self.data:
            path = self.path+"/"+partition
            if os.path.getsize(path) < self.partition_size:
                data = json.loads(utils.readLines(path))
                data[key] = value
                utils.fileWrite(path, json.dumps(data))
                return "OK"
        path = self.path+"/"+str(uuid.uuid4())
        data = {}
        data[key] = value
        utils.fileWrite(path, json.dumps(data))
        self.data = os.listdir(self.path)
        return "OK"

    def get_all(self):
        dict = {}
        for i in range(0,len(self.data)):
            first = utils.merge_two_dicts(dict, json.loads(utils.readLines(self.path+"/"+self.data[i])))
            if i+1 in self.data:
                second = json.loads(utils.readLines(self.path+"/"+self.data[i+1]))
            else:
                second = {}
            dict = utils.merge_two_dicts(first, second)
            i+=1
        return dict

    def destroy(self):
        utils.rmdir(self.path)
        return "OK"

class Set:
    def on_get(self, req, resp, id, key, value):
        resp.body = Cache(id).set(key, value)

class Get:
    def on_get(self, req, resp, id, key):
        resp.body = Cache(id).get(key)

class Destroy:
    def on_get(self, req, resp, id):
        Cache(id).destroy()
        resp.body = "OK"

class GetAll:
    def on_get(self, req, resp, id):
        resp.body = json.dumps(Cache(id).get_all())

api = falcon.API()

api.add_route("/set/{id}&{key}={value}", Set())
api.add_route("/get/{id}&{key}", Get())
api.add_route("/destroy/{id}", Destroy())
api.add_route("/get_all/{id}", GetAll())
