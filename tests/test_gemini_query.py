import unittest
from unittest.mock import patch, MagicMock
import os
from app.routes import query_gemini_model


class TestQueryGeminiModel(unittest.TestCase):

    @patch('app.routes.query_gemini')  # Mock get_gemini_feedback
    @patch('app.routes.dict_to_csv')  # Mock dict_to_csv
    @patch('app.routes.get_all_jobs')  # Mock get_all_jobs
    def test_query_gemini_model_success(self, mock_get_all_jobs, mock_dict_to_csv, mock_get_gemini_feedback):
        """
        Test query_gemini_model when the response is successfully fetched from Gemini.
        """
        # Arrange
        mock_get_all_jobs.return_value = [{'id': 1, 'title': 'Job 1'}, {'id': 2, 'title': 'Job 2'}]
        mock_get_gemini_feedback.return_value = "This is the Gemini response."

        # Act
        result = query_gemini_model("Test user message")
        
        # Assert
        mock_get_all_jobs.assert_called_once()  # Ensure get_all_jobs was called
        mock_dict_to_csv.assert_called_once()  # Ensure dict_to_csv was called
        mock_get_gemini_feedback.assert_called_once_with(os.path.join("tmp", "reviews", "tmp_review.txt"), "Test user message")

    @patch('app.routes.query_gemini')  # Mock get_gemini_feedback
    @patch('app.routes.dict_to_csv')  # Mock dict_to_csv
    @patch('app.routes.get_all_jobs')  # Mock get_all_jobs
    def test_query_gemini_model_no_response(self, mock_get_all_jobs, mock_dict_to_csv, mock_get_gemini_feedback):
        """
        Test query_gemini_model when the response from Gemini is None.
        """
        # Arrange
        mock_get_all_jobs.return_value = [{'id': 1, 'title': 'Job 1'}, {'id': 2, 'title': 'Job 2'}]
        mock_get_gemini_feedback.return_value = None

        # Act
        result = query_gemini_model("Test user message")

        # Assert
        mock_get_all_jobs.assert_called_once()  # Ensure get_all_jobs was called
        mock_dict_to_csv.assert_called_once()  # Ensure dict_to_csv was called
        mock_get_gemini_feedback.assert_called_once_with(os.path.join("tmp", "reviews", "tmp_review.txt"), "Test user message")
