from flask import Flask,render_template
from flask_cors import CORS, cross_origin
from flask import request
from PIL import Image

import numpy as np
import cv2
import base64
import os

UPLOAD_FOLDER = './upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def dem_so_mat(face):

    # Khởi tạo bộ phát hiện khuôn mặt
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Chuyen gray
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    # Phát hiện khuôn mặt trong ảnh
    faces = face_cascade.detectMultiScale(gray, 1.2, 10)

    so_mat = len(faces)
    return so_mat


@app.route('/')
@cross_origin(origin='*')
def index():
    return render_template('index.html')

@app.route('/numberoffaces', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'fileUpload' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['fileUpload']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path) #save image to path
        image = cv2.imread(path)
        # count face in image
        face_numbers = dem_so_mat(image)
        # return
        #return "Số mặt là = " + str(face_numbers)
        return render_template('result.html', result = face_numbers)
    return render_template('index.html')

# Start Backend
if __name__ == '__main__':
    app.run()
