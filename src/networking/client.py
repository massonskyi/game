# src/networking/client.py

import socket

class Client:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.server_address, self.server_port))

    def send(self, data):
        self.socket.sendall(data)

    def receive(self):
        return self.socket.recv(1024)
