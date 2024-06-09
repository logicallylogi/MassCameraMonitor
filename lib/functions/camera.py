from flask import Flask, render_template, Response, request, send_from_directory
import logging
import cv2 as cv

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
camera = cv.VideoCapture(0)

def get():
    _, frame = camera.read()
    response = cv.imencode('.jpg', frame)[1].tobytes()
    return response

@app.route('/')
def video_static():
    return Response(get(),
            mimetype='image/jpeg')

def start():
    app.run(host='0.0.0.0', debug=False, port=5555)