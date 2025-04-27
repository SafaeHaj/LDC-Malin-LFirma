from flask import Flask

from routes.weather_route import weather_bp
from db.connect_postgres import connect_to_db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# app.register_blueprint(plant_bp)
# app.register_blueprint(soil_bp)
# app.register_blueprint(water_bp)
app.register_blueprint(weather_bp)


if __name__ == '__main__':
    connection = connect_to_db()
    if connection:
        print("Database connection established.")
    else:
        print("Failed to establish database connection.")
    app.run(host='0.0.0.0', port=8080)
