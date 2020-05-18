
import json
import tensorflow as tf
import numpy as np
import os
import random
import string

from flask import Flask, request


app = Flask(__name__)

from tensorflow.python.keras.backend import set_session
sess = tf.Session()
graph = tf.get_default_graph()

set_session(sess)

model = tf.keras.models.load_model('model.h5')

feature_model = tf.keras.Model(model.inputs, [layer.output for layer in model.layers])

_, (x_test, _) = tf.keras.datasets.mnist.load_data()
x_test = x_test / 255.

def get_prediction():
    index = np.random.choice(x_test.shape[0])
    image = x_test[index]
    image_arr = np.reshape(image, (1, 784))
    global graph
    global sess
    with graph.as_default():
        set_session(sess)
        out = feature_model.predict(image_arr)
    return out, image

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        preds, image = get_prediction()
        final_preds = [p.tolist() for p in preds]
        return json.dumps({'prediction': final_preds, 'image': image.tolist()})
    return 'Welcome to the ml server'

if __name__ == '__main__':
    app.run()
