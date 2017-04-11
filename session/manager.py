import json
import uuid
import crypt
import utils
from cassandra.cluster import Cluster

"""
In cassandra the update create the record if doesn t exists
"""
class Session:
    def __init__(self, user, ip, in_memory=True, timeout=10 ):
        cluster = Cluster(["172.17.0.1"])
        self.session = cluster.connect("session")
        self.ip = ip
        self.user = user
        self.status = False
        self.in_memory = in_memory
        self.data = {}

    def __exists(self):
        return self.session.execute("SELECT * FROM users WHERE user_id=%s AND ip_addr=%s", (self.user, self.ip))

    def __put_in_memory(self):
        rows = self.session.execute("SELECT * FROM data WHERE session_id = %s", (self.session_id,))#grandissima stronzata che pero se no fatta va in errore
        print rows
        for row in rows:
            self.data[row.data_key] = row.data_value

    def start(self):
        exists = self.__exists()
        if not exists:
            self.session_id = str(uuid.uuid4())
            self.session.execute("INSERT INTO users (ip_addr, user_id, session_id) VALUES (%s, %s, %s)", (self.ip, self.user, self.session_id))
        else:
            for row in exists:
                self.session_id = row.session_id
        self.status = True
        if self.in_memory:
            self.__put_in_memory()
        #self.expire() -> da fare

    def set(self, data_key, data_value):
        if self.status:
            query = "UPDATE data SET data_value=%s WHERE data_key=%s AND session_id=%s AND data_id=now()"
            self.session.execute(query, (data_value, data_key, self.session_id))
            if self.in_memory:
                self.__put_in_memory()

    def get(self, data_key):
        if self.status:
            if self.in_memory:
                return self.data[data_key]
            else:
                return self.session.prepare("SELECT data_value INTO data WHERE data_key=%s", (data_key))

    def destroy(self):
        self.session.execute("DELETE * FROM data WHERE session_id=%s", (self.session_id))
        self.session.execute("DELETE * FROM data WHERE user_id=%s AND ip_addr=%s", (self.user, self.ip))
        self.session.shutdown()
