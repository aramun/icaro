import psycopg2 as postgre
from sshtunnel import open_tunnel
import icaro.core.utils as utils
from icaro.core.utils.ssh_tunnel import SshTunnel
import logging
import psycopg2.extras

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
        """
        self.__map_database_config(database_config)
        self.ssh_tunnel = SshTunnel(ssh_tunnel_config)
        self.tunnel_mode = False

    def __map_database_config(self, database_config):
        self.db_name = database_config["db_name"]
        self.db_user = database_config["db_user"]
        self.db_password = database_config["db_password"]
        self.db_host = database_config["db_host"]
        self.db_port = database_config["db_port"]

    def get_connection(self):
        self.tunnel_mode = self.ssh_tunnel.open_tunnel()
        self.__connect()
        return self.conn
    
    def get_connection_dict_cursor(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return cur

    def close_connection(self):
        self.conn.close()
        self.ssh_tunnel.close_tunnel()

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

