# Calendar Service

## Overview
The Calendar Service is a simple Python Flask application that allows users to create, retrieve, and filter calendar events. The service supports three main operations:

1. **Create an event**: Adds a new event to the calendar.
2. **Get an event by ID**: Retrieves a specific event based on its ID.
3. **Get events within a date range**: Retrieves all events that fall within a specified date range.

The service stores events persistently in a `JSON` file (`events.json`), and it provides flexible formatting for event date-time information using `strftime`/`strptime` formatting.

## Features

- **POST /events**: Accepts events with a description, time, and unique ID.
- **GET /events/<ID>**: Retrieves a specific event by its ID.
- **GET /events**: Retrieves all events within a specific time range (`from_time` to `to_time`). If not specify it will retrieve the events on the current day.

## Requirements

- Python 3.13
- Pip

To use a virtual environment, run:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

### Run the app
Use the following command to run the app on your terminal. 
```bash
python3 app.py 
```

### Access the app
The webserver is now accessible at [localhost:5000](http://127.0.0.1:5000)

### Testing
Unit tests are provided to validate the functionality. 
Run the tests using the following command.
```bash
python3 -m unittest test_app.py
```

## Docker

You can containerize the service using Docker. If you don't have Docker installed, follow the instructions on Docker's website to install it.

#### Build the Docker Image
In the root directory of your project, run the following command to build the Docker image:

```
docker build -t calendar-service .
```
#### Run the Docker Container
Once the image is built, run the container with the following command:
```
docker run -d -p 5001:5000 --name calendar-service-container calendar-service
```

#### Run tests inside the container

First access the container, in the terminal execute the following command to enter an interactive shell inside the running container:
```
docker exec -it calendar-service-container /bin/bash
```
Inside the container you can run the test as usual:
`python3 -m unittest test_app.py`

To exit the container form the terminal: `Control + D`


If you want to test the functionality of the app directly inside the Docker container you can access the container's shell:
`docker exec -it calendar-service-container bash`

Use the curl commands as described below in API endpoints, for example:
`curl -X POST -H "Content-Type: application/json" -d '{"description": "Meeting with John", "time": "2025-01-06T14:00:00", "id": 6}' "http://127.0.0.1:5000/events"`


### API Endpoints

### 1. POST/events
This endpoint accepts an event payload and stores the event in events.json.
```
{
    "description": "<FREE FORM EVENT DESCRIPTION>",
    "time": "<DATE TIME>",
    "id": "<NUMERIC ID>"
}
```
Example: 
`curl -X POST -H "Content-Type: application/json" -d '{"description": "Meeting with John", "time": "2025-01-06T14:00:00", "id": 1}' "http://127.0.0.1:5000/events"`
Response: 
```
{
    "description": "Meeting with John",
    "time": "2025-01-06T14:00:00",
    "id": 1
}
```

### 2. GET/events/ID
This endpoint retrieves an event by its ID if there is no event with the specific ID there will be an error message displayed.

Example: `curl -X GET http://127.0.0.1:5000/events/1`

Response: 
```
{
    "description": "Meeting with John",
    "time": "2025-01-06T14:00:00",
    "id": 1
}
```

### 3. GET/events
This endpoint retrieves all events within a specified time range. You can provide optional datetime_format, from_time, and to_time query parameters.
If you don't specify the time it will retrieve the events that are between the start of that day and the current time of executing the command. 
If the `to time` of the requests is before than the `from time` an `error` will appear.
If there are no events on that time frame an empty list will show up.


Example: `curl "http://127.0.0.1:5000/events?from_time=2025-01-05T00:00:00&to_time=2025-01-07T00:00:00"`

Response: 
```
{
    "description": "Meeting with John",
    "time": "2025-01-06T14:00:00",
    "id": 1
}
```

### Query Parameters
- `datetime_format`: The format for parsing and displaying the `time` field. Default is `%Y-%m-%dT%H:%M:%S`.
- `from_time`: The start time of the date range (in the format specified by `datetime_format`).
- `to_time`: The end time of the date range (in the format specified by `datetime_format`).

### Troubleshooting
- Empty Reply from Server: This typically happens if the Flask app doesn't start correctly. Ensure the container is running and accessible via the correct port.
- Missing events file: If there is no `events.json` file, the service will create one automatically.
- Docker: 
  - check your docker container is running: `docker ps`
