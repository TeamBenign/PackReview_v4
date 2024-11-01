"""
This module contains unit tests for the Flask application routes.

It tests the following routes:
- Index route
- Page content retrieval and submission
- Adding a review
- User signup and login
- Additional functionality related to reviews

Each test ensures that the expected HTTP status codes are returned for 
various endpoints, validating the application's behavior during testing.
"""

import os
import sys
from app import app
sys.path.append(os.getcwd()[:-5] + "app")


def test_index_route():
    """Test the index route for a successful response."""
    response = app.test_client().get('/')
    assert response.status_code == 200

def test_page_content_route():
    """Test the page content POST route for a successful response."""
    response = app.test_client().post('/pageContentPost', data={"search": "Setup"})
    assert response.status_code == 200

# def test_add_post_route():
#     """Test adding a new post via the page content POST route."""
#     response = app.test_client().post('/pageContentPost', data={
#         "job_title": "1",
#         "job_description": "2",
#         "department": "3",
#         "locations": "4",
#         "hourly_pay": "5",
#         "benefits": "6",
#         "review": "7",
#         "rating": "2",
#         "recommendation": "2",
#         "search": ""
#     })
#     assert response.status_code == 200

# def test_signup_route():
#     """Test the signup route for a successful response."""
#     response = app.test_client().get('/signup')
#     assert response.status_code == 200

def test_login_route():
    """Test the login route for a successful response."""
    response = app.test_client().get('/login')
    assert response.status_code == 200

def test_add_review_route():
    """Test the add review route to ensure proper redirection."""
    response = app.test_client().get('/review')
    assert response.status_code == 302

def test_review_route():
    """Test the review route for a successful response."""
    response = app.test_client().get('/pageContent')
    assert response.status_code == 200

# Running the tests
test_index_route()
test_review_route()
test_add_review_route()
# test_add_post_route()
test_page_content_route()
