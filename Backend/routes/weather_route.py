from flask import Blueprint, request, jsonify
from predictors.weather_predictor import predict, get_weather

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/api/weather', methods=['GET'])
def predict_weather():
    try:
        data = get_weather("Benguerir")
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        prediction = predict(data)
        return jsonify({"prediction": prediction}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
