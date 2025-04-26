from flask import Blueprint, request, jsonify
from predictors.water_predictor import predict_depletion as water_predict

water_bp = Blueprint('water', __name__)

@water_bp.route('/predict/watertank', methods=['POST'])
def predict_watertank():
    water_data = request.json
    if not water_data:
        return jsonify({'error': 'No JSON data'}), 400

    prediction = water_predict(water_data)
    return jsonify({'tank_water_usage_score': prediction})


@water_bp.route('/predict/well', methods=['POST'])
def predict_well():
    water_data = request.json
    if not water_data:
        return jsonify({'error': 'No JSON data'}), 400

    prediction = water_predict(water_data)
    return jsonify({'well_water_usage_score': prediction})
