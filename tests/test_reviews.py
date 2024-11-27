import unittest
from unittest.mock import patch, MagicMock
from pymongo.errors import PyMongoError
from collections import Counter

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
    @patch('app.routes.JOBS_DB.find_one')
    @patch('app.routes.intialize_db')
    def test_update_review_success(self, mock_initialize_db, mock_find_one):
        """Test updating a job review successfully."""
        mock_find_one.return_value = {"_id": "123", "title": "Software Engineer"}

        response = self.app.get('/api/updateReview?id=123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Software Engineer', response.data)
        mock_find_one.assert_called_once_with({"_id": "123"})

    @patch('app.routes.JOBS_DB.find_one')
    @patch('app.routes.intialize_db')
    def test_update_review_not_found(self, mock_initialize_db, mock_find_one):
        """Test updating a job review that does not exist."""
        mock_find_one.return_value = None

        response = self.app.get('/api/updateReview?id=123')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Review not found', response.data)
        mock_find_one.assert_called_once_with({"_id": "123"})

    @patch('app.routes.JOBS_DB.find_one')
    @patch('app.routes.intialize_db')
    def test_update_review_invalid_id(self, mock_initialize_db, mock_find_one):
        """Test updating a job review with an invalid ID."""
        mock_find_one.side_effect = KeyError("Invalid ID")

        response = self.app.get('/api/updateReview?id=invalid_id')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid ID provided', response.data)

    @patch('app.routes.JOBS_DB.find_one')
    @patch('app.routes.intialize_db')
    def test_update_review_db_error(self, mock_initialize_db, mock_find_one):
        """Test updating a job review with a database error."""
        mock_find_one.side_effect = PyMongoError("Database error")

        response = self.app.get('/api/updateReview?id=123')
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'An error occurred', response.data)

class TestGetAvgSalTitlesByLocations(unittest.TestCase):
    def test_get_avg_sal_titles_by_locations(self):
        """Test the get_avg_sal_titles_by_locations function."""
        jobs = [
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1', 'hourly_pay': 100},
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1', 'hourly_pay': 110},
            {'title': 'Data Scientist', 'company': 'Company B', 'locations': 'Location 2', 'hourly_pay': 120},
            {'title': 'Data Scientist', 'company': 'Company B', 'locations': 'Location 2', 'hourly_pay': 130},
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 2', 'hourly_pay': 105}
        ]

        expected_output = {
            "locations": ['Location 1', 'Location 2'],
            "titles": ['Software Engineer', 'Data Scientist'],
            "average_pay": {
                'Software Engineer': [105.0, 105.0],
                'Data Scientist': [0, 125.0]
            }
        }

        result = routes.get_avg_sal_titles_by_locations(jobs)

        # Sort the locations and titles in both expected and actual outputs
        result['locations'].sort()
        result['titles'].sort()
        for title in result['average_pay']:
            result['average_pay'][title] = sorted(result['average_pay'][title])

        expected_output['locations'].sort()
        expected_output['titles'].sort()
        for title in expected_output['average_pay']:
            expected_output['average_pay'][title] = sorted(expected_output['average_pay'][title])

        self.assertEqual(result, expected_output)

    def test_get_avg_sal_titles_by_locations_empty(self):
        """Test the get_avg_sal_titles_by_locations function with an empty list."""
        jobs = []
        expected_output = {
            "locations": [],
            "titles": [],
            "average_pay": {}
        }
        result = routes.get_avg_sal_titles_by_locations(jobs)
        self.assertEqual(result, expected_output)
class TestGetAvgSalTitlesByLocations(unittest.TestCase):
    def test_get_avg_sal_titles_by_locations(self):
        """Test the get_avg_sal_titles_by_locations function."""
        jobs = [
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1', 'hourly_pay': 100},
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1', 'hourly_pay': 110},
            {'title': 'Data Scientist', 'company': 'Company B', 'locations': 'Location 2', 'hourly_pay': 120},
            {'title': 'Data Scientist', 'company': 'Company B', 'locations': 'Location 2', 'hourly_pay': 130},
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 2', 'hourly_pay': 105}
        ]

        expected_output = {
            "locations": ['Location 1', 'Location 2'],
            "titles": ['Software Engineer', 'Data Scientist'],
            "average_pay": {
                'Software Engineer': [105.0, 105.0],
                'Data Scientist': [0, 125.0]
            }
        }

        result = routes.get_avg_sal_titles_by_locations(jobs)

        # Sort the locations and titles in both expected and actual outputs
        result['locations'].sort()
        result['titles'].sort()
        for title in result['average_pay']:
            result['average_pay'][title] = sorted(result['average_pay'][title])

        expected_output['locations'].sort()
        expected_output['titles'].sort()
        for title in expected_output['average_pay']:
            expected_output['average_pay'][title] = sorted(expected_output['average_pay'][title])

        self.assertEqual(result, expected_output)

    def test_get_avg_sal_titles_by_locations_empty(self):
        """Test the get_avg_sal_titles_by_locations function with an empty list."""
        jobs = []
        expected_output = {
            "locations": [],
            "titles": [],
            "average_pay": {}
        }
        result = routes.get_avg_sal_titles_by_locations(jobs)
        self.assertEqual(result, expected_output)

class TestExtractDataFunctions(unittest.TestCase):
    def test_extract_location_data(self):
        """Test the extract_location_data function."""
        jobs = [
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1'},
            {'title': 'Data Scientist', 'company': 'Company B', 'locations': 'Location 2'},
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1'}
        ]

        expected_locations = ['Location 1', 'Location 2']
        expected_counts = [2, 1]

        locations, counts = routes.extract_location_data(jobs)
        self.assertEqual(locations, expected_locations)
        self.assertEqual(counts, expected_counts)

    def test_extract_company_data(self):
        """Test the extract_company_data function."""
        jobs = [
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1'},
            {'title': 'Data Scientist', 'company': 'Company B', 'locations': 'Location 2'},
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1'}
        ]

        expected_companies = ['Company A', 'Company B']
        expected_counts = [2, 1]

        companies, counts = routes.extract_company_data(jobs)
        self.assertEqual(companies, expected_companies)
        self.assertEqual(counts, expected_counts)

    def test_extract_hourly_pay_data(self):
        """Test the extract_hourly_pay_data function."""
        jobs = [
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1', 'hourly_pay': 100},
            {'title': 'Data Scientist', 'company': 'Company B', 'locations': 'Location 2', 'hourly_pay': 120},
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1', 'hourly_pay': 110}
        ]

        expected_titles = ['Software Engineer', 'Data Scientist', 'Software Engineer']
        expected_hourly_pays = [100, 120, 110]

        titles, hourly_pays = routes.extract_hourly_pay_data(jobs)
        self.assertEqual(titles, expected_titles)
        self.assertEqual(hourly_pays, expected_hourly_pays)

    def test_extract_rating_data(self):
        """Test the extract_rating_data function."""
        jobs = [
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1', 'rating': 4.5},
            {'title': 'Data Scientist', 'company': 'Company B', 'locations': 'Location 2', 'rating': 5.0},
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1', 'rating': 4.0}
        ]

        expected_ratings = [4.5, 5.0, 4.0]
        expected_counts = Counter([4.5, 5.0, 4.0])

        ratings, counts = routes.extract_rating_data(jobs)
        self.assertEqual(ratings, expected_ratings)
        self.assertEqual(counts, expected_counts)

if __name__ == '__main__':
    unittest.main()