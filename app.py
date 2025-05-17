# app.py
from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import cv2
import numpy as np
from datetime import datetime

app = Flask(__name__, static_folder='static')
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blend', methods=['POST'])
def blend():
    alpha = float(request.form.get('alpha', 0.5))
    beta = float(request.form.get('beta', 0.5))

    img1_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image1.jpg')
    img2_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image2.jpg')

    if not os.path.exists(img1_path) or not os.path.exists(img2_path):
        return jsonify({'error': 'Both images must be uploaded first.'}), 400

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    blended = cv2.addWeighted(img1, alpha, img2, beta, 0)

    output_filename = 'blended.jpg'
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    cv2.imwrite(output_path, blended)

    return jsonify({"url": f"/static/{output_filename}?t={datetime.now().timestamp()}"})

@app.route('/upload', methods=['POST'])
def upload():
    for i in [1, 2]:
        file = request.files.get(f'image{i}')
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'image{i}.jpg')
            file.save(filepath)
    return ('', 204)

@app.route('/download')
def download():
    path = os.path.join(app.config['UPLOAD_FOLDER'], 'blended.jpg')
    if os.path.exists(path):
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path='blended.jpg', as_attachment=True)
    return 'No image to download', 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
