import socket

HOST = "25.42.224.13"
PORT = 6066

class conn:
    self.sock = None
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        
    def connect(self):
        self.sock.sendall("CONNECT\n".encode())
        data = self.sock.recv(1024).decode()
        
        print(data)
        return data