import unittest
from collections import defaultdict
from app.routes import transform_jobs  # Adjust the import based on your project structure

class TestTransformJobs(unittest.TestCase):
    def test_transform_jobs(self):
        """Test the transform_jobs function."""
        jobs = [
            {
                'title': 'Software Engineer',
                'company': 'Company A',
                'locations': 'Location 1',
                'department': 'Engineering',
                'salary': 100000,
                'experience': 5
            },
            {
                'title': 'Software Engineer',
                'company': 'Company A',
                'locations': 'Location 1',
                'department': 'Engineering',
                'salary': 110000,
                'experience': 6
            },
            {
                'title': 'Data Scientist',
                'company': 'Company B',
                'locations': 'Location 2',
                'department': 'Data',
                'salary': 120000,
                'experience': 4
            }
        ]

        expected_output = [
            {
                'title': 'Software Engineer',
                'company': 'Company A',
                'locations': 'Location 1',
                'department': 'Engineering',
                'other_attributes': [
                    {'salary': 100000, 'experience': 5},
                    {'salary': 110000, 'experience': 6}
                ]
            },
            {
                'title': 'Data Scientist',
                'company': 'Company B',
                'locations': 'Location 2',
                'department': 'Data',
                'other_attributes': [
                    {'salary': 120000, 'experience': 4}
                ]
            }
        ]

        result = transform_jobs(jobs)
        self.assertEqual(result, expected_output)

    def test_transform_jobs_empty(self):
        """Test the transform_jobs function with an empty list."""
        jobs = []
        expected_output = []
        result = transform_jobs(jobs)
        self.assertEqual(result, expected_output)

    def test_transform_jobs_single_entry(self):
        """Test the transform_jobs function with a single job entry."""
        jobs = [
            {
                'title': 'Software Engineer',
                'company': 'Company A',
                'locations': 'Location 1',
                'department': 'Engineering',
                'salary': 100000,
                'experience': 5
            }
        ]

        expected_output = [
            {
                'title': 'Software Engineer',
                'company': 'Company A',
                'locations': 'Location 1',
                'department': 'Engineering',
                'other_attributes': [
                    {'salary': 100000, 'experience': 5}
                ]
            }
        ]

        result = transform_jobs(jobs)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()