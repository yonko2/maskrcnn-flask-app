import os
import tensorflow as tf
from model import load_model, visualize_image
from werkzeug import secure_filename
from flask import Flask, request, render_template


app = Flask(__name__)
x=None
graph = tf.get_default_graph()

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))     # uploads image/video file will save here.
        f.save(file_path)

        with graph.as_default():
            visualize_image(file_path,*x)
    return ""



if __name__ == '__main__':
    x = load_model()
    app.run()
