# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 22:26:48 2023

@author: HP
"""

from flask import Flask, render_template, Response, request
import cv2


def genframe():
    frame = cv2.imread('sourceQRCode.jpg')
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
    ret, buffer = cv2.imencode('.jpg', frame, encode_param)
    frame = buffer.tobytes()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
    
app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("frame.html")

@app.route("/image")
def image():
    return Response(genframe(), mimetype='multipart/x-mixed-replace; boundary=frame')

if(__name__=="__main__"):
    app.run()
    