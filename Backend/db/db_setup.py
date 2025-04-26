from connect_postgres import engine
from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(text(
        "CREATE TABLE IF NOT EXISTS soil ("
        "temperature REAL,"
        "humidity REAL,"
        "moisture REAL,"
        "read_at TIMESTAMP DEFAULT now()"
        ")"
    ))
    conn.execute(text(
        "CREATE TABLE IF NOT EXISTS watering_log ("
        "id SERIAL PRIMARY KEY,"
        "tank_level REAL,"
        "well_level REAL,"
        "watered_at TIMESTAMP,"
        "pump_status BOOLEAN,"
        "rain_value REAL"
        ")"
    ))