import psycopg2 as postgre
from sshtunnel import open_tunnel
import icaro.core.utils as utils
import logging

class PostgreConnector():
    
    def __init__(self, database_config, ssh_tunnel_config):
        """
            database_config {
                db_name: database name
                db_user: database user to logon
                db_password: database password
                db_host: database host ip
                db_port: database port
            }

            ssh_tunnel_config {
                ssh_ip_address: ip address server to connect
                ssh_port: port server to connect
                ssh_username: username
                ssh_password: password
                ssh_remote_bind_address: remote address to bind
                ssh_remote_bind_port: remote port to bind
            }
        """
        self.__map_database_config(database_config)
        self.__map_ssh_config(ssh_tunnel_config)
        self.tunnel_mode = False

    def __map_database_config(self, database_config):
        self.db_name = database_config["db_name"]
        self.db_user = database_config["db_user"]
        self.db_password = database_config["db_password"]
        self.db_host = database_config["db_host"]
        self.db_port = database_config["db_port"]

    def __map_ssh_config(self, ssh_tunnel_config):
        self.ssh_ip_address = ssh_tunnel_config["ssh_ip_address"]
        self.ssh_port = ssh_tunnel_config["ssh_port"]
        self.ssh_username = ssh_tunnel_config["ssh_username"]
        self.ssh_password = ssh_tunnel_config["ssh_password"]
        self.ssh_remote_bind_address = ssh_tunnel_config["ssh_remote_bind_address"]
        self.ssh_remote_bind_port = ssh_tunnel_config["ssh_remote_bind_port"]
    
    def open_tunnel(self):
        self.tunnel = open_tunnel((self.ssh_ip_address, self.ssh_port), ssh_username=self.ssh_username, 
                ssh_password=self.ssh_password, remote_bind_address=(self.ssh_remote_bind_address, self.ssh_remote_bind_port))
        self.tunnel.start()
        self.tunnel_mode = True
        logging.info("tunnel ssh succesfully created and started")

    def close_tunnel(self):
        self.tunnel.close()
        logging.info("tunnel ssh closed")
    
    def get_connection(self):
        self.open_tunnel()
        self.__connect()
        return self.conn

    def close_connection(self):
        self.conn.close()
        self.close_tunnel()

    def get_db_connection(self):
        self.__connect()
        return self.conn

    def close_db_connection(self):
        self.conn.close()
        logging.info("connection to db closed")

    def __connect(self):
        database_port = self.db_port
        if self.tunnel_mode:
            database_port = self.tunnel.local_bind_ports[0]
        self.conn = postgre.connect(database = self.db_name, user = self.db_user, password = self.db_password, host = self.db_host, port = database_port)
        logging.info("connection to postgres database succesfully created")


db_config = {"db_name":"postgres", "db_user":"postgres", "db_password":"Lavazza38", "db_host":"localhost", "db_port":""}
ssh_config = {"ssh_ip_address":"192.168.1.40", "ssh_port":22, "ssh_username":"mario", "ssh_password":"Lavazza38", "ssh_remote_bind_address":"localhost", "ssh_remote_bind_port":5432}
connector = PostgreConnector(db_config, ssh_config)
conn = connector.get_connection()
cur = conn.cursor()
cur.execute("select * from roles")
rows = cur.fetchall()
for row in rows:
    print row[1]
connector.close_connection()
