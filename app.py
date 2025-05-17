from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

image1_path = None
image2_path = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global image1_path, image2_path
    if request.method == 'POST':
        image1 = request.files['image1']
        image2 = request.files['image2']

        image1_path = os.path.join(UPLOAD_FOLDER, 'image1.jpg')
        image2_path = os.path.join(UPLOAD_FOLDER, 'image2.jpg')

        image1.save(image1_path)
        image2.save(image2_path)

        return render_template('index.html', uploaded=True)
    return render_template('index.html', uploaded=False)

@app.route('/blend', methods=['POST'])
def blend():
    global image1_path, image2_path
    alpha = float(request.form['alpha'])
    beta = float(request.form['beta'])

    if not image1_path or not image2_path:
        return jsonify({'error': 'Images not uploaded yet.'}), 400

    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)
    img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    blended = cv2.addWeighted(img1, alpha, img2, beta, 0)
    blended_path = os.path.join(UPLOAD_FOLDER, 'blended.jpg')
    cv2.imwrite(blended_path, blended)

    return jsonify({'blended_url': blended_path})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
