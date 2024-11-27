import unittest
from unittest.mock import patch, MagicMock

from app import app
from app.routes import get_job_by_id
import app.routes as routes
class TestGetJobById(unittest.TestCase):
    def setUp(self):
        # Configure the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.routes.process_jobs')  # Mock the process_jobs function
    @patch('app.routes.JOBS_DB')  # Mock the JOBS_DB object
    def test_get_job_by_id(self, mock_jobs_db, mock_process_jobs):
        # Mock the `find` method of JOBS_DB
        mock_jobs_db.find.return_value = [
            {"_id": "123", "title": "Software Engineer"},
            {"_id": "123", "title": "Backend Developer"}
        ]
        
        # Mock the process_jobs function
        mock_process_jobs.return_value = [
            {"id": "123", "title": "Software Engineer"},
            {"id": "123", "title": "Backend Developer"}
        ]

        # Call the function under test
        job_id = "123"
        result = get_job_by_id(job_id)

        # Assertions
        mock_jobs_db.find.assert_called_once_with({"_id": job_id})  # Ensure find was called with correct parameters
        mock_process_jobs.assert_called_once_with(list(mock_jobs_db.find.return_value))  # Ensure process_jobs was called with correct data
        self.assertEqual(result, mock_process_jobs.return_value)  # Check the function's return value
    
    @patch('app.routes.intialize_db')
    @patch('app.routes.get_all_jobs')
    def test_review_not_logged_in(self, mock_get_all_jobs, mock_initialize_db):
        """Test the /review route when the user is not logged in."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.pop('username', None)  # Ensure no user is logged in
            
            response = client.get('/review')
            
            self.assertEqual(response.status_code, 302)  # Redirect expected

    @patch('app.routes.intialize_db')
    @patch('app.routes.get_all_jobs')
    def test_review_all_jobs(self, mock_get_all_jobs, mock_initialize_db):
        """Test the /review route when all jobs are fetched."""
        mock_initialize_db.return_value = None  # Mock DB initialization
        mock_get_all_jobs.return_value = [
            {'id': 1, 'title': 'Job 1'},
            {'id': 2, 'title': 'Job 2'}
        ]  # Mock job data
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['username'] = 'testuser'  # Simulate logged-in user

            response = client.get('/review')
            
            self.assertEqual(response.status_code, 200)  # Success expected
            self.assertIn(b'Job 1', response.data)  # Job 1 should be in response
            self.assertIn(b'Job 2', response.data)  # Job 2 should be in response

    @patch('app.routes.intialize_db')
    @patch('app.routes.get_job_by_id')
    def test_review_specific_jobs(self, mock_get_job_by_id, mock_initialize_db):
        """Test the /review route with specific job IDs provided."""
        mock_initialize_db.return_value = None  # Mock DB initialization
        mock_get_job_by_id.side_effect = lambda job_id: [{'id': int(job_id), 'title': f'Job {job_id}'}]

        with self.app as client:
            with client.session_transaction() as sess:
                sess['username'] = 'testuser'  # Simulate logged-in user

            response = client.get('/review?review_id=1,2')
            
            self.assertEqual(response.status_code, 200)  # Success expected
            self.assertIn(b'Job 1', response.data)  # Job 1 should be in response
            self.assertIn(b'Job 2', response.data)  # Job 2 should be in response

    @patch('app.routes.intialize_db')
    def test_review_invalid_session(self, mock_initialize_db):
        """Test the /review route with an invalid session."""
        mock_initialize_db.return_value = None  # Mock DB initialization

        with self.app as client:
            response = client.get('/review')
            
            self.assertEqual(response.status_code, 302)  # Redirect expected

if __name__ == '__main__':
    unittest.main()