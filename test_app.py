import unittest
import os
from app import app, load_events, save_events
import logging

EVENTS_FILE = 'events.json'


class TestEventStorage(unittest.TestCase):
    TEST_EVENTS = [
        {"description": "Test Event 1", "time": "2025-01-01T00:00:00", "id": 1},
        {"description": "Test Event 2", "time": "2025-01-02T10:00:00", "id": 2},
        {"description": "Test Event 3", "time": "2025-01-06T10:00:00", "id": 3},
    ]

    def setUp(self):
        """Reset the events file and set up the test client."""
        if os.path.exists(EVENTS_FILE):
            os.remove(EVENTS_FILE)
        self.client = app.test_client()

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(EVENTS_FILE):
            os.remove(EVENTS_FILE)

    def test_save_and_load_events(self):
        """Test saving and loading events."""
        save_events(self.TEST_EVENTS)
        loaded_events = load_events()
        self.assertEqual(loaded_events, self.TEST_EVENTS, "Loaded events do not match saved events.")

    def test_load_empty_events(self):
        """Test loading events when no file exists."""
        if os.path.exists(EVENTS_FILE):
            os.remove(EVENTS_FILE)
        loaded_events = load_events()
        self.assertEqual(loaded_events, [], "Loaded events should be an empty list when no file exists.")

    def test_add_event_success(self):
        """Test adding a valid event."""
        event = {"description": "New Event", "time": "2025-01-10T15:00:00", "id": 4}
        response = self.client.post('/events', json=event)
        self.assertEqual(response.status_code, 201, "Adding a valid event should return a 201 status.")
        self.assertEqual(response.json, event, "Response should match the added event.")

    def test_add_event_missing_fields(self):
        """Test adding an event with missing required fields."""
        incomplete_event = {"description": "Incomplete Event", "time": "2025-01-01T00:00:00"}
        response = self.client.post('/events', json=incomplete_event)
        self.assertEqual(response.status_code, 400, "Missing fields should result in a 400 status.")
        self.assertIn("Missing required fields", response.json['error'], "Error message should indicate missing fields.")

    def test_get_event_not_found(self):
        """Test retrieving a non-existent event."""
        response = self.client.get('/events/999')
        self.assertEqual(response.status_code, 404, "Non-existent event should return a 404 status.")
        self.assertIn("not found", response.json['error'], "Error message should indicate event not found.")

if __name__ == '__main__':
    unittest.main()
