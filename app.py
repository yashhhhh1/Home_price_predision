from flask import Flask, request, jsonify
import util
import warnings
import os

# Ignore warnings from sklearn
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

# Initialize the Flask app
app = Flask(__name__)

# Load artifacts at startup, not just when running as main
print("Loading artifacts...")
util.load_saved_artifacts()
print("Artifacts loaded successfully")

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
    from waitress import serve
    util.load_saved_artifacts()
    serve(app, host='0.0.0.0', port=8080)