from flask import Blueprint, request, jsonify
from predictors.soil_predictor import predict as soil_predict

soil_bp = Blueprint('soil', __name__)

@soil_bp.route('/predict/soil', methods=['POST'])
def predict_soil():
    sensor_data = request.json
    if not sensor_data:
        return jsonify({'error': 'No JSON data'}), 400

    prediction = soil_predict(sensor_data)
    return jsonify({'soil_health_score': prediction})
