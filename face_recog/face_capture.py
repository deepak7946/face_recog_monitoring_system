import argparse
import cv2
import time
import os
import imutils

class face_capture:
    def __init__(self):
        self.detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.parent_out_dir = "images"
        self.vc = None
        return

    def capture_face(self):
        self.vc = cv2.VideoCapture(0)
        time.sleep(5)
        while True:
            _, frame = self.vc.read()
            frame = imutils.resize(frame, width=400)
            rects = self.detector.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                                                   scaleFactor=1.1, minNeighbors=5,
                                                   minSize=(30,30))
            for x, y, w, h in rects:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                print("Cleaning up and closing face capture")
                cv2.destroyAllWindows()
                break

def start_face_capture():
    cap = face_capture()
    cap.capture_face()

if __name__ == "__main__":
    start_face_capture()
