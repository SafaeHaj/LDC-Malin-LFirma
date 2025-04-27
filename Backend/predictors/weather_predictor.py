import os
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/forecast.json"

def get_weather(city_name):
    print(API_KEY)
    params = {
        "key": API_KEY,
        "q": city_name,
        "days": 7,
        "dt": datetime.today().strftime('%Y-%m-%d'),
        "aqi": "yes",
        "alerts": "yes"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def predict(weather_data):
    if not weather_data:
        return None

    current = weather_data["current"]
    forecast = weather_data["forecast"]["forecastday"]

    summary = {
        "humidity": current["humidity"],
        "wind_kph": current["wind_kph"],
        "rain_mm": current["precip_mm"],
        "condition": current["condition"]["text"],
        "temperature_c": current["temp_c"],
        "air_quality": {
            "co": current["air_quality"]["co"],
            "no2": current["air_quality"]["no2"],
            "o3": current["air_quality"]["o3"],
            "so2": current["air_quality"]["so2"],
            "pm2_5": current["air_quality"]["pm2_5"],
            "pm10": current["air_quality"]["pm10"],
            "us_epa_index": current["air_quality"]["us-epa-index"],
            "gb_defra_index": current["air_quality"]["gb-defra-index"]
        },
        "forecast_week": [
            {
                "date": day["date"],
                "condition": day["day"]["condition"]["text"],
                "maxtemp_c": day["day"]["maxtemp_c"],
                "mintemp_c": day["day"]["mintemp_c"],
                "avgtemp_c": day["day"]["avgtemp_c"],
                "daily_chance_of_rain": day["day"]["daily_chance_of_rain"],
                "maxwind_kph": day["day"]["maxwind_kph"]
            }
            for day in forecast
        ]
    }

    return summary
