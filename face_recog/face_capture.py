import argparse
import cv2
import time
import os
import imutils

class FaceCapture:
    def __init__(self):
        haarcascade = os.path.join(os.path.dirname(__file__), 'haarcascade_frontalface_default.xml')
        self.detector = cv2.CascadeClassifier(haarcascade)
        self.parent_out_dir = "images"
        self.vc = None
        return

    def read_draw_rect(self):
        _, frame = self.vc.read()
        frame = imutils.resize(frame, width=400)
        rects = self.detector.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                                               scaleFactor=1.1, minNeighbors=5,
                                               minSize=(30,30))
        for x, y, w, h in rects:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        return frame

    def capture_face_imshow(self):
        self.vc = cv2.VideoCapture(0)
        time.sleep(5)
        while True:
            frame = self.read_draw_rect()
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("Cleaning up and closing face capture")
                break
        return

    def capture_face_feed(self):
        self.vc = cv2.VideoCapture(0)
        time.sleep(2)
        while True:
            frame = self.read_draw_rect()
            byteArray = cv2.imencode('.jpg', frame)[1].tobytes()
            img = (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + byteArray + b'\r\n')
            yield img
        return

    def __del__(self):
        self.vc.release()
        cv2.destroyAllWindows()
        self.vc = None

if __name__ == "__main__":
    cap = FaceCapture()
    cap.capture_face_feed()
