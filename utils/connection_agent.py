import pickle
import socket
import time

HEADER_LEN = 10

class connection_agent:
    def __init__(self):
        self.server_status = "Not Connected"
        self.server_ip = "127.0.0.1"
        self.server = None
        self.server_connect()
        return
    
    def get_server(self):
        return self.server

    def get_server_status(self):
        return self.server_status

    def server_connect(self):
        try:
            print("Connecting to Server")
            self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.server.connect((self.server_ip, 8002))
            print("Connected to server {}" .format(self.server))
            self.server_status = "Connected"
        except OSError as errmsg:
            self.server_status = "Not Connected"
            print("ERROR: {}" .format(errmsg))
            self.server = None
        return

    def close_connection(self):
        try:
            self.server.close()
        except Exception as errmsg:
            print("Close Connection Failed: {}" .format(errmsg))
            pass

    def __del__(self):
        self.close_connection()

    def send_frame(self, frame):
        try:
            data = pickle.dumps(frame)
            data = bytes(f'{len(data):<{HEADER_LEN}}', "utf-8") + data
            self.server.sendall(data)
            response = self.server.recv(512)
            response =  pickle.loads(response)
        except Exception:
            msg = "Connection to server {} failed" .format(self.server_ip)
            self.close_connection()
            self.server_status = "Not Connected"
        return response