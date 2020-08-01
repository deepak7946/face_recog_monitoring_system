from utils.face_recog import FaceRecog

if __name__ == "__main__":
    fr = FaceRecog()
    fr.encode_faces()
    fr.save_encodings()
