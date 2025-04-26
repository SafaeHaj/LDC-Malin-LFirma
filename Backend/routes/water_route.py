from flask import Blueprint, request, jsonify
from predictors.water_predictor import predict_depletion as water_predict
from sensor_reader import get_latest

water_bp = Blueprint('water', __name__)

def get_water_params(data):
    return {
        'rain_value': data.get('rain_value'),
        'water_level': data.get('water_level'),
        'water_sensor_level': data.get('water_sensor_level'),
        'pump_status': data.get('pump_status'),
    }
    
@water_bp.route('/api/predict/watertank', methods=['POST'])
def predict_watertank():
    data = get_latest()
    water_data = get_water_params(data)
    if not water_data:
        return jsonify({'error': 'No JSON data'}), 400

    prediction = water_predict(water_data)
    return jsonify({'tank_water_usage_score': prediction})


@water_bp.route('/predict/well', methods=['POST'])
def predict_well():
    data = get_latest()
    water_data = get_water_params(data)
    if not water_data:
        return jsonify({'error': 'No JSON data'}), 400

    prediction = water_predict(water_data)
    return jsonify({'well_water_usage_score': prediction})
