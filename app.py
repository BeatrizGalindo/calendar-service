import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify

# Constants
EVENTS_FILE = 'events.json'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Flask app
app = Flask(__name__)

# Load and Save Event Helpers
def load_events():
    if os.path.exists(EVENTS_FILE):
        try:
            with open(EVENTS_FILE, 'r') as file:
                events = json.load(file)
                logging.info(f"Loaded events: {events}")
                return events
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}")
    logging.debug("No events file found or file is empty.")
    return []

def save_events(events):
    try:
        with open(EVENTS_FILE, 'w') as file:
            json.dump(events, file, indent=4)
        logging.info(f"Events saved to {os.path.abspath(EVENTS_FILE)}")
    except Exception as e:
        logging.error(f"Error saving events: {e}")


# Event Processing Logic
def process_event(event, events):
    """
    Validates and processes an event.

    Args:
        event (dict): The event data.
        events (list): The current list of events.

    Returns:
        tuple: (response_data, status_code)
    """
    required_fields = ["description", "time", "id"]
    if not all(field in event for field in required_fields):
        return {"error": "Missing required fields"}, 400

    if any(existing_event["id"] == event["id"] for existing_event in events):
        return {"error": f"Event already exists with id {event['id']}"}, 400

    events.append(event)
    save_events(events)
    logging.info(f"Event {event['id']} added.")
    return event, 201

def find_event_by_id(event_id, events, datetime_format):
    """
    Retrieve an event by its ID and format the time if necessary.

    :param event_id: The ID of the event to retrieve.
    :param events: The list of events.
    :param datetime_format: The format for the event time.
    :return: A tuple containing the event (if found) and the HTTP status code.
    """
    for event in events:
        if event["id"] == event_id:
            try:
                event_time = datetime.strptime(event["time"], DATETIME_FORMAT)
                event["time"] = event_time.strftime(datetime_format)
                logging.info(f"Event time {event['time']} found and formatted.")
                return event, 200
            except ValueError:
                logging.error(f"Invalid time format for event {event_id}.")
                return {"error": f"Invalid time format for event {event_id}."}, 400

    logging.warning(f"Event {event_id} not found.")
    return {"error": f"Event with id {event_id} not found."}, 404

def retrieve_events(events, datetime_format, from_time_str=None, to_time_str=None):
    """
    Retrieve all events within a specific time range.

    :param events: List of all events.
    :param datetime_format: Desired datetime format for input/output.
    :param from_time_str: Start time in string format (optional).
    :param to_time_str: End time in string format (optional).
    :return: A tuple containing the matching events and HTTP status code.
    """
    try:
        now = datetime.now()
        from_time = datetime.strptime(from_time_str, datetime_format) if from_time_str else datetime(now.year, now.month, now.day)
        to_time = datetime.strptime(to_time_str, datetime_format) if to_time_str else now

        if from_time > to_time:
            return {"error": "'from_time' cannot be after 'to_time'."}, 400

        matching_events = [
            {**event, "time": datetime.strptime(event["time"], DATETIME_FORMAT).strftime(datetime_format)}
            for event in events
            if from_time <= datetime.strptime(event["time"], DATETIME_FORMAT) <= to_time
        ]
        return {"events": matching_events}, 200
    except ValueError as ve:
        logging.error(f"Invalid date format: {ve}")
        return {"error": "Invalid date format."}, 400
    except Exception as e:
        logging.error(f"Error retrieving events: {e}")
        return {"error": "An error occurred."}, 500

# Routes
@app.route('/events', methods=['POST'])
def add_event():
    """Handle the POST request to add an event."""
    try:
        event = request.get_json()
        response_data, status_code = process_event(event, events)
        return jsonify(response_data), status_code
    except Exception as e:
        logging.error(f"Error adding event: {e}")
        return jsonify({"error": "Invalid event data."}), 400

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """HTTP endpoint to retrieve a specific event by ID."""
    try:
        datetime_format = request.args.get('datetime_format', DATETIME_FORMAT)
        result, status_code = find_event_by_id(event_id, events, datetime_format)
        return jsonify(result), status_code
    except Exception as e:
        logging.error(f"Error retrieving event {event_id}: {e}")
        return {"error": f"Error retrieving event {event_id}."}, 500

@app.route('/events', methods=['GET'])
def get_events():
    """Retrieve all events within a specific time range."""
    datetime_format = request.args.get('datetime_format', DATETIME_FORMAT)
    from_time_str = request.args.get('from_time')
    to_time_str = request.args.get('to_time')

    response, status_code = retrieve_events(events, datetime_format, from_time_str, to_time_str)
    return jsonify(response), status_code

# Load initial events
events = load_events()

# Main
if __name__ == '__main__':
    app.run(debug=True)
