from flask import Blueprint, request, jsonify
from predictors.plant_predictor import predict as plant_predict, provide_tip

plant_bp = Blueprint('plant', __name__)

@plant_bp.route('/predict/plant', methods=['POST'])
def predict_plant():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    prediction = plant_predict(file.read())
    return jsonify({'prediction': prediction, 'tip': provide_tip(prediction)})
