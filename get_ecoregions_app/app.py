
import os
import geopandas as gpd
from shapely.geometry import Point
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Read the file relative to this script
parquet_path = os.path.join(os.path.dirname(__file__), 'ecoregions4.parquet')
US4 = gpd.read_parquet(parquet_path)
US4 = gpd.GeoDataFrame(US4, geometry='geometry', crs='EPSG:4326')

def get_eco4(lat, lon):
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return ['Latitude and longitude not valid', 'Not valid', 'Not valid', 'Not valid']
    point = Point(lon, lat)
    for i in range(len(US4)):
        if point.within(US4.loc[i, "geometry"]):
            return [
                US4.loc[i, 'L1_KEY'],
                US4.loc[i, 'L2_KEY'],
                US4.loc[i, 'L3_KEY'],
                US4.loc[i, 'L4_KEY']
            ]
    return ['Latitude and longitude outside of US.', 'Not valid', 'Not valid', 'Not valid']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_ecoregion', methods=['POST'])
def get_ecoregion():
    data = request.get_json()
    lat = float(data['latitude'])
    lon = float(data['longitude'])
    result = get_eco4(lat, lon)
    return jsonify({
        'Level_1': result[0],
        'Level_2': result[1],
        'Level_3': result[2],
        'Level_4': result[3]
    })

if __name__ == '__main__':
    app.run(debug=True)

