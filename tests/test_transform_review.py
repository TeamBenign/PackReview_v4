import unittest
from collections import defaultdict
from app.routes import transform_jobs  # Replace 'yourmodule' with the actual module name

class TestTransformJobs(unittest.TestCase):
    def test_transform_jobs(self):
        # Input data
        jobs = [
            {'title': 'Engineer', 'company': 'ABC', 'locations': 'NY', 'department': 'R&D', 'salary': 100000},
            {'title': 'Engineer', 'company': 'ABC', 'locations': 'NY', 'department': 'R&D', 'benefits': 'Health'},
            {'title': 'Manager', 'company': 'XYZ', 'locations': 'CA', 'department': 'Sales', 'salary': 120000},
            {'title': 'Engineer', 'company': 'ABC', 'locations': 'NY', 'department': 'R&D', 'bonus': 5000},
            {'title': 'Manager', 'company': 'XYZ', 'locations': 'CA', 'department': 'Sales', 'benefits': '401k'},
        ]

        # Expected output
        expected_output = [
            {
                'title': 'Engineer',
                'company': 'ABC',
                'locations': 'NY',
                'department': 'R&D',
                'other_attributes': [
                    {'salary': 100000},
                    {'benefits': 'Health'},
                    {'bonus': 5000},
                ],
            },
            {
                'title': 'Manager',
                'company': 'XYZ',
                'locations': 'CA',
                'department': 'Sales',
                'other_attributes': [
                    {'salary': 120000},
                    {'benefits': '401k'},
                ],
            },
        ]

        # Call the function
        result = transform_jobs(jobs)

        # Sort the results to ensure order doesn't affect comparison
        result_sorted = sorted(result, key=lambda x: (x['title'], x['company'], x['locations'], x['department']))
        expected_output_sorted = sorted(expected_output, key=lambda x: (x['title'], x['company'], x['locations'], x['department']))

        # Assert the results match the expected output
        self.assertEqual(result_sorted, expected_output_sorted)

if __name__ == '__main__':
    unittest.main()
