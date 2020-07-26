import face_recognition
import cv2
import json
import os
import glob
from imutils import paths
import pickle


class FaceRecog(object):
    def __init__(self):
        self.model = None
        self.img_path = os.path.join(os.path.dirname(__file__), 'images')
        self.detection_method = "cnn"
        self.face_encodings = {"encodings": [], "names": []}
        self.encode_file = os.path.join(os.path.dirname(__file__), "encoding.pkl")

    def encode_faces(self):
        img_list = list(paths.list_images(self.img_path))
        total_imgs = len(img_list)
        count = 1
        for img_path in img_list:
            name = img_path.split(os.path.sep)[-2]
            print("Processing image {}/{}" .format(count, total_imgs))
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_loc = face_recognition.face_locations(img, model=self.detection_method)
            encodings = face_recognition.face_encodings(img, face_loc)
            self.face_encodings["encodings"].append(encodings[0])
            self.face_encodings["names"].append(name)
            count += 1
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

    def load_encodings(self):
        if not os.path.exists(self.encode_file):
            raise FileNotFoundError("The file {} does not exist. Save images to image folder and encode perform encode to create an encodings file"
                                    .format(self.encode_file))
        with open(self.encode_file, "rb") as f:
            self.face_encodings = pickle.load(f)
        return

    def identify_face(self, img):
        #self.load_encodings()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_loc = face_recognition.face_locations(img, model=self.detection_method)
        encodings = face_recognition.face_encodings(img, face_loc)
        names = []
        for encoding in encodings:
            possible_ids = face_recognition.compare_faces(self.face_encodings["encodings"], encoding)
            name = "Unknown"
            if True in possible_ids:
                name = self.vote_for_id(possible_ids)
            names.append(name)
        return list(zip(face_loc, names))

    def vote_for_id(self, possible_ids):
        #Get the index of True in the list
        true_index = [index for (index, value) in enumerate(possible_ids) if value]
        counts = {}
        for i in true_index:
            name = self.face_encodings["names"][i]
            counts[name] = counts.get(name, 0) + 1
        name = max(counts, key=counts.get)
        return name
 
            

if __name__ == "__main__":
    fr = FaceRecog()
    fr.encode_faces()
    fr.save_encodings()