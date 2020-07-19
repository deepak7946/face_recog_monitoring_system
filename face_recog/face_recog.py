import face_recognition
import cv2
import json
import os
import glob
from imutils import paths
import pickle


class FaceRecog:
    def __init__(self):
        self.model = None
        self.img_path = os.path.join(os.path.dirname(__file__), 'images')
        self.detection_method = "cnn"
        self.face_encodings = {"encodings": [], "names": []}
        self.encode_file = os.path.join(os.path.dirname(__file__), "encoding.pkl")

    def encode_faces(self):
        img_list = list(paths.list_images(self.img_path))
        for img_path in img_list:
            name = img_path.split(os.path.sep)[-2]
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_loc = face_recognition.face_locations(img, model=self.detection_method)
            encodings = face_recognition.face_encodings(img, face_loc)
            self.face_encodings["encodings"].append(encodings[0])
            self.face_encodings["names"].append(name)
        return

    def save_encodings(self):
        with open(self.encode_file, "wb") as f:
            pickle.dump(self.face_encodings, f)
        return

    def change_detec_method(self, method="cnn"):
        if method != "cnn" or method != "hog":
            raise ValueError("Only 'cnn' and 'hog' are accepted methods")
        self.detection_method = method
        return

if __name__ == "__main__":
    fr = FaceRecog()
    fr.encode_faces()
    #fr.save_encodings()