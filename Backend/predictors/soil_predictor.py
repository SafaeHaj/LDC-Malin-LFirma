# soil_predictor.py
import numpy as np
from datetime import datetime
from connect_postgres import connect_to_db, text

def get_db_data(sensor_data):
    with connect_to_db() as conn:
        result = conn.execute(
            text(
                "SELECT watered_at, tank_level FROM watering_log "
                "WHERE sensor_id = :sid ORDER BY watered_at DESC LIMIT 1"
            ),
            {"sid": sensor_data.get("sensor_id")}
    ).fetchone()
    return result
    
def predict(sensor_data):
    moisture = sensor_data["moisture"]
    temperature = sensor_data["temperature"]
    humidity = sensor_data["humidity"]
    now = datetime.now(datetime.timezone.utc)
    
    result = get_db_data(sensor_data)
    last_watered, tank_level = result or (None, None)
    hours_since = (now - last_watered).total_seconds() / 3600 if last_watered else None
    # simple heuristic: if moisture below 30% and >24h since watering, recommend irrigation
    should_water = moisture < 0.30 and (hours_since is None or hours_since > 24)
    return {
        "moisture": moisture,
        "temperature": temperature,
        "humidity": humidity,
        "hours_since_last_water": hours_since,
        "tank_level": tank_level,
        "should_water": should_water
    }
