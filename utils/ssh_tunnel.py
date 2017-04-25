from sshtunnel import open_tunnel
import logging

class SshTunnel:

    def __init__(self, ssh_tunnel_config):
        """
            ssh_tunnel_config {
                ssh_ip_address: ip address server to connect
                ssh_port: port server to connect
                ssh_username: username
                ssh_password: password
                ssh_remote_bind_address: remote address to bind
                ssh_remote_bind_port: remote port to bind
            }
        """
        self.__map_ssh_config(ssh_tunnel_config)

    def __map_ssh_config(self, ssh_tunnel_config):
        self.ssh_ip_address = ssh_tunnel_config["ssh_ip_address"]
        self.ssh_port = ssh_tunnel_config["ssh_port"]
        self.ssh_username = ssh_tunnel_config["ssh_username"]
        self.ssh_password = ssh_tunnel_config["ssh_password"]
        self.ssh_remote_bind_address = ssh_tunnel_config["ssh_remote_bind_address"]
        self.ssh_remote_bind_port = ssh_tunnel_config["ssh_remote_bind_port"]

    def open_tunnel(self):
        self.tunnel = open_tunnel((self.ssh_ip_address, self.ssh_port), ssh_username=self.ssh_username, ssh_password = self.ssh_password, remote_bind_address=(self.ssh_remote_bind_address, self.ssh_remote_bind_port))
        self.tunnel.start()
        logging.info("tunnel ssh succesfully created and started")
        return True

    def close_tunnel(self):
        self.tunnel.close()
        logging.info("tunnel ssh closed")
