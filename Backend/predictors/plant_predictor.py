
from flask import Flask, request, jsonify
import numpy as np
import cv2
from keras.models import load_model
import tensorflow as tf
import json

model = load_model('plant_disease_model.h5')
CLASS_NAMES = ('Tomato___Septoria_leaf_spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___healthy')

with open("../assets/plant_tips.json", "r") as file:
    tips_data = json.load(file)
    
tips = {name: tips_data[name] for name in tips_data}

def prepare_image(image_bytes):
    file_bytes = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    opencv_image = cv2.resize(opencv_image, (256, 256))
    opencv_image = opencv_image.reshape(1, 256, 256, 3)
    return opencv_image

def predict(image_bytes):
    image = prepare_image(image_bytes)
    prediction = model.predict(image)
    return CLASS_NAMES[np.argmax(prediction)]

def provide_tip(name): 
    return tips[name]
