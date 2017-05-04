import json
import uuid
import crypt
import requests
from threading import Timer

class Session:
    def __init__(self, req, resp, generate=False, in_memory=True, timeout=10):
        self.resp = resp
        self.addr = "http://172.17.0.1:5000"
        self.in_memory = in_memory
        self.data = {}
        self.timeout = timeout
        self.generate = generate
        self.__create(req, resp)

    def __create(self, req, resp):
        if "with_milk" in req.cookies:
            self.session_id = req.cookies["with_milk"]
        else:
            if self.generate:
                self.session_id = str(uuid.uuid4())
                resp.set_cookie("with_milk", self.session_id, max_age = self.timeout*60, secure=False, http_only=True, path="/")
            else:
                print "No session exist!"
                return
        if self.in_memory:
            self.__put_in_memory()
        t = Timer(self.timeout*60, self.destroy)
        t.start()

    def __put_in_memory(self):
        r = requests.get(self.addr+"/get_all/"+self.session_id)
        self.data = json.loads(r.text)
 
    def set(self, data_key, data_value):
        r = requests.get(self.addr+"/set/"+self.session_id+"&"+data_key+"="+data_value)
        if self.in_memory:
            self.__put_in_memory()
        return r.text

    def get(self, data_key):
        if self.in_memory:
            try:
                return self.data[data_key]
            except Exception as e:
                print "can't get session key, details: "+str(e)
                return None
        else:
            return requests.get(self.addr+"/get/"+self.session_id+"&"+data_key).text

    def destroy(self):
        self.resp.unset_cookie("with_milk")
        requests.get(self.addr+"/destroy/"+self.session_id)

