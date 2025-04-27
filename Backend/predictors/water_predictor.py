import numpy as np
from keras.models import load_model
from db.connect_postgres import connect_to_db
from sqlalchemy import text

BASE_DIR   = Path(__file__).resolve().parent.parent
MODEL_DIR  = BASE_DIR / 'models'
ASSET_DIR  = BASE_DIR / 'assets'

MODEL_PATH = MODEL_DIR / 'water_model.h5'
model = load_model(MODEL_PATH)

def fetch_latest_window(window_size):
    conn = connect_to_db()
    result = conn.execute(
        text(
            "SELECT * FROM water_log "
            "ORDER BY time DESC LIMIT :n"
        ),
        {"n": window_size}
    ).fetchall()
    conn.close()
    if not result or len(result) < window_size:
        return None
    arr = np.array(result)[::-1]
    return arr.reshape(1, window_size, 2)

def generate_synthetic_history(window_size, default_usage=0.5):
    synthetic = np.array([[0.0, default_usage]] * window_size)
    return synthetic.reshape(1, window_size, 2)

def predict_depletion(window_size, current_tank_level):
    hours = 0
    remaining = current_tank_level
    history = fetch_latest_window(window_size)

    if history is None:
        history = generate_synthetic_history(window_size)
    
    history = history[0].tolist()
    while remaining > 0 and hours < 168:
        inp = np.array(history[-window_size:]).reshape(1, window_size, 2)
        usage = float(model.predict(inp, verbose=0)[0][0])
        usage = max(usage, 0)  # Ensure no negative usage
        remaining -= usage
        history.append([0.0, usage])
        hours += 1
    
    return hours
