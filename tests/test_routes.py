import unittest
from unittest.mock import patch, MagicMock
from flask import session, jsonify
from app import app
from pymongo.errors import PyMongoError

class TestGetUser(unittest.TestCase):
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_user_with_username(self):
        """Test retrieving the username from the session when available."""
        with self.app.session_transaction() as sess:
            sess['username'] = 'testuser'

        response = self.app.get('/api/getUser')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), 'testuser')


if __name__ == '__main__':
    unittest.main()