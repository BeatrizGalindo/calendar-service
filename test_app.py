import unittest
import json
import os

from app import app, load_events, save_events

EVENTS_FILE = 'events.json'


class TestEventStorage(unittest.TestCase):

    def setUp(self):
        """Reset the events file before each test."""
        if os.path.exists(EVENTS_FILE):
            os.remove(EVENTS_FILE)

        # Set up Flask test client
        self.client = app.test_client()

    def test_save_and_load_events(self):
        events = [
            {"description": "Test Event 1", "time": "2025-01-01T00:00:00", "id": 1},
            {"description": "Test Event 2", "time": "2025-01-02T10:00:00", "id": 2},
            {"description": "Test Event 3", "time": "2025-01-06T10:00:00", "id": 3}
        ]

        # Save events
        save_events(events)

        # Load events
        loaded_events = load_events()

        # Check if the events are correctly loaded
        self.assertEqual(loaded_events, events, "The loaded events do not match the saved events.")

    def test_load_empty_events(self):
        """Test loading events from an empty file."""
        # Ensure the file does not exist
        if os.path.exists(EVENTS_FILE):
            os.remove(EVENTS_FILE)

        loaded_events = load_events()

        # Assert that it loads as an empty list
        self.assertEqual(loaded_events, [], "Loaded events should be an empty list.")

    def test_save_event_with_missing_fields(self):
        """Test saving an event with missing required fields."""
        incomplete_event = {"description": "Test Event", "time": "2025-01-01T00:00:00"}

        # Simulate sending a request to add an event with missing 'id'
        response = self.client.post('/events', json=incomplete_event)

        # Check if the response status code is 400 (Bad Request) and contains the correct error message
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", response.json['error'])

    # def test_load_invalid_json(self):
    #     """Test loading events from a corrupted JSON file."""
    #     corrupted_json = "{description: 'Test Event', time: '2025-01-01T00:00:00', id: 1}"
    #     with open(EVENTS_FILE, 'w') as file:
    #         file.write(corrupted_json)
    #
    #     # Attempt to load corrupted events
    #     with self.assertRaises(json.JSONDecodeError):
    #         load_events()

    # def test_save_event_with_duplicate_id(self):
    #     """Test saving events with duplicate IDs."""
    #     #  log in here the current events
    #     events = [
    #         {"description": "Test Event 1", "time": "2025-01-01T00:00:00", "id": 1},
    #         {"description": "Test Event 2", "time": "2025-01-02T10:00:00", "id": 1}  # Duplicate ID
    #     ]
    #
    #     # Save events
    #     save_events(events)
    #
    #     # Load events
    #     loaded_events = load_events()
    #
    #     # Check if duplicate ID handling works correctly
    #     self.assertEqual(len(loaded_events), 4, "Duplicate events with the same ID should not be saved.")

    # def test_save_empty_event_list(self):
    #     """Test saving an empty list of events."""
    #     # Save empty list
    #     save_events([])
    #
    #     # Load events
    #     loaded_events = load_events()
    #
    #     # Assert that the list is empty
    #     self.assertEqual(loaded_events, [], "Loaded events should be an empty list.")

    def tearDown(self):
        """Cleanup after each test."""
        if os.path.exists(EVENTS_FILE):
            os.remove(EVENTS_FILE)


if __name__ == '__main__':
    unittest.main()
