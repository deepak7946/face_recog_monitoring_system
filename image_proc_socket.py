import cv2
from utils.face_recog import FaceRecog
import pickle
import socket

HOST =''
PORT=8002
HEADER_LEN = 10

fr = FaceRecog()
fr.load_encodings()


class server_socket:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        print("Binding completed")
        self.sock.listen(10)
        print("Server listening for connection")
        return

    def run(self):
        self.watch_connection()

    def watch_connection(self):
        conn, addr = self.sock.accept()
        print("[{}] connected to server" .format(addr))
        while True:
            msg = b''
            new_frame = True
            while True:
                rec_data = conn.recv(1000000)
                if len(rec_data) != 0:
                    if new_frame:
                        msg_len = int(rec_data[:HEADER_LEN])
                        new_frame = False
                    msg += rec_data
                    if len(msg)-HEADER_LEN == msg_len:
                        break
            frame = pickle.loads(msg[HEADER_LEN:])
            new_frame = True
            msg = b''
            response = self.predict_face(frame)
            conn.sendall(response)
        return

    def predict_face(self, frame):
        name_loc = fr.identify_face(frame)
        response = {"status": "Success", "data": name_loc}
        response = pickle.dumps(response)
        return response

server = server_socket()
server.run()