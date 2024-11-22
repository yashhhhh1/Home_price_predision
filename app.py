from flask import Flask, request, jsonify
from waitress import serve
import util
import warnings

# Ignore warnings from sklearn
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

# Initialize the Flask app - remove the second initialization
# You're importing app from app.server and then creating a new Flask instance
# which could cause conflicts
app = Flask(__name__)

# Route for getting location names
@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Route for predicting home prices
@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    util.load_saved_artifacts()  # Make sure artifacts are loaded
    serve(app, host='0.0.0.0', port=8080)