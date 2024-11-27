import unittest
from unittest.mock import patch, MagicMock
from flask import session, redirect, flash
from app import app
import app.routes as routes
from app.recommendation import recommend_jobs

class TestJobRecommendations(unittest.TestCase):
    def setUp(self):
        # Configure the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.routes.intialize_db')
    @patch('app.routes.get_all_jobs')
    @patch('app.routes.recommend')  # Correct path for recommend_jobs
    @patch('app.routes.transform_jobs')
    def test_job_recommendations_logged_in(self, mock_transform_jobs, mock_recommend_jobs, mock_get_all_jobs, mock_initialize_db):
        """
        Test the /job_recommendations route when the user is logged in and recommendations are available.
        """
        # Mock the database initialization
        mock_initialize_db.return_value = None
        
        # Mock the return value of get_all_jobs with the provided data format
        mock_get_all_jobs.return_value = [
           {'id': 1, 'title': 'Job 1','rating': 4, 'recommendation': 2},
            {'id': 2, 'title': 'Job 2','rating': 4, 'recommendation': 2}
        ]
        
        # Mock the return value of recommend_jobs and transform_jobs
        mock_recommend_jobs.return_value = [
             {'id': 1, 'title': 'Job 1','rating': 4, 'recommendation': 2},
            {'id': 2, 'title': 'Job 2','rating': 4, 'recommendation': 1}
        ]
        mock_transform_jobs.return_value = [
            {'id': 1, 'title': 'Job 1','rating': 4, 'recommendation': 2},
            {'id': 2, 'title': 'Job 2','rating': 4, 'recommendation': 1}
        ]

        # Simulate a logged-in user
        with self.app as client:
            with client.session_transaction() as sess:
                sess['username'] = 'testuser'  # Simulate a logged-in user

            # Call the route
            response = client.get('/job_recommendations')
            mock_initialize_db.assert_called_once()  # Check if DB initialization was called
            #mock_get_all_jobs.assert_called_once()  # Check if get_all_jobs was called
            mock_recommend_jobs.assert_called_once_with(mock_get_all_jobs.return_value, 'testuser', 10)  # Check if recommend_jobs was called
            #mock_transform_jobs.assert_called_once_with(mock_recommend_jobs.return_value)  # Check if transform_jobs was called
            # Assertions
            #self.assertEqual(response.status_code, 200)  # Success expected
            #mock_initialize_db.assert_called_once()  # Check if DB initialization was called
            #mock_get_all_jobs.assert_called_once()  # Check if get_all_jobs was called
            #mock_recommend_jobs.assert_called_once_with(mock_get_all_jobs.return_value, 'testuser', 10)  # Check if recommend_jobs was called
            #mock_transform_jobs.assert_called_once_with(mock_recommend_jobs.return_value)  # Check if transform_jobs was called
    
    @patch('app.routes.intialize_db')
    @patch('app.routes.get_all_jobs')
    def test_job_recommndations_not_logged_in(self, mock_get_all_jobs, mock_initialize_db):
       
        # Mock the database initialization
        mock_initialize_db.return_value = None
        
        # Mock the return value of get_all_jobs with the provided data format
        mock_get_all_jobs.return_value = [
            {'title': 'Web Developer', 'company': 'Oracle', 'description': 'Good', 'locations': 'VA', 'department': 'Development', 'hourly_pay': '40', 'benefits': 'HI', 'review': 'Good', 'rating': '5', 'recommendation': '5', 'author': 'test', 'upvote': 0, 'id': 'Web Developer_Oracle_VA'}
        ]

        # Simulate no user logged in
        with self.app as client:
            with client.session_transaction() as sess:
                sess.pop('username', None)  # Ensure no user is logged in

            # Call the route
            response = client.get('/job_recommendations')
            
            # Assertions
            self.assertEqual(response.status_code, 302)  # Redirect expected (to login page)

    @patch('app.routes.intialize_db')
    @patch('app.routes.get_all_jobs')
    @patch('app.routes.recommend')  # Correct path for recommend_jobs
    @patch('app.routes.transform_jobs')
    def test_job_recommendations_no_recommendations(self, mock_transform_jobs, mock_recommend_jobs, mock_get_all_jobs, mock_initialize_db):
        
        # Mock the database initialization
        mock_initialize_db.return_value = None
        
        # Mock the return value of get_all_jobs with the provided data format
        mock_get_all_jobs.return_value = [
            {'title': 'Web Developer', 'company': 'Oracle', 'description': 'Good', 'locations': 'VA', 'department': 'Development', 'hourly_pay': '40', 'benefits': 'HI', 'review': 'Good', 'rating': '5', 'recommendation': '5', 'author': 'test', 'upvote': 0, 'id': 'Web Developer_Oracle_VA'}
        ]
        
        # Mock the return value of recommend_jobs to be empty
        mock_recommend_jobs.return_value = []
        mock_transform_jobs.return_value = []

        # Simulate a logged-in user
        with self.app as client:
            with client.session_transaction() as sess:
                sess['username'] = 'testuser'  # Simulate a logged-in user

            # Call the route
            response = client.get('/job_recommendations')
            
            # Assertions
            self.assertEqual(response.status_code, 200)  # Success expected
            mock_initialize_db.assert_called_once()  # Check if DB initialization was called
            mock_get_all_jobs.assert_called_once()  # Check if get_all_jobs was called
            mock_recommend_jobs.assert_called_once_with(mock_get_all_jobs.return_value, 'testuser', 10)  # Check if recommend_jobs was called

if __name__ == '__main__':
    unittest.main()
