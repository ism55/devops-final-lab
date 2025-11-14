"""
Comprehensive tests for the Flask application with coverage analysis
"""
import unittest
import json
from app.app import app

class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application"""

    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        """Test main endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Notes API is running!')

if __name__ == '__main__':
    unittest.main()
