from flask import Blueprint, request, jsonify
from predictors.plant_predictor import predict as plant_predict, provide_tip, PlantDetectionError

plant_bp = Blueprint('plant', __name__)

@plant_bp.route('/predict/plant', methods=['POST'])
def predict_plant():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        pred, confidence  = plant_predict(file.read())
        tip = provide_tip(pred)
        return jsonify({'prediction': pred, 'pred_confidence':confidence, 'tip': tip})
    except PlantDetectionError as e:
        return jsonify({'error': str(e)}), 400
