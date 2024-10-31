import unittest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from app import app
from app.routes import db, intializeDB, setTest

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        """Set up test client and mock database."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        setTest(True)
        # Initialize mock database
        self.mock_db = patch('app.db', MagicMock()).start()
        intializeDB()  # Initialize DB with mock

        self.mock_usersDb = self.mock_db.Users
        self.mock_jobsDb = self.mock_db.Jobs
        self.mock_forumDb = self.mock_db.Forum

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

    def tearDown(self):
        """Tear down test case, stop all patches."""
        setTest(False)
        patch.stopall()

    def test_home_page(self):
        """Test home page access."""
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Home", response.data)

    def test_login_post_valid_user(self):
        """Test login with valid user credentials."""
        with self.client.session_transaction() as session:
            session['username'] = None

        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')

    def test_login_post_invalid_user(self):
        """Test login with invalid credentials."""
        response = self.client.post('/login', data={
            'username': 'fakeuser',
            'password': 'fakepass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You should be redirected automatically to the target URL:', response.data)

    def test_signup_post_existing_user(self):
        """Test signup with an existing username."""
        response = self.client.post('/signup', data={
            'username': 'existinguser',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username already exists', response.data)

    def test_add_job_review(self):
        """Test adding a job review."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        review_data = {
            'job_title': 'Software Engineer',
            'company': 'Tech Corp',
            'job_description': 'Development role',
            'locations': 'NYC',
            'department': 'Engineering',
            'hourly_pay': '30',
            'benefits': 'Health, Dental',
            'review': 'Great experience',
            'rating': '5',
            'recommendation': '1'
        }
        
        response = self.client.post('/add', data=review_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')

    def test_view_job_review(self):
        """Test viewing a job review."""
        job_id = 'Software Engineer_Tech Corp_NYC'

        response = self.client.get(f'/view/{job_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Software Engineer', response.data)

    def test_upvote_review(self):
        """Test upvoting a job review."""
        job_id = 'Software Engineer_Tech Corp_NYC'

        response = self.client.get(f'/upvote/{job_id}')
        self.assertEqual(response.status_code, 302)

    def test_pagination(self):
        """Test pagination on pageContent."""
        response = self.client.get('/pageContent?page=1&per_page=10')
        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):
        """Test deleting a job review."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        review_data = {
            'job_title': 'Software Engineer',
            'company': 'Tech Corp',
            'job_description': 'Development role',
            'locations': 'NYC1',
            'department': 'Engineering',
            'hourly_pay': '30',
            'benefits': 'Health, Dental',
            'review': 'Great experience',
            'rating': '5',
            'recommendation': '1'
        }
        
        response = self.client.post('/add', data=review_data)
        job_id = 'Software Engineer_Tech Corp_NYC1'

        response = self.client.get(f'/delete/{job_id}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/myjobs')

    def test_signup_post_successful(self):
        """Test signup with a new username."""
        response = self.client.post('/signup', data={
            'username': 'newuser',
            'password': 'newpass',
            'confirm_password': 'newpass'
        })
        self.assertEqual(response.status_code, 200)

    def test_add_job_review_without_login(self):
        """Test adding a job review without being logged in."""
        review_data = {
            'job_title': 'Software Engineer',
            'company': 'Tech Corp',
            'job_description': 'Development role',
            'locations': 'NYC',
            'department': 'Engineering',
            'hourly_pay': '30',
            'benefits': 'Health, Dental',
            'review': 'Great experience',
            'rating': '5',
            'recommendation': '1'
        }
        with self.assertRaises(KeyError):
            response = self.client.post('/add', data=review_data)

    def test_invalid_add_job_review(self):
        """Test adding a job review with missing fields."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        with self.assertRaises(TypeError):    
            response = self.client.post('/add', data={'job_title': ''})  # Missing other fields

    def test_view_job_review_nonexistent(self):
        """Test viewing a nonexistent job review."""
        job_id = 'Nonexistent Job'
        with self.assertRaises(AttributeError):
            response = self.client.get(f'/view/{job_id}')

    def test_add_review_redirects_after_success(self):
        """Test redirect after adding a review."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        review_data = {
            'job_title': 'Software Engineer',
            'company': 'Tech Corp',
            'job_description': 'Development role',
            'locations': 'NYC',
            'department': 'Engineering',
            'hourly_pay': '30',
            'benefits': 'Health, Dental',
            'review': 'Great experience',
            'rating': '5',
            'recommendation': '1'
        }
        response = self.client.post('/add', data=review_data)
        self.assertEqual(response.status_code, 302)

    def test_upvote_review_already_upvoted(self):
        """Test upvoting a review that is already upvoted."""
        job_id = 'Software Engineer_Tech Corp_NYC'
        # Simulate that the user has already upvoted
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        response = self.client.get(f'/upvote/{job_id}')
        self.assertEqual(response.status_code, 302)

    def test_downvote_review(self):
        """Test downvoting a job review."""
        job_id = 'Software Engineer_Tech Corp_NYC'
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        response = self.client.get(f'/downvote/{job_id}')
        self.assertEqual(response.status_code, 302)

    def test_delete_review_without_login(self):
        """Test deleting a job review without being logged in."""
        job_id = 'Software Engineer_Tech Corp_NYC'
        with self.assertRaises(KeyError):
            response = self.client.get(f'/delete/{job_id}')

    def test_delete_nonexistent_review(self):
        """Test deleting a nonexistent job review."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        job_id = 'Nonexistent Job'
        with self.assertRaises(ValueError):
            response = self.client.get(f'/delete/{job_id}')

    def test_pagination_bounds(self):
        """Test pagination with a page number that exceeds available pages."""
        response = self.client.get('/pageContent?page=999&per_page=10')
        self.assertEqual(response.status_code, 200)  # Assuming you handle this case

    def test_edit_review(self):
        """Test editing a job review."""
        job_id = 'Software Engineer_Tech Corp_NYC'
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        edit_data = {
            'review': 'Updated review',
            'rating': '4'
        }
        response = self.client.post(f'/edit/{job_id}', data=edit_data)
        self.assertEqual(response.status_code, 404)

    def test_login_empty_fields(self):
        """Test login with empty username or password fields."""
        response = self.client.post('/login', data={'username': '', 'password': ''}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password.', response.data) 

    def test_access_restricted_route_without_login(self):
        """Test that restricted routes require authentication."""
        response = self.client.get('/myjobs')
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)  # 302 for redirect
        self.assertIn('/login', response.location)  # Ensure
    
    def test_access_restricted_new_topic_route_without_login(self):
        """Test that creating a new topic requires authentication."""
        response = self.client.get('/forum/new')
        self.assertEqual(response.status_code, 302)  
        self.assertIn('/login', response.headers['Location'])

    def test_forum_page_access_without_login(self):
        """Test that accessing the forum page is allowed without login."""
        response = self.client.get('/forum')
        self.assertEqual(response.status_code, 200)  
        
        self.assertIn(b'Discussion Forum', response.data) 

    def test_logout(self):
        """Test logout functionality."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(response.location, '/')  


if __name__ == "__main__":
    unittest.main()
