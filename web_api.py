#!/usr/bin/python3.7

from flask import Flask, render_template, Response, redirect, url_for, request
import cv2
import time
from utils.face_capture import FaceCapture
import json
import argparse

app = Flask (__name__)
fc = FaceCapture()
fc.start_camera()


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        if valid_login(request.form["username"].lower(), request.form["password"]):
            return redirect(url_for("video_feed_page"))
        else:
            error = "Invalid credentials. Please try again"
    return render_template("login.html", error=error)

@app.route("/", methods=['GET', 'POST'])
@app.route("/video_feed_page", methods=["GET", "POST"])
def video_feed_page():
    error = None
    if request.method == "POST":
        name = request.form["name"].lower()
        if name == '':
            error = "Provide a name while capturing face"
        else:
            fc.take_snap(name)
    return render_template("video_feed.html", error=error)

@app.route("/video_feed")
def video_feed(op_name=None):
    return Response(fc.capture_face_feed(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def valid_login(username, password):
    with open("static/creds.json",  "r") as f:
        creds = json.load(f)
    if username in creds.keys():
        if password == creds[username]:
            return True
    return False

def connect_socket():
    parser = argparse.ArgumentParser(description='Provide IP of server for face recognition')
    parser.add_argument("--serverIP", type=str, help="Provide ip of face recog server. (Default: 127.0.0.1)",
                        default="127.0.0.1")
    args = parser.parse_args()
    fc.server_conn_agent.set_serverip(args.serverIP)
    fc.server_conn_agent.server_connect()


if __name__ == "__main__":
    connect_socket()
    print("Flask App loading ... ")
    app.run(host="0.0.0.0", port=8001, threaded=True)

