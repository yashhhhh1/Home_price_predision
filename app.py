from flask import Flask, request, jsonify
from waitress import serve
import os
import util
import warnings

# Ignore warnings from sklearn
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

# Initialize the Flask app
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

# Serve the app using waitress
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    util.load_saved_artifacts()  # Make sure artifacts are loaded
    serve(app, host='0.0.0.0', port=port)
