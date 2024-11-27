import unittest
from unittest.mock import patch, MagicMock
from app import app
from app.routes import intialize_db, set_test
from bson import ObjectId
import json
class TestDashboard(unittest.TestCase):
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
        patch.stopall()
    @patch('app.routes.get_all_jobs')
    @patch('app.routes.get_all_users')
    @patch('app.routes.get_web_statistics')
    @patch('app.routes.extract_location_data')
    @patch('app.routes.extract_company_data')
    @patch('app.routes.extract_hourly_pay_data')
    @patch('app.routes.extract_rating_data')
    @patch('app.routes.get_avg_sal_titles_by_locations')
    def test_dashboard(self, mock_get_avg_sal_titles_by_locations, mock_extract_rating_data, mock_extract_hourly_pay_data, mock_extract_company_data, mock_extract_location_data, mock_get_web_statistics, mock_get_all_users, mock_get_all_jobs):
        """Test the dashboard route."""
        # Mock the return values of the functions
        mock_get_all_jobs.return_value = [{'title': 'Job1', 'locations': 'City1', 'company': 'Company1', 'hourly_pay': 20, 'rating': 4}]
        mock_get_all_users.return_value = [{'username': 'testuser'}]
        mock_get_web_statistics.return_value = {'total_jobs': 1, 'total_users': 1}
        mock_extract_location_data.return_value = (['City1'], [1])
        mock_extract_company_data.return_value = (['Company1'], [1])
        mock_extract_hourly_pay_data.return_value = (['Job1'], [20])
        mock_extract_rating_data.return_value = ([4], [1])
        mock_get_avg_sal_titles_by_locations.return_value = {'City1': {'Job1': 20}}

        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"City1", response.data)
    @patch('app.routes.get_all_jobs')
    def test_top_jobs(self, mock_get_all_jobs):
        """Test the top_jobs route."""
        # Mock the return value of get_all_jobs
        mock_get_all_jobs.return_value = [
            {'title': 'Job1', 'company': 'Company1', 'locations': 'City1', 'department': 'Engineering', 'recommendation': 5, 'rating': 4},
            {'title': 'Job2', 'company': 'Company2', 'locations': 'City2', 'department': 'Marketing', 'recommendation': 3, 'rating': 5},
            {'title': 'Job3', 'company': 'Company3', 'locations': 'City3', 'department': 'Sales', 'recommendation': 4, 'rating': 3}
        ]

        response = self.client.get('/top_jobs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Job1', response.data)
        self.assertIn(b'Company1', response.data)
        self.assertIn(b'City1', response.data)
        self.assertIn(b'Job2', response.data)
        self.assertIn(b'Company2', response.data)
        self.assertIn(b'City2', response.data)
        self.assertIn(b'Job3', response.data)
        self.assertIn(b'Company3', response.data)
        self.assertIn(b'City3', response.data)
    
if __name__ == '__main__':
    unittest.main()