from flask import Flask, request, jsonify

import datetime


app = Flask(__name__)

events = []

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


@app.route('/events', methods=['POST'])
def add_event():
    try:
        data = request.json
        if "description" not in data or "time" not in data or "id" not in data:
            return jsonify({"error": "Missing data"}), 400
        try:
            datetime.datetime.strptime(data["time"], DATETIME_FORMAT)
        except ValueError:
            return jsonify({"error": "Invalid time"}), 400

        events.append(data)
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

