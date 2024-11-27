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

import unittest
from unittest.mock import patch, MagicMock
from flask import session
from app import app

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
        with self.app.session_transaction() as sess:
            self.assertEqual(sess['username'], 'newuser')

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

class TestLogin(unittest.TestCase):
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.routes.USERS_DB.find_one')
    @patch('app.routes.bcrypt.checkpw')
    def test_login_success(self, mock_checkpw, mock_find_one):
        """Test successful login."""
        mock_find_one.return_value = {'username': 'testuser', 'password': b'hashed_password'}
        mock_checkpw.return_value = True

        response = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')
        mock_find_one.assert_called_once_with({"username": 'testuser'})
        mock_checkpw.assert_called_once_with(b'password123', b'hashed_password')
        with self.app.session_transaction() as sess:
            self.assertEqual(sess['username'], 'testuser')

    @patch('app.routes.USERS_DB.find_one')
    @patch('app.routes.bcrypt.checkpw')
    def test_login_invalid_credentials(self, mock_checkpw, mock_find_one):
        """Test login with invalid username or password."""
        mock_find_one.return_value = {'username': 'testuser', 'password': b'hashed_password'}
        mock_checkpw.return_value = False

        response = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/login')
        # self.assertIn(b'Invalid username or password.', response.data)
        mock_find_one.assert_called_once_with({"username": 'testuser'})
        mock_checkpw.assert_called_once_with(b'wrongpassword', b'hashed_password')

    def test_login_user_already_logged_in(self):
        """Test login when user is already logged in."""
        with self.app.session_transaction() as sess:
            sess['username'] = 'loggedinuser'

        response = self.app.get('/login')
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

class TestAddComment(unittest.TestCase):
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_add_comment_not_logged_in(self):
        """Test adding a comment when the user is not logged in."""
        response = self.app.post('/forum/add_comment', json={
            'topicId': '674601b9b7f9ec52b94d45e7',
            'content': 'This is a test comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/login')

    def test_add_vote_not_logged_in(self):
        """Test adding a vote when the user is not logged in."""
        response = self.app.post('/forum/674601b9b7f9ec52b94d45e7/upvote_post', json={
            'topicId': '674601b9b7f9ec52b94d45e7',
            'content': 'This is a test comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/login')

    def test_down_vote_not_logged_in(self):
        """Test adding a vote when the user is not logged in."""
        response = self.app.post('/forum/674601b9b7f9ec52b94d45e7/downvote_post', json={
            'topicId': '674601b9b7f9ec52b94d45e7',
            'content': 'This is a test comment'
        })
        # response2 = self.app.post('/forum/674601b9b7f9ec52b94d45e7', json={
        #     'topicId': '674601b9b7f9ec52b94d45e7',
        #     'content': 'This is a test comment'
        # })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/login')

    @patch('app.routes.FORUM_DB.update_one')
    @patch('app.routes.FORUM_DB.find_one')
    def test_add_comment_exception(self, mock_find_one, mock_update_one):
        """Test adding a comment when an exception occurs."""
        with self.app.session_transaction() as sess:
            sess['username'] = 'testuser'

        mock_update_one.side_effect = PyMongoError("Database error")

        response = self.app.post('/forum/add_comment', json={
            'topicId': '674601b9b7f9ec52b94d45e7',
            'content': 'This is a test comment'
        })
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Database error')
class TestPageContentPost(unittest.TestCase):
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.routes.get_all_jobs')
    @patch('app.routes.process_jobs')
    @patch('app.routes.JOBS_DB.find')
    @patch('app.routes.JOBS_DB.distinct')
    @patch('app.routes.get_page_args')
    def test_page_content_post_pagination(self, mock_get_page_args, mock_distinct, mock_find, mock_process_jobs, mock_get_all_jobs):
        """Test the pagination condition in page_content_post."""
        mock_get_page_args.return_value = (1, 10, 0)
        mock_get_all_jobs.return_value = [{'title': 'Job1', 'company': 'Company1', 'locations': 'Location1', 'department': 'Dept1'}]
        mock_distinct.side_effect = [['Dept1'], ['Location1'], ['Company1']]
        mock_find.return_value = [{'title': 'Job1', 'company': 'Company1', 'locations': 'Location1', 'department': 'Dept1'}]
        mock_process_jobs.return_value = [{'title': 'Job1', 'company': 'Company1', 'locations': 'Location1', 'department': 'Dept1'}]

        response = self.app.post('/pageContentPost', data={
            'search': '',
            'dept_filter': '',
            'company_filter': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Job1', response.data)
        self.assertIn(b'Company1', response.data)
        self.assertIn(b'Location1', response.data)
        self.assertIn(b'Dept1', response.data)

    def test_page_content_post_jsonify(self):
        """Test the return jsonify condition in page_content_post."""
        response = self.app.get('/pageContentPost')
        self.assertEqual(response.get_json(), None)

if __name__ == '__main__':
    unittest.main()