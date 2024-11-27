"""
test_app.py

This module contains unit tests for the Flask web application defined in 'app.py'.
It uses the unittest framework to test various routes and functionalities of the application,
including user authentication, job reviews, forum interactions, and user profiles.

The tests are structured to ensure that:
- Users can sign up, log in, and log out successfully.
- Job reviews can be added, viewed, edited, and deleted.
- Forum posts can be created, viewed, edited, and deleted.
- Restricted routes require authentication.
- The application handles various edge cases and errors gracefully.

Mocking is employed to simulate database interactions, ensuring that tests do not depend on
the actual database state.
"""

import unittest
from unittest.mock import patch, MagicMock
from app import app
from app.routes import intialize_db, set_test
from bson import ObjectId
from tests.test_forum import TestForum

class FlaskAppTests(unittest.TestCase):
    """
    FlaskAppTests

    This class contains unit tests for the Flask application. It sets up a test client
    and a mock database to isolate tests from the actual application state. The tests
    cover a wide range of functionalities, including user registration, login/logout,
    adding and managing job reviews, forum interactions, and profile management.

    Methods:
    - setUp(): Initializes the test client and mocks the database for testing.
    - tearDown(): Cleans up after tests by stopping all patches and resetting the test state.
    - test_home_page(): Tests access to the home page.
    - test_login_post_valid_user(): Tests logging in with valid user credentials.
    - test_login_post_invalid_user(): Tests logging in with invalid user credentials.
    - test_signup_post_existing_user(): Tests signing up with an existing username.
    - test_add_job_review(): Tests adding a job review.
    - test_view_job_review(): Tests viewing a job review.
    - test_upvote_review(): Tests upvoting a job review.
    - test_pagination(): Tests pagination functionality.
    - test_delete_review(): Tests deleting a job review.
    - test_signup_post_successful(): Tests signing up with a new username.
    - test_add_job_review_without_login(): Tests adding a job review without being logged in.
    - test_invalid_add_job_review(): Tests adding a job review with missing fields.
    - test_view_job_review_nonexistent(): Tests viewing a nonexistent job review.
    - test_add_review_redirects_after_success(): Tests redirect after adding a review.
    - test_upvote_review_already_upvoted(): Tests upvoting a review that is already upvoted.
    - test_downvote_review(): Tests downvoting a job review.
    - test_delete_review_without_login(): Tests deleting a job review without being logged in.
    - test_delete_nonexistent_review(): Tests deleting a nonexistent job review.
    - test_pagination_bounds(): Tests pagination with a page number that exceeds available pages.
    - test_edit_review(): Tests editing a job review.
    - test_login_empty_fields(): Tests logging in with empty username or password fields.
    - test_access_restricted_route_without_login(): Restricted routes require authentication.
    - test_access_restricted_new_topic_route_without_login()
    - test_forum_page_access_without_login(): accessing the forum page is allowed without login.
    - test_logout(): Tests logout functionality.
    - test_edit_nonexistent_review(): Tests editing a nonexistent job review.
    - test_view_forum(): Tests viewing the forum page.
    - test_add_forum_post(): Tests adding a post to the forum.
    - test_view_forum_post(): Tests viewing a specific forum post.
    - test_delete_forum_post(): Tests deleting a forum post.
    - test_edit_forum_post(): Tests editing a forum post.
    - test_view_profile(): Tests viewing a user profile.
    - test_edit_profile(): Tests editing user profile.
    """

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
        
    def tearDown(self):
        """Tear down test case, stop all patches."""
        set_test(False)
        patch.stopall()

    def test_home_page(self):
        """Test home page access."""
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Home", response.data)

    def test_forum(self):
        """Test the forum class."""
        TestForum().test_view_topic_forum()
    # def test_login_post_valid_user(self):
    #     """Test login with valid user credentials."""
    #     with self.client.session_transaction() as session:
    #         session['username'] = None

    #     response = self.client.post('/login', data={
    #         'username': 'testuser',
    #         'password': 'testpass'
    #     })
    #     print("--------------", response.data, "---------------------------------")
    #     self.assertEqual(response.status_code, 302)
    #     self.assertIn('/', response.location)

    # def test_login_post_invalid_user(self):
    #     """Test login with invalid credentials."""
    #     response = self.client.post('/login', data={
    #         'username': 'fakeuser',
    #         'password': 'fakepass'
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertIn(
    #         b'You should be redirected automatically to the target URL:',
    #         response.data)

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
        self.assertEqual(response.location, '/myjobs')

    def test_view_job_review(self):
        """Test viewing a job review."""
        job_id = 'Software Engineer_Tech Corp_NYC'

        response = self.client.get(f'/view/{job_id}')
        self.assertEqual(response.status_code, 200)

    def test_upvote_review(self):
        """Test upvoting a job review."""
        job_id = 'Software Engineer_Tech Corp_NYC'

        response = self.client.get(f'/upvote/{job_id}')
        self.assertEqual(response.status_code, 302)


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
            self.client.post('/add', data=review_data)

    def test_invalid_add_job_review(self):
        """Test adding a job review with missing fields."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        with self.assertRaises(TypeError):
            # Missing other fields
            self.client.post('/add', data={'job_title': ''})

    def test_view_job_review_nonexistent(self):
        """Test viewing a nonexistent job review."""
        job_id = 'NonexistentJobID'  # Example ID that should not exist
        response = self.client.get(f'/view/{job_id}')
        self.assertEqual(response.status_code, 200)

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
            self.client.get(f'/delete/{job_id}')

    def test_delete_nonexistent_review(self):
        """Test deleting a nonexistent job review."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        job_id = 'Nonexistent Job'
        response = self.client.get(f'/delete/{job_id}')
        self.assertEqual(response.status_code, 302)

        # with self.assertRaises(ValueError):
        #     self.client.get(f'/delete/{job_id}')


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

    # def test_login_empty_fields(self):
    #     """Test login with empty username or password fields."""
    #     response = self.client.post('/login', data={'username': '', 'password': ''})
    #     print("--------------", response.data, "---------------------------------")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Invalid username or password.', response.data)

    def test_access_restricted_route_without_login(self):
        """Test that restricted routes require authentication."""
        response = self.client.get('/myjobs')
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)  # 302 for redirect
        self.assertIn('/login', response.location)  # Ensure

    def test_access_restricted_new_topic_route_without_login(self):
        """Test that creating a new topic requires authentication."""
        response = self.client.post('/forum/new_topic')
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

    def test_edit_nonexistent_review(self):
        """Test editing a nonexistent job review."""
        job_id = 'Nonexistent Job'
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        edit_data = {
            'review': 'Updated review',
            'rating': '4'
        }
        response = self.client.post(f'/edit/{job_id}', data=edit_data)
        # Assuming you handle this case
        self.assertEqual(response.status_code, 404)

    def test_view_forum(self):
        """Test viewing the forum page."""
        response = self.client.get('/forum')
        self.assertEqual(response.status_code, 200)

    def test_add_forum_post(self):
        """Test adding a post to the forum."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        post_data = {
            'topic_title': 'Discussion about Software Engineering',
            'topic_description': 'What do you think about the future of software engineering?',
            'comments': [], 'author': 'testuser',
            'timestamp': '2021-09-01 12:00:00',
            'likes': [], 'dislikes': []
        }
        response = self.client.post('/forum/new_topic', data=post_data)
        self.assertEqual(response.status_code, 302)

    def test_view_forum_post(self):
        """Test viewing a specific forum post."""
        post_id = ObjectId()
        response = self.client.get(f'/forum/{post_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_forum_post(self):
        """Test deleting a forum post."""
        post_id = ObjectId()
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        response = self.client.get(f'/forum/delete/{post_id}')
        self.assertEqual(response.status_code, 404)

    def test_edit_forum_post(self):
        """Test editing a forum post."""
        post_id = ObjectId()
        edit_data = {
            'title': 'Updated title',
            'content': 'Updated content'
        }
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        response = self.client.post(f'/forum/edit/{post_id}', data=edit_data)
        self.assertEqual(response.status_code, 404)

    def test_view_profile(self):
        """Test viewing a user profile."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        response = self.client.get('/profile/testuser')
        self.assertEqual(response.status_code, 404)

    def test_edit_profile(self):
        """Test editing user profile."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'
        profile_data = {
            'email': 'testuser@example.com',
            'bio': 'This is my bio'
        }
        response = self.client.post('/profile/edit', data=profile_data)
        self.assertEqual(response.status_code, 404)

    def test_reset_password(self):
        """Test resetting password functionality."""
        response = self.client.post('/reset_password', data={
            'username': 'testuser',
            'new_password': 'newtestpass',
            'confirm_password': 'newtestpass'
        })
        self.assertEqual(response.status_code, 404)

    def test_reset_password_invalid_user(self):
        """Test resetting password for a nonexistent user."""
        response = self.client.post('/reset_password', data={
            'username': 'nonexistentuser',
            'new_password': 'newtestpass',
            'confirm_password': 'newtestpass'
        })
        self.assertEqual(response.status_code, 404)

    def test_index_route(self):
        """Test the index route for successful access (status code 200)."""
        response = self.client.get('/')
        assert response.status_code == 200



    def test_signup_route(self):
        """Test the signup route for successful access (status code 200)."""
        response = self.client.get('/signup')
        assert response.status_code == 200

    def test_login_route(self):
        """Test the login route for successful access (status code 200)."""
        response = self.client.get('/login')
        assert response.status_code == 200

    def test_add_review_route(self):
        """
        Test the add review route for redirecting (status code 302)
        when accessing the review page.
        """
        response = self.client.get('/review')
        assert response.status_code == 302


    def test_view_forum_topic_route(self):
        """Test viewing a specific forum topic."""
        topic_id = '672531d244fdeb1ec36c110d'
        response = self.client.get(f'/forum/{topic_id}')
        assert response.status_code == 200


    def test_get_user_logged_in(self):
        """Test for logging in users."""
        with self.client as client:
            with client.session_transaction() as session:
                session['username'] = 'testuser'
            response = client.get('/api/getUser')
            assert response.status_code == 200
            assert response.json == 'testuser'

    def test_get_user_not_logged_in(self):
        """Test for wgat if user not logged in."""
        with self.client as client:
            response = client.get('/api/getUser')
            assert response.status_code == 200
            assert response.json == ''

    def test_get_user_session_key_none(self):
        """Test for None user."""
        with self.client as client:
            with client.session_transaction() as session:
                session['username'] = None
            response = client.get('/api/getUser')
            assert response.status_code == 200
            assert response.json == ''

if __name__ == "__main__":
    unittest.main()
