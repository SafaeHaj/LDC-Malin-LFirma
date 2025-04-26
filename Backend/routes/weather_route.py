from flask import Blueprint, request, jsonify
from predictors.weather_predictor import predict as weather_predict

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/api/weather', methods=['POST'])
def predict_weather():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        prediction = weather_predict(data)
        return jsonify({"prediction": prediction}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
