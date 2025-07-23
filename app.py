from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Crime Data in Mohali (Moved away from the safe route)
CRIME_DATA = [
    {"lat": 30.6900, "lon": 76.6900, "type": "Snatching"},
    {"lat": 30.7100, "lon": 76.7500, "type": "Molestation"},
    {"lat": 30.7250, "lon": 76.7700, "type": "Acid throwing"},
    {"lat": 30.7400, "lon": 76.6800, "type": "Murder"},
    {"lat": 30.7500, "lon": 76.6600, "type": "Physical Violence"},
]

@app.route("/get-crime-data", methods=["GET"])
def get_crime_data():
    return jsonify({"crimes": CRIME_DATA})

@app.route("/find-safe-route", methods=["POST"])
def find_safe_route():
    data = request.json
    start = data["start"]
    end = data["end"]

    # OSRM Free API (Doesn't require a key)
    osrm_url = f"https://router.project-osrm.org/route/v1/driving/{start['lon']},{start['lat']};{end['lon']},{end['lat']}?overview=full&geometries=geojson"

    response = requests.get(osrm_url)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch safe route"}), 500

if __name__ == "__main__":
    app.run(debug=True)
