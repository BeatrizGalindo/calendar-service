import unittest
import json
import os
from datetime import datetime

from app import load_events, save_events

EVENTS_FILE = 'events.json'


class TestEventStorage(unittest.TestCase):

    def setUp(self):
        """Reset the events file before each test."""
        if os.path.exists(EVENTS_FILE):
            os.remove(EVENTS_FILE)

    def test_save_and_load_events(self):
        events = [
            {"description": "Test Event 1", "time": "2025-01-01T00:00:00", "id": 1},
            {"description": "Test Event 2", "time": "2025-01-02T10:00:00", "id": 2}
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

    def tearDown(self):
        """Cleanup after each test."""
        if os.path.exists(EVENTS_FILE):
            os.remove(EVENTS_FILE)


if __name__ == '__main__':
    unittest.main()
