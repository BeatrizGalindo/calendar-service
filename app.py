from flask import Flask, request, jsonify

from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG for detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format for logs
)



app = Flask(__name__)

# events = []
events = [
    {"description": "New Year Celebration", "time": "2025-01-01T00:00:00", "id": 1},
    {"description": "Meeting", "time": "2025-01-02T10:00:00", "id": 2},
    {"description": "Meeting", "time": "2025-01-06T10:00:00", "id": 3},
    {"description": "Meeting", "time": "2025-01-06T10:30:00", "id": 4},
    {"description": "Meeting", "time": "2025-01-06T11:30:00", "id": 5},
]


DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


@app.route('/events', methods=['POST'])
def add_event():
    try:
        event = request.get_json()
        required_fields = ["description", "time", "id"]
        if not all(field in event for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        if any(existing_event["id"] == event["id"] for existing_event in events):
            return jsonify({"error": f"Event already exists with ID {event['id']}"}), 400

        events.append(event)
        logging.info(f"Event {event['id']} added to database")
        return jsonify(event), 201

    except Exception as e:
        logging.error(f"Error creating event: {str(e)}")
        return jsonify({"error": str(e)}), 400

@app.route('/events/<int:ID>', methods=['GET'])
def get_event(ID):
    try:
        logging.debug(f"Received request to retrieve event with ID: {ID}")
        datetime_format = request.args.get('datetime_format', '%Y-%m-%dT%H:%M:%S')
        logging.debug(f"Using datetime format: {datetime_format}")


        for event in events:
            logging.debug(f"Checking event: {event}")
            if event["id"] == ID:
                try:
                    event_time = datetime.strptime(event["time"], '%Y-%m-%dT%H:%M:%S')
                    event["time"] = event_time.strftime(datetime_format)
                    logging.debug(f"Formatted event time: {event['time']}")

                except ValueError:
                    logging.error(f"Could not parse time from event {event['id']}")
                    return jsonify({"error": f"Could not parse time from event {event['id']}"}), 400
                logging.info(f"Event {event['id']} retrieved from database")
                return jsonify(event), 200

        logging.warning(f"Event {ID} not found")
        return jsonify({"error": f"Event with ID {ID} not found"}), 404

    except Exception as e:
        logging.error(f"Error retrieving event: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/events', methods=['GET'])
def get_events():
    try:
        datetime_format = request.args.get('datetime_format', '%Y-%m-%dT%H:%M:%S')
        from_time_str = request.args.get('from_time')
        to_time_str = request.args.get('to_time')

        now = datetime.now()
        if not from_time_str:
            from_time = datetime(now.year, now.month, now.day)
        else:
            from_time = datetime.strptime(from_time_str, datetime_format)

        if not to_time_str:
            to_time = now
        else:
            to_time = datetime.strptime(to_time_str, datetime_format)

        if from_time > to_time:
            return jsonify({"error": f"From time {from_time} > to time {to_time}"}),400

        matching_events = []
        for event in events:
            event_time = datetime.strptime(event["time"], '%Y-%m-%dT%H:%M:%S')
            if from_time <= event_time <= to_time:
                event["time"] = event_time.strftime(datetime_format)
                matching_events.append(event)
        return jsonify({"events": matching_events}), 200
    except Exception as e:
        logging.error(f"Error retrieving events: {str(e)}")
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)

