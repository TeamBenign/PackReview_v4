import unittest
from unittest.mock import patch, MagicMock
from app import app
from app.routes import intialize_db, set_test
from bson import ObjectId

class TestForum(unittest.TestCase):
    def setUp(self):
        """Set up test client and mock database."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        # Mock the get_db function to return a mocked database
        self.mock_get_db = patch('app.routes.get_db').start()
        # Create a mock database and mock collections
        self.mock_db = MagicMock()
        self.mock_jobs_db = MagicMock()
        self.mock_users_db = MagicMock()
        self.mock_forum_db = MagicMock()

        # Set up the mock collections
        self.mock_db.Users = self.mock_users_db
        self.mock_db.Jobs = self.mock_jobs_db
        self.mock_db.Forum = self.mock_forum_db

        # Set the return value of get_db to the mocked database
        self.mock_get_db.return_value = self.mock_db
        intialize_db()  # Initialize DB with mock

        # Signup two users for testing
        self.client.post('/signup', data={
            'username': 'testuser',
            'password': 'testpass',
            'confirm_password': 'testpass'
        })
        self.client.post('/signup', data={
            'username': 'existinguser',
            'password': 'password123',
            'confirm_password': 'password123'
        })
    #test case for add_forum method
    def test_view_topic_forum(self):
        """Test view a forum."""
        self.setUp()
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        data = {
            'comment': 'very helpful',
            'username': session['username']
        }

        response = self.client.post('/forum/674601b9b7f9ec52b94d45e7', data=data)
        self.assertEqual(response.status_code, 302)

def __main__():
    unittest.main()