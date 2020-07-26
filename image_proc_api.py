from flask import Flask, Response, request, jsonify
import cv2
from face_recog.face_recog import FaceRecog
import numpy as np
import json

img_app = Flask(__name__)
fr = FaceRecog()
fr.load_encodings()

@img_app.route("/predict", methods=["POST"])
def predict_face():
    data = request.data
    nparr = np.fromstring(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    name_loc = fr.identify_face(img)
    #name_loc = json.dumps(name_loc)
    response = {"status": "Success", "data": name_loc}
    response = json.dumps(response)
    return Response(response=response, status=200, mimetype="application/json")

if __name__ == "__main__":
    img_app.run(host="0.0.0.0", port=8002)