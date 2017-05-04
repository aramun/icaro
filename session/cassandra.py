import json
import uuid
import crypt
from cassandra.cluster import Cluster
from threading import Timer

class Session:
    def __init__(self, req, resp, generate=False, in_memory=True, timeout=10):
        cluster = Cluster(["172.17.0.1"])
        self.resp = resp
        self.session = cluster.connect("session")
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
        rows = self.session.execute("SELECT * FROM data WHERE session_id = %s", (self.session_id,))
        for row in rows:
            self.data[row.data_key] = row.data_value
    
    def set(self, data_key, data_value):
        query = "UPDATE data SET data_value=%s WHERE data_key=%s AND session_id=%s"
        self.session.execute(query, (data_value, data_key, self.session_id))
        if self.in_memory:
            self.__put_in_memory()

    def get(self, data_key):
        if self.in_memory:
            try:
                return self.data[data_key]
            except Exception as e:
                print "can't get session key, details: "+str(e)
                return None
        else:
            try:
                return self.session.execute("SELECT data_value FROM data WHERE session_id=%s AND data_key=%s", (self.session, data_key))
            except Exception as e:
                print "can't get session key, details: "+str(e)
                return None

    def destroy(self):
        self.resp.unset_cookie("with_milk")
        self.session.execute("DELETE FROM data WHERE session_id=%s", (self.session_id,))
        self.session.shutdown()
