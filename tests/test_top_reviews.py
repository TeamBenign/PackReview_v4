import unittest
from unittest.mock import patch
from app import app
from app.routes import process_jobs, get_all_users


class TestTopJobsRoute(unittest.TestCase):
    def setUp(self):
        # Configure the Flask test client
        self.app = app.test_client()
        self.app.testing = True
        
    @patch('app.routes.get_all_jobs')  # Mock the `get_all_jobs` function
    @patch('app.routes.intialize_db')  # Mock the database initialization
    def test_top_jobs_functions_called(self, mock_initialize_db, mock_get_all_jobs):
        # Mock database initialization
        mock_initialize_db.return_value = None

        # Mock job data to simulate the response from `get_all_jobs()`
        mock_get_all_jobs.return_value = [
            {'title': 'Job 1', 'recommendation': 5, 'rating': 4},
            {'title': 'Job 2', 'recommendation': 3, 'rating': 5},
            {'title': 'Job 3', 'recommendation': 4, 'rating': 3},
            {'title': 'Job 4', 'recommendation': 6, 'rating': 5},
            {'title': 'Job 5', 'recommendation': 2, 'rating': 2},
            {'title': 'Job 6', 'recommendation': 7, 'rating': 4},
            {'title': 'Job 7', 'recommendation': 8, 'rating': 5},
            {'title': 'Job 8', 'recommendation': 9, 'rating': 3},
            {'title': 'Job 9', 'recommendation': 5, 'rating': 4},
            {'title': 'Job 10', 'recommendation': 3, 'rating': 5},
            {'title': 'Job 11', 'recommendation': 4, 'rating': 5},
        ]

        with self.app as client:
            # Simulate a request to the /top_jobs route
            response = client.get('/top_jobs')

            # Check if the status code is 200 (OK)
            self.assertEqual(response.status_code, 200)

            # Check if the mock functions were called
            mock_initialize_db.assert_called_once()  # Ensure the database initialization function was called once
            mock_get_all_jobs.assert_called_once()  
class TestProcessJobs(unittest.TestCase):
    def test_process_jobs(self):
        """Test the process_jobs function."""
        job_list = [
            {"_id": "123", "title": "Software Engineer"},
            {"_id": "456", "title": "Data Scientist"}
        ]

        expected_output = [
            {"id": "123", "title": "Software Engineer"},
            {"id": "456", "title": "Data Scientist"}
        ]

        result = process_jobs(job_list)
        self.assertEqual(result, expected_output)

class TestGetAllUsers(unittest.TestCase):
    @patch('app.routes.USERS_DB.find')
    @patch('app.routes.process_jobs')
    def test_get_all_users(self, mock_process_jobs, mock_find):
        """Test the get_all_users function."""
        mock_find.return_value = [
            {"_id": "123", "username": "user1"},
            {"_id": "456", "username": "user2"}
        ]

        mock_process_jobs.return_value = [
            {"id": "123", "username": "user1"},
            {"id": "456", "username": "user2"}
        ]

        result = get_all_users()
        self.assertEqual(result, mock_process_jobs.return_value)
        mock_find.assert_called_once()
        mock_process_jobs.assert_called_once_with(list(mock_find.return_value))

if __name__ == '__main__':
    unittest.main()
