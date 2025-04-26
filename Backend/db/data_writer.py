from datetime import datetime
from connect_postgres import engine
from sqlalchemy import text

_prev_pump = None

def write_soil(data):
    with engine.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO soil (time, temperature, humidity, moisture)"
                "VALUES (:time,:temperature, :humidity, :moisture)"
            ),
            time=datetime.now(datetime.timezone.utc),
            temperature=data['temperature'],
            humidity=data['humidity'],
            moisture=data['soil_moisture']
        )

def write_watering(data):
    global _prev_pump
    pump = data['pump_status']
    if _prev_pump is None or pump != _prev_pump:
        with engine.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO watering_log"
                    "(tank_level, well_level, watered_at, pump_status, rain_value)"
                    "VALUES (:tank, :well, :time, :pump, :rain)"
                ),
                tank=data['water_level'],
                well=data['water_sensor_level'],
                time=datetime.now(datetime.timezone.utc),
                pump=pump,
                rain=data['rain_value']
            )
        _prev_pump = pump

def write_all(data):
    write_soil(data)
    write_watering(data)