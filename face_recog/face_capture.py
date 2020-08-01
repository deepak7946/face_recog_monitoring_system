import cv2
import time
import os
import imutils
from face_recog.connection_agent import connection_agent


class FaceCapture:
    def __init__(self):
        haarcascade = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')
        self.detector = cv2.CascadeClassifier(haarcascade)
        self.out_dir = os.path.join(os.path.dirname(__file__), "images/")
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)
        self.vc = None
        self.server_conn_agent = connection_agent()
        return

    def read_draw_rect(self, save_orig=False, path=None, identify=True):
        _, frame = self.vc.read()
        frame = imutils.resize(frame, width=400)
        if save_orig:
            cv2.imwrite(path, frame)
        else:
            if self.server_conn_agent.get_server_status() == "Connected":
                try:
                    response = self.server_conn_agent.send_frame(frame)
                    name_loc = response['data']
                    for (top, right, bottom, left), name in name_loc:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
                        y = top - 15 if top - 15 > 15 else top + 15
                        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (0, 255, 0), 1)
                except TypeError:
                    print("Server connection lost. Rolling back to local face detection without recognition")
                    pass
            else:
                rects = self.detector.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                                                       scaleFactor=1.1, minNeighbors=5,
                                                       minSize=(30,30))
                for x, y, w, h in rects:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        return frame

    def start_camera(self):
        self.vc = cv2.VideoCapture(0)
        time.sleep(2)
        return

    def capture_face_imshow(self):
        self.start_camera()
        while True:
            frame = self.read_draw_rect()
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("Cleaning up and closing face capture")
                break
        return

    def setup_path(self, op_name):
        path = os.path.join(self.out_dir, "{}/" .format(op_name))
        if not os.path.exists(path):
            os.mkdir(path)
        list_files = os.listdir(path)
        if len(list_files) == 0:
            file = "00000"
        else:
            file = int(list_files[-1].split(".png")[0])
            file = str(file+1).zfill(5)
        path = os.path.join(path, "{}.png" .format(file))
        return path

    def take_snap(self, name):
        path = self.setup_path(name)
        self.read_draw_rect(save_orig=True, path=path)

    def capture_face_feed(self):
        while True:
            frame = self.read_draw_rect()
            byteArray = cv2.imencode('.jpg', frame)[1].tobytes()
            img = (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + byteArray + b'\r\n')
            yield img
        return
    
    def __del__(self):
        if not self.vc is None:
            self.vc.release()
            cv2.destroyAllWindows()
        self.vc = None


if __name__ == "__main__":
    cap = FaceCapture()
