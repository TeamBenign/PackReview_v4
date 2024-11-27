import unittest
from unittest.mock import patch
from flask import json
from app import app

class TestGeminiResponse(unittest.TestCase):
    def setUp(self):
        # Configure the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.routes.query_gemini_model')  # Mock query_gemini_model function
    def test_get_gemini_response(self, mock_query_gemini_model):
        """
        Test the /get_gemini_response route when a valid message is sent.
        """
        # Sample input data
        user_message = "What is the review of the google?"

        # Mock the return value of query_gemini_model
        mock_query_gemini_model.return_value = ("This is the AI response.", "12345")

        # Simulate a POST request with JSON data
        response = self.app.post('/get_gemini_response', 
                                 data=json.dumps({"message": user_message}),
                                 content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 200)  # Ensure the request was successful
        response_json = response.get_json()

        # Check that the response JSON contains the expected 'ai_message'
        expected_ai_message = "This is the AI response.\n\nClick <a href=\"/review?review_id=12345\">here</a> to see the review details."
        self.assertEqual(response_json['ai_message'], expected_ai_message)

        # Check that query_gemini_model was called once with the correct argument
        mock_query_gemini_model.assert_called_once_with(user_message)
    
    @patch('app.routes.query_gemini_model')  # Mock query_gemini_model function
    def test_get_gemini_response_no_message(self, mock_query_gemini_model):
       
        # Simulate a POST request with no message in the JSON data
        response = self.app.post('/get_gemini_response', 
                                 data=json.dumps({}),
                                 content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 500)  # Bad request, since message is missing


    @patch('app.routes.query_gemini_model')  # Mock query_gemini_model function
    def test_get_gemini_response_invalid_json(self, mock_query_gemini_model):
  
        # Simulate a POST request with invalid JSON data
        response = self.app.post('/get_gemini_response', 
                                 data="invalid json", 
                                 content_type='application/json')

        # Assertions
        self.assertEqual(response.status_code, 400)  
        
if __name__ == '__main__':
    unittest.main()
