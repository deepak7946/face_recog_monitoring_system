import argparse
import cv2
import time
import os
import imutils
import glob

class FaceCapture:
    def __init__(self):
        haarcascade = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')
        self.detector = cv2.CascadeClassifier(haarcascade)
        self.out_dir = os.path.join(os.path.dirname(__file__), "images/")
        self.vc = None
        return

    def read_draw_rect(self, save_orig=False, path=None):
        _, frame = self.vc.read()
        frame = imutils.resize(frame, width=400)
        if save_orig:
            cv2.imwrite(path, frame)
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
    cap.start_camera()
    cap.take_snap("deepak")
