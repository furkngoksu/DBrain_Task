from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route('/products', methods=['GET'])
def get_products():
    # Define the path to the data.json file
    file_path = "data.json"
    
    # Check if the data.json file exists
    if os.path.exists(file_path):
        # Open and read the data.json file
        with open(file_path, 'r') as file:
            data = json.load(file)
        # Return the data as a JSON response
        return jsonify(data)
    else:
        # Return an error message if the file is not found
        return jsonify({"error": "data.json file not found"}), 404

if __name__ == '__main__':
    # Run the Flask app on host 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
