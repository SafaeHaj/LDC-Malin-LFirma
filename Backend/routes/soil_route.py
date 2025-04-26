from flask import Blueprint, jsonify
from predictors.soil_predictor import predict as soil_predict
from sensor_reader import get_latest

soil_bp = Blueprint('soil', __name__)

def get_soil_params(data):
    return {
        'temperature': data.get('temperature'),
        'humidity': data.get('humidity'),
        'soil_moisture': data.get('soil_moisture'),
    }

@soil_bp.route('/predict/soil', methods=['GET'])
def predict_soil():
    data = get_latest()
    sensor_data = get_soil_params(data)
    if not sensor_data:
        return jsonify({'error': 'No sensor data available'}), 503
    score = soil_predict(sensor_data)
    return jsonify({'soil_health_score': score})
