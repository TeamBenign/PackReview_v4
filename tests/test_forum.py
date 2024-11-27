import unittest
from unittest.mock import patch, MagicMock
from app import app
from app.routes import intialize_db, set_test
from bson import ObjectId
import json

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
    def test_add_comment_forum(self):
        """Test adding a comment to a forum topic."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        data = {
            'topicId': '674601b9b7f9ec52b94d45e7',
            'content': 'very helpful'
        }

        # Mock the update_one and find_one methods
        self.mock_forum_db.update_one.return_value = None
        self.mock_forum_db.find_one.return_value = {
            '_id': ObjectId('674601b9b7f9ec52b94d45e7'),
            'comments': [{
                '_cid': str(ObjectId()),
                'commenter': 'testuser',
                'content': 'very helpful',
                'likes': [],
                'dislikes': [],
                'timestamp': '2021-10-01 12:00:00'
            }]
        }

        response = self.client.post('/forum/add_comment', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data']['content'], 'very helpful')
    
    def test_update_reaction(self):
        """Test updating a reaction to a forum topic or comment."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        data = {
            'topicId': '674601b9b7f9ec52b94d45e7',
            'commentId': '674601b9b7f9ec52b94d45e8',
            'discussionType': 'topic',
            'reactionType': 'like'
        }

        # Mock the find_one and update_one methods
        self.mock_forum_db.find_one.return_value = {
            '_id': ObjectId('674601b9b7f9ec52b94d45e7'),
            'likes': [],
            'dislikes': [],
            'comments': [{
                '_cid': '674601b9b7f9ec52b94d45e8',
                'commenter': 'testuser',
                'content': 'very helpful',
                'likes': [],
                'dislikes': [],
                'timestamp': '2021-10-01 12:00:00'
            }]
        }
        self.mock_forum_db.update_one.return_value = None

        # Mock the find_one method for USERS_DB
        self.mock_users_db.find_one.return_value = {
            'username': 'testuser',
            'reviews': ['review1', 'review2', 'review3', 'review4', 'review5']
        }

        response = self.client.post('/forum/update_reaction', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data'], 0) 
    
def __main__():
    unittest.main()