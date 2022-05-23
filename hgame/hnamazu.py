# -*- coding: UTF-8 -*-
# Public package
import requests
# Private package
# Internal package


class NAMAZU():
    def __init__(self):
        self.port = 9638
        self.url = 'http://127.0.0.1:port/command'

    def send(self, command):
        requests.post(url=self.url.replace('port', '%d' % (self.port)), data=command.encode('utf-8'))

    def sends(self, commands):
        for command in commands:
            self.send(command)

    def set_port(self, port):
        self.port = port
