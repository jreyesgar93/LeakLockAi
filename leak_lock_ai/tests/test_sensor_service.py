
import sys
import os
import unittest
import fastapi
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from leak_lock_ai.services import sensors_service

class TestSensorsService(unittest.TestCase):

    def test_get_latest_data_for_all_sensors(self):
        # Mock data or set up necessary preconditions
        result = sensors_service.get_latest_data_for_all_sensors()
        # Assertions to verify the expected outcome
        self.assertIsInstance(result, dict)
        self.assertIn('data', result)
        self.assertIn('last_available_date', result)

if __name__ == '__main__':
    unittest.main()
