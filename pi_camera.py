#!/usr/bin/python3.7

from flask import Flask, render_template, Response, redirect, url_for, request
import io
import cv2
import socket
import time
import threading
import json
#from flask.flask_login import login_required

print("Flask App loading ... ")
app = Flask (__name__)
print("Creating vide capture obj")
video = cv2.VideoCapture(0)
#print("Setting Resolution")
#video.set(3, 320)
#video.set(4, 320)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    error = None
    with open("static/creds.json", "r") as f:
        creds = json.load(f)
    if request.method == 'POST':
        username = request.form["username"].lower()
        password = request.form["password"]
        if username in creds.keys():
            if password == creds[username]:
                return redirect(url_for("video_feed_page"))
            else:
               error = "Invalid credentials. Please try again"
        else:
            error = "Invalid credentials. Please try again"
    return render_template("login.html", error=error)

@app.route("/")
def home_page():
    return redirect(url_for("login_page"))

def gen_camera():
    while True:
        _, frame = video.read()
        byteArray = cv2.imencode('.jpg', frame)[1].tobytes()
        img = (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + byteArray + b'\r\n')
        yield(img)

@app.route("/video_feed_page")
#@login_required
def video_feed_page():
    return render_template("video_feed.html")

@app.route("/video_feed")
def video_feed():
    return Response(gen_camera(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    web_app = app.run(host="0.0.0.0", port=8001, threaded=True)
    web_thread = threading.Thread(target=web_app)
    web_thread.start()
    web_thread.join()

