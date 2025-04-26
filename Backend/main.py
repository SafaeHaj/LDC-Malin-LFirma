from flask import Flask
from routes.plant_route import plant_bp
from routes.soil_route import soil_bp
from routes.water_route import water_bp
from routes.weather_route import weather_bp
from connect_postgres import connect_to_db

app = Flask(__name__)
app.register_blueprint(plant_bp)
app.register_blueprint(soil_bp)
app.register_blueprint(water_bp)
app.register_blueprint(weather_bp)


if __name__ == '__main__':
    connection = connect_to_db()
    if connection:
        print("Database connection established.")
    else:
        print("Failed to establish database connection.")
    app.run(host='0.0.0.0', port=8000)
