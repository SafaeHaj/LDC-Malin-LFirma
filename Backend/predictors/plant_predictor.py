from pathlib import Path
import numpy as np
import cv2
from keras.models import load_model
from ultralytics import YOLO
import json


BASE_DIR   = Path(__file__).resolve().parent.parent
MODEL_DIR  = BASE_DIR / 'models'
ASSET_DIR  = BASE_DIR / 'assets'

MODEL_PATH = MODEL_DIR / 'plant_disease_model.h5'

model = load_model(MODEL_PATH)

yolo_model = YOLO('yolov8n.pt')
CLASS_NAMES = ('Tomato___Septoria_leaf_spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___healthy')

with open('../assets/plant_tips.json', 'r') as f:
    tips = json.load(f)

class PlantDetectionError(Exception):
    pass

def prepare_image(image_bytes):
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (256, 256))
    return img.reshape(1, 256, 256, 3)

def sanity_check(image_array, threshold=0.3):
    results = yolo_model.predict(source=image_array, verbose=False)
    r = results[0]
    confs = r.boxes.conf if hasattr(r.boxes, 'conf') else []
    if len(confs) == 0 or float(confs.max()) < threshold:
        raise PlantDetectionError('No plant detected')

def predict(image_bytes):
    img = prepare_image(image_bytes)
    sanity_check(img)
    preds = model.predict(img)
    confidence = preds.max()
    return CLASS_NAMES[int(np.argmax(preds))], confidence

def provide_tip(name):
    return tips.get(name, '')