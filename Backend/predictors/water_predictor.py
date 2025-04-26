# water_predictor.py
import numpy as np
from keras.models import load_model
from db.connect_postgres import connect_to_db
from sqlalchemy import text

model = load_model('water_model.h5')

def fetch_latest_window(window_size):
    conn = connect_to_db()
    df = conn.execute(
        text(
            "SELECT flow_rate, usage_last_hour FROM water_readings "
            "ORDER BY timestamp DESC LIMIT :n"
        ),
        {"n": window_size}
    ).fetchall()
    conn.close()
    arr = np.array(df)[::-1]
    return arr.reshape(1, window_size, 2)

def predict_depletion(window_size, current_tank_level):
    hours = 0
    remaining = current_tank_level
    history = fetch_latest_window(window_size)[0].tolist()
    while remaining > 0 and hours < 168:
        inp = np.array(history[-window_size:]).reshape(1, window_size, 2)
        usage = float(model.predict(inp)[0][0])
        remaining -= usage
        history.append([0.0, usage])
        hours += 1
    return hours
