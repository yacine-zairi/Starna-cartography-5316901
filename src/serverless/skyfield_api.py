from flask import Flask, request, jsonify
from skyfield.api import load, Topos, load_constellation_map
from datetime import datetime
import os

app = Flask(__name__)

# Assuming 'de421.bsp' is in a 'data' subdirectory relative to this script
KERNEL_PATH = os.path.join(os.path.dirname(__file__), 'data')
earth = load.path(os.path.join(KERNEL_PATH, 'de421.bsp'))
ts = load.timescale()
planets = load('de421.bsp')
constellation_map = load_constellation_map()

@app.route('/celestial_positions', methods=['POST'])
def get_celestial_positions():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    datetime_str = data.get("datetime")
    if not all((latitude, longitude, datetime_str)):
      return jsonify({"error": "Missing parameters"}), 400
    try:  
      dt = datetime.fromisoformat(datetime_str)
    except ValueError:  
      return jsonify({"error": "Invalid datetime format"}), 400

    observer = earth + Topos(latitude_degrees = latitude, longitude_degrees = longitude)
    time = ts.from_datetime(dt)  
    astrometric = observer.at(time)
    
    # Sirius position calculation
    sirius = planets['Sirius']
    apparent = astrometric.observe(sirius)
    ra, dec, distance = apparent.radec()
    sirius_ra, sirius_dec = ra.degrees, dec.degrees

    #Sun position calculation
    sun = planets['Sun']
    sun_apparent = astrometric.observe(sun)
    sun_ra, sun_dec, sun_distance = sun_apparent.radec()

    return jsonify(
        {
            "sirius_ra": sirius_ra,
            "sirius_dec": sirius_dec,
            "sun_ra": sun_ra,
            "sun_dec": sun_dec,
        }
    )

if __name__ == '__main__':
    app.run(debug=True)