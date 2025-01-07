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
- Flask
- `requirements.txt` dependencies

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd calendar-service
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Docker

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
This will start the container and map port 5000 from the container to 5001 on your host machine. You can access the service at http://localhost:5001.

### 4. Run the application locally (without Docker)

```
python3 app.py
```


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
`curl -X POST http://localhost:5001/events -H "Content-Type: application/json" -d '{"description": "Meeting with John", "time": "2024-01-15T14:00:00", "id": 1}'`

Response: 
```
{
    "description": "Meeting with John",
    "time": "2024-01-15T14:00:00",
    "id": 1
}
```

### 2. GET/events/<ID>
This endpoint retrieves an event by its ID. 

Example: `curl "http://localhost:5001/events/1"

`

Response: 
```
{
    "description": "Meeting with John",
    "time": "2024-01-15T14:00:00",
    "id": 1
}
```

### 3. GET/events
This endpoint retrieves all events within a specified time range. You can provide optional datetime_format, from_time, and to_time query parameters.
If you don't specify the time it will retrieve the events that are between the start of that day and the current time of executing the command. 

Example: `curl "http://localhost:5001/events?datetime_format=%Y-%m-%d&from_time=2024-01-01T00:00:00&to_time=2024-12-31T23:59:59"`

Response: 
```
{
    "description": "Meeting with John",
    "time": "2024-01-15T14:00:00",
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
