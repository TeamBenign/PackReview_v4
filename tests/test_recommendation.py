import unittest

from app.recommendation import recommend_jobs

class TestRecommendJobs(unittest.TestCase):
    def setUp(self):
        self.reviews = [
            {"id": 1, "author": "user1", "rating": 5, "recommendation": 10},
            {"id": 2, "author": "user1", "rating": 4, "recommendation": 8},
            {"id": 3, "author": "user2", "rating": 3, "recommendation": 6},
            {"id": 4, "author": "user2", "rating": 2, "recommendation": 4},
            {"id": 5, "author": "user3", "rating": 5, "recommendation": 10},
            {"id": 1, "author": "user3", "rating": 4, "recommendation": 8},
        ]

    def test_recommend_jobs_valid_user(self):
        target_user = "user1"
        top_n = 3
        recommendations = recommend_jobs(self.reviews, target_user, top_n)
        self.assertIsInstance(recommendations, list)
        self.assertTrue(len(recommendations) <= top_n)
        self.assertTrue(all(isinstance(job, dict) for job in recommendations))
    
    def test_recommend_jobs_nonexistent_user(self):
        target_user = "nonexistent_user"
        recommendations = recommend_jobs(self.reviews, target_user, 3)
        self.assertIsNone(recommendations)
    
    def test_recommend_jobs_empty_reviews(self):
        empty_reviews = []
        target_user = "user1"
        recommendations = recommend_jobs(empty_reviews, target_user, 3)
        self.assertEqual(recommendations, [])
    
    def test_recommend_jobs_no_unrated_jobs(self):
        # Simulate a user who has rated all jobs
        reviews = [
            {"id": 1, "author": "user1", "rating": 5, "recommendation": 10},
            {"id": 2, "author": "user1", "rating": 4, "recommendation": 8},
        ]
        target_user = "user1"
        recommendations = recommend_jobs(reviews, target_user, 3)
        self.assertEqual(recommendations, [])
    
    def test_recommend_jobs_partial_ratings(self):
        # Test for a user with partial ratings
        reviews = [
            {"id": 1, "author": "user1", "rating": 5, "recommendation": 10},
            {"id": 2, "author": "user1", "rating": None, "recommendation": None},
            {"id": 3, "author": "user2", "rating": 4, "recommendation": 8},
            {"id": 1, "author": "user2", "rating": 2, "recommendation": 8},
        ]
        target_user = "user1"
        recommendations = recommend_jobs(reviews, target_user, 2)
        self.assertGreater(len(recommendations), 0)

    def test_recommend_jobs_invalid_top_n(self):
        # Test with invalid `top_n` parameter
        target_user = "user1"
        with self.assertRaises(ValueError):
            recommend_jobs(self.reviews, target_user, -1)

    def test_recommend_jobs_invalid_data(self):
        # Test with invalid review data structure
        invalid_reviews = [{"id": 1, "author": "user1"}]  # Missing fields
        target_user = "user1"
        with self.assertRaises(KeyError):
            recommend_jobs(invalid_reviews, target_user, 3)

if __name__ == "__main__":
    unittest.main()
