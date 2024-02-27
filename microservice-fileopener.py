from flask import Flask, jsonify
import json

app = Flask(__name__)

# Global variable for the filename
FILENAME = 'workouts.txt'

# Function to load workouts data from file
def load_workouts_from_file():
    try:
        with open(FILENAME, 'r') as file:
            data = json.load(file)
            # Return both data and a success message
            return data, "File opened successfully"
    except FileNotFoundError:
        return {}, "File not found"
    except json.JSONDecodeError:
        return {}, "Error decoding JSON from file"


# Route to get all workouts
@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts, message = load_workouts_from_file()
    # You could also include the success message in the response if you like
    return jsonify({"data": workouts, "message": message})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Copy and paste this to see data in file
# http://localhost:5000/fileopener
