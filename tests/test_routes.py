import unittest
from unittest.mock import patch, MagicMock
from flask import session, jsonify
from app import app
from pymongo.errors import PyMongoError

class TestSignup(unittest.TestCase):
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.routes.USERS_DB.find_one')
    @patch('app.routes.USERS_DB.insert_one')
    @patch('app.routes.bcrypt.hashpw')
    def test_signup_success(self, mock_hashpw, mock_insert_one, mock_find_one):
        """Test successful signup."""
        mock_find_one.return_value = None
        mock_hashpw.return_value = b'hashed_password'

        response = self.app.post('/signup', data={
            'username': 'newuser',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')
        mock_find_one.assert_called_once_with({"username": 'newuser'})
        mock_insert_one.assert_called_once()

    @patch('app.routes.USERS_DB.find_one')
    def test_signup_passwords_not_matching(self, mock_find_one):
        """Test signup with passwords not matching."""
        mock_find_one.return_value = None

        response = self.app.post('/signup', data={
            'username': 'newuser',
            'password': 'password123',
            'confirm_password': 'password456'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Passwords do not match!', response.data)
        mock_find_one.assert_not_called()
    @patch('app.routes.USERS_DB.find_one')
    def test_signup_username_exists(self, mock_find_one):
        """Test signup with username already existing."""
        mock_find_one.return_value = {'username': 'existinguser'}

        response = self.app.post('/signup', data={
            'username': 'existinguser',
            'password': 'password123',
            'confirm_password': 'password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already exists! Please login or use a different username.', response.data)
        mock_find_one.assert_called_once_with({"username": 'existinguser'})

    def test_signup_user_already_logged_in(self):
        """Test signup when user is already logged in."""
        with self.app.session_transaction() as sess:
            sess['username'] = 'loggedinuser'

        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')
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