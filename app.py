from socketserver import TCPServer
from http.server import SimpleHTTPRequestHandler

import pandas as pd

from socket import AF_INET6
from ipaddress import ip_address
from ipaddress import IPv6Address, IPv4Address

import subprocess
import sys

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TCPServer6(TCPServer):
    address_family = AF_INET6

    def __init__(self, addr, Handler):
        super().__init__(addr, Handler)

class HTTPServersHandle():
    def __init__(self, auto= True, ipv6=False, port=8000):
        self.protcol = IPv6Address if ipv6 else IPv4Address
        self.server = TCPServer6 if ipv6 else TCPServer
        self.Handler = SimpleHTTPRequestHandler

        self.ipconfig = "./config_ipv6" if ipv6 else "./config_ipv4"
        if auto:
            try:
                with open(self.ipconfig, "r") as f:
                    self.addr = f.read(), port
            except FileNotFoundError:
                raise Exception("ip config file is not found.")
            except Exception as e:
                raise e
            if self.addr[0] == "":
                raise Exception("IP addres is not configured.")
        else:
            self.addr = input("input IP addr"), port
        
        logger.info("addr info is set %s and port info is set %s"%(self.addr[0], self.addr[1]))
        

    def start_server(self):
        with self.server(self.addr, self.Handler) as httpd:
            try:
                if ipv6:
                    logger.info("server is listening at http://[%s]:%s"%(self.addr[0], self.addr[1]))
                else:
                    logger.info("server is listening at http://%s:%s"%(self.addr[0], self.addr[1]))
                httpd.serve_forever()
            except KeyboardInterrupt:
                del httpd
                logger.info("stop server")

if __name__ == "__main__":
    ipv6 = False
    try:
        if sys.argv[1] == "ipv6":
            ipv6 = True
    except IndexError:
        pass

    if ipv6:
        sv_handle = HTTPServersHandle(ipv6=True)
        sv_handle.start_server()
    else:
        sv_handle = HTTPServersHandle(ipv6=False)
        sv_handle.start_server()
