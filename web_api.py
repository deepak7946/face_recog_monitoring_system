#!/usr/bin/python3.7

from flask import Flask, render_template, Response, redirect, url_for, request
import io
import cv2
import socket
import time
import threading
import json
from face_recog.face_capture import FaceCapture 
print("Flask App loading ... ")
app = Flask (__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login_page():
    error = None
    print(request.remote_addr)
    if request.method == 'POST':
        if valid_login(request.form["username"].lower(), request.form["password"]):
            return redirect(url_for("video_feed_page"))
        else:
            error = "Invalid credentials. Please try again"
    return render_template("login.html", error=error)

@app.route("/video_feed_page")
def video_feed_page():
    return render_template("video_feed.html")

@app.route("/video_feed")
def video_feed():
    fc = FaceCapture()
    return Response(fc.capture_face_feed(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def valid_login(username, password):
    with open("static/creds.json",  "r") as f:
        creds = json.load(f)
    if username in creds.keys():
        if password == creds[username]:
            return True
    return False

if __name__ == "__main__":
    web_app = app.run(host="0.0.0.0", port=8001, threaded=True)
    web_thread = threading.Thread(target=web_app)
    web_thread.start()
    web_thread.join()

