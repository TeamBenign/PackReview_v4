import unittest
from unittest.mock import patch, MagicMock
from app import app
from app.routes import intialize_db, set_test
import app.routes as routes
from bson import ObjectId
import json

class TestForum(unittest.TestCase):
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
    #test case for add_forum method
    def test_view_topic_forum(self):
        """Test view a forum."""
        self.setUp()
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        data = {
            'comment': 'very helpful',
            'username': session['username']
        }

        response = self.client.post('/forum/674601b9b7f9ec52b94d45e7', data=data)
        self.assertEqual(response.status_code, 302)
    def test_add_comment_forum(self):
        """Test adding a comment to a forum topic."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        data = {
            'topicId': '674601b9b7f9ec52b94d45e7',
            'content': 'very helpful'
        }

        # Mock the update_one and find_one methods
        self.mock_forum_db.update_one.return_value = None
        self.mock_forum_db.find_one.return_value = {
            '_id': ObjectId('674601b9b7f9ec52b94d45e7'),
            'comments': [{
                '_cid': str(ObjectId()),
                'commenter': 'testuser',
                'content': 'very helpful',
                'likes': [],
                'dislikes': [],
                'timestamp': '2021-10-01 12:00:00'
            }]
        }

        response = self.client.post('/forum/add_comment', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data']['content'], 'very helpful')
    
    def test_update_reaction_topic_like(self):
        """Test updating a reaction to a forum topic or comment."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        data = {
            'topicId': '674601b9b7f9ec52b94d45e7',
            'commentId': '674601b9b7f9ec52b94d45e8',
            'discussionType': 'topic',
            'reactionType': 'like'
        }

        # Mock the find_one and update_one methods
        self.mock_forum_db.find_one.return_value = {
            '_id': ObjectId('674601b9b7f9ec52b94d45e7'),
            'likes': [],
            'dislikes': [],
            'comments': [{
                '_cid': '674601b9b7f9ec52b94d45e8',
                'commenter': 'testuser',
                'content': 'very helpful',
                'likes': [],
                'dislikes': [],
                'timestamp': '2021-10-01 12:00:00'
            }]
        }
        self.mock_forum_db.update_one.return_value = None

        # Mock the find_one method for USERS_DB
        self.mock_users_db.find_one.return_value = {
            'username': 'testuser',
            'reviews': ['review1', 'review2', 'review3', 'review4', 'review5']
        }

        response = self.client.post('/forum/update_reaction', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data'], 0) 
    def test_update_reaction_topic_dislike(self):
        """Test updating a reaction to a forum topic or comment."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        data = {
            'topicId': '674601b9b7f9ec52b94d45e7',
            'commentId': '674601b9b7f9ec52b94d45e8',
            'discussionType': 'topic',
            'reactionType': 'dislike'
        }

        # Mock the find_one and update_one methods
        self.mock_forum_db.find_one.return_value = {
            '_id': ObjectId('674601b9b7f9ec52b94d45e7'),
            'likes': [],
            'dislikes': [],
            'comments': [{
                '_cid': '674601b9b7f9ec52b94d45e8',
                'commenter': 'testuser',
                'content': 'very helpful',
                'likes': [],
                'dislikes': [],
                'timestamp': '2021-10-01 12:00:00'
            }]
        }
        self.mock_forum_db.update_one.return_value = None

        # Mock the find_one method for USERS_DB
        self.mock_users_db.find_one.return_value = {
            'username': 'testuser',
            'reviews': ['review1', 'review2', 'review3', 'review4', 'review5']
        }

        response = self.client.post('/forum/update_reaction', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data'], 0) 
    def test_update_reaction_comment_like(self):
        """Test updating a like reaction to a forum comment."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        data = {
            'topicId': '674601b9b7f9ec52b94d45e7',
            'commentId': '674601b9b7f9ec52b94d45e8',
            'discussionType': 'comment',
            'reactionType': 'like'
        }

        # Mock the find_one and update_one methods for FORUM_DB
        self.mock_forum_db.find_one.return_value = {
            '_id': ObjectId('674601b9b7f9ec52b94d45e7'),
            'likes': [],
            'dislikes': [],
            'comments': [{
                '_cid': '674601b9b7f9ec52b94d45e8',
                'commenter': 'testuser',
                'content': 'very helpful',
                'likes': [],
                'dislikes': [],
                'timestamp': '2021-10-01 12:00:00'
            }]
        }
        self.mock_forum_db.update_one.return_value = None

        response = self.client.post('/forum/update_reaction', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data'], 0)
    def test_update_reaction_comment_dislike(self):
        """Test updating a dislike reaction to a forum comment."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        data = {
            'topicId': '674601b9b7f9ec52b94d45e7',
            'commentId': '674601b9b7f9ec52b94d45e8',
            'discussionType': 'comment',
            'reactionType': 'dislike'
        }

        # Mock the find_one and update_one methods for FORUM_DB
        self.mock_forum_db.find_one.return_value = {
            '_id': ObjectId('674601b9b7f9ec52b94d45e7'),
            'likes': [],
            'dislikes': [],
            'comments': [{
                '_cid': '674601b9b7f9ec52b94d45e8',
                'commenter': 'testuser',
                'content': 'very helpful',
                'likes': [],
                'dislikes': [],
                'timestamp': '2021-10-01 12:00:00'
            }]
        }
        self.mock_forum_db.update_one.return_value = None

        response = self.client.post('/forum/update_reaction', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['data'], 0)
    @patch('app.routes.USERS_DB.find_one')
    def test_get_badge_newbie(self, mock_find_one):
        """Test get_badge function for NewBie badge."""
        mock_find_one.return_value = {'username': 'testuser', 'reviews': ['review1', 'review2', 'review3', 'review4']}
        from app.routes import get_badge
        badge = get_badge('testuser')
        self.assertEqual(badge, 'NewBie')

    @patch('app.routes.USERS_DB.find_one')
    def test_get_badge_intermediate(self, mock_find_one):
        """Test get_badge function for Intermediate badge."""
        mock_find_one.return_value = {'username': 'testuser', 'reviews': ['review1', 'review2', 'review3', 'review4', 'review5', 'review6', 'review7', 'review8', 'review9']}
        from app.routes import get_badge
        badge = get_badge('testuser')
        self.assertEqual(badge, 'Intermediate')

    @patch('app.routes.USERS_DB.find_one')
    def test_get_badge_advanced(self, mock_find_one):
        """Test get_badge function for Advanced badge."""
        mock_find_one.return_value = {'username': 'testuser', 'reviews': ['review1', 'review2', 'review3', 'review4', 'review5', 'review6', 'review7', 'review8', 'review9', 'review10', 'review11', 'review12', 'review13', 'review14']}
        from app.routes import get_badge
        badge = get_badge('testuser')
        self.assertEqual(badge, 'Advanced')

    @patch('app.routes.USERS_DB.find_one')
    def test_get_badge_expert(self, mock_find_one):
        """Test get_badge function for Expert badge."""
        mock_find_one.return_value = {'username': 'testuser', 'reviews': ['review1', 'review2', 'review3', 'review4', 'review5', 'review6', 'review7', 'review8', 'review9', 'review10', 'review11', 'review12', 'review13', 'review14', 'review15']}
        from app.routes import get_badge
        badge = get_badge('testuser')
        self.assertEqual(badge, 'Expert')

    @patch('app.routes.USERS_DB.find_one')
    def test_get_badge_anonymous(self, mock_find_one):
        """Test get_badge function for Anonymous user."""
        mock_find_one.return_value = None
        from app.routes import get_badge
        badge = get_badge('testuser')
        self.assertEqual(badge, 'Anonymous')
    @patch('app.routes.get_badge')
    def test_get_refined_topics(self, mock_get_badge):
        """Test getRefinedTopics function."""
        mock_get_badge.side_effect = lambda username: 'Expert' if username == 'testuser' else 'NewBie'
        topics = [{
            'author': 'testuser',
            'timestamp': '2021-10-01 12:00:00',
            'likes': ['user1', 'user2'],
            'dislikes': ['user3'],
            'comments': [{
                'commenter': 'user4',
                'timestamp': '2021-10-01 12:00:00',
                'likes': ['user5'],
                'dislikes': ['user6']
            }]
        }]
        from app.routes import getRefinedTopics
        refined_topics = getRefinedTopics(topics)
        self.assertEqual(refined_topics[0]['author_badge'], 'Expert')
        self.assertEqual(refined_topics[0]['timestamp'], 'Friday, October 01, 2021, 12:00 PM')
        self.assertEqual(refined_topics[0]['topics_likes'], 2)
        self.assertEqual(refined_topics[0]['topics_dislikes'], 1)
        self.assertEqual(refined_topics[0]['likes'][0]['badge'], 'NewBie')
        self.assertEqual(refined_topics[0]['dislikes'][0]['badge'], 'NewBie')
        self.assertEqual(refined_topics[0]['comments'][0]['commenter_badge'], 'NewBie')
        self.assertEqual(refined_topics[0]['comments'][0]['timestamp'], 'Friday, October 01, 2021, 12:00 PM')
        self.assertEqual(refined_topics[0]['comments'][0]['comment_likes'], 1)
        self.assertEqual(refined_topics[0]['comments'][0]['comment_dislikes'], 1)
        self.assertEqual(refined_topics[0]['comments'][0]['likes'][0]['badge'], 'NewBie')
        self.assertEqual(refined_topics[0]['comments'][0]['dislikes'][0]['badge'], 'NewBie')
    
    def test_upvote_post(self):
        """Test upvoting a forum topic."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        topic_id = '674601b9b7f9ec52b94d45e7'

        # Mock the update_one method
        self.mock_forum_db.update_one.return_value = None

        response = self.client.post(f'/forum/{topic_id}/upvote_post')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/forum')

    def test_downvote_post(self):
        """Test downvoting a forum topic."""
        with self.client.session_transaction() as session:
            session['username'] = 'testuser'

        topic_id = '674601b9b7f9ec52b94d45e7'

        # Mock the update_one method
        self.mock_forum_db.update_one.return_value = None

        response = self.client.post(f'/forum/{topic_id}/downvote_post')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/forum')
    def test_get_web_statistics(self):
        """Test the get_web_statistics function."""
        jobs = [
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1', 'rating': 4.5},
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1', 'rating': 4.0},
            {'title': 'Data Scientist', 'company': 'Company B', 'locations': 'Location 2', 'rating': 5.0},
            {'title': 'Data Scientist', 'company': 'Company B', 'locations': 'Location 2', 'rating': 4.5},
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 2', 'rating': 3.5}
        ]
        users = [
            {'username': 'user1'},
            {'username': 'user2'},
            {'username': 'user3'}
        ]

        expected_output = {
            "total_jobs": 5,
            "total_companies": 2,
            "total_titles": 2,
            "total_locations": 2,
            'avg_ratings': 4.3,
            'total_users': 3
        }

        result = routes.get_web_statistics(jobs, users)
        self.assertEqual(result, expected_output)

    def test_get_web_statistics_empty(self):
        """Test the get_web_statistics function with empty lists."""
        jobs = []
        users = []
        expected_output = {
            "total_jobs": 0,
            "total_companies": 0,
            "total_titles": 0,
            "total_locations": 0,
            'avg_ratings': 0,
            'total_users': 0
        }
        result = routes.get_web_statistics(jobs, users)
        self.assertEqual(result, expected_output)
def __main__():
    unittest.main()