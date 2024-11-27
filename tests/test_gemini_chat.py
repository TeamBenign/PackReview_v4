import unittest
from unittest.mock import patch, MagicMock
from app.gemini_chat import get_gemini_feedback  # Replace with the actual module name
from app.routes import query_gemini_model, chunk_text
from app.routes import query_gemini

class TestGeminiFeedback(unittest.TestCase):
    # Test Case 1: Test with valid inputs (csv_path and user_prompt)
    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.upload_file")
    def test_get_gemini_feedback_valid(self, mock_upload_file, mock_GenerativeModel):
        # Arrange
        csv_path = "valid.txt"
        user_prompt = "Tell me about the work culture"
        
        # Mock the file upload to avoid the need for an actual file
        mock_upload_file.return_value = "mocked_file_content"
        
        # Mock the response from the API call
        mock_response = MagicMock()
        mock_response.text = "para 1: The work culture is great. para 2: [ID_START] 1, 2, 3 [ID_END]"
        
        # Setup the mock to return the response
        mock_GenerativeModel.return_value.generate_content.return_value = mock_response
        
        # Act
        response_text, ids_string = get_gemini_feedback(csv_path, user_prompt)
        
        # Assert
        self.assertEqual(response_text, "The work culture is great.")
        self.assertEqual(ids_string, "1, 2, 3")

    # Test Case 2: Test with missing or invalid CSV path
    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.upload_file")
    def test_get_gemini_feedback_invalid_csv(self, mock_upload_file, mock_GenerativeModel):
        # Arrange
        csv_path = ""  # Invalid path
        user_prompt = "Tell me about the work culture"
        
        # Act
        response = get_gemini_feedback(csv_path, user_prompt)
        
        # Assert
        self.assertIsNone(response)

    # Test Case 3: Test with malformed API response (no IDs found)
    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.upload_file")
    def test_get_gemini_feedback_no_ids(self, mock_upload_file, mock_GenerativeModel):
        # Arrange
        csv_path = "valid_path.csv"
        user_prompt = "Tell me about the work culture"
        
        # Mock the file upload to avoid the need for an actual file
        mock_upload_file.return_value = "mocked_file_content"
        
        # Mock the response from the API call
        mock_response = MagicMock()
        mock_response.text = "para 1: The work culture is great. para 2: No IDs here."
        
        # Setup the mock to return the response
        mock_GenerativeModel.return_value.generate_content.return_value = mock_response
        
        # Act
        response_text, ids_string = get_gemini_feedback(csv_path, user_prompt)
        
        # Assert
        self.assertEqual(response_text, "The work culture is great.")
        self.assertEqual(ids_string, "")

    # Test Case 4: Test when an error occurs in the API call
    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.upload_file")
    def test_get_gemini_feedback_api_error(self, mock_upload_file, mock_GenerativeModel):
        # Arrange
        csv_path = "valid_path.csv"
        user_prompt = "Tell me about the work culture"
        
        # Simulate an exception in the API call
        mock_GenerativeModel.return_value.generate_content.side_effect = Exception("API Error")
        
        # Act
        response = get_gemini_feedback(csv_path, user_prompt)
        
        # Assert
        self.assertIsNone(response)

    # Test Case 5: Test empty user prompt
    @patch("google.generativeai.GenerativeModel")
    @patch("google.generativeai.upload_file")
    def test_get_gemini_feedback_empty_prompt(self, mock_upload_file, mock_GenerativeModel):
        # Arrange
        csv_path = "valid_path.csv"
        user_prompt = ""  # Empty user prompt
        
        # Mock the file upload to avoid the need for an actual file
        mock_upload_file.return_value = "mocked_file_content"
        
        # Mock the response from the API call
        mock_response = MagicMock()
        mock_response.text = "para 1: The work culture is great. para 2: [ID_START] 1, 2 [ID_END]"
        
        # Setup the mock to return the response
        mock_GenerativeModel.return_value.generate_content.return_value = mock_response
        
        # Act
        response_text, ids_string = get_gemini_feedback(csv_path, user_prompt)
        
        # Assert
        self.assertEqual(response_text, "The work culture is great.")
        self.assertEqual(ids_string, "1, 2")
    
    @patch('app.gemini_chat.get_gemini_feedback')
    @patch('app.routes.dict_to_csv')
    @patch('app.routes.get_all_jobs')
    def test_query_gemini_model(self, mock_get_all_jobs, mock_dict_to_csv, mock_get_gemini_feedback):
        """Test the query_gemini_model function."""
        user_message = "Tell me about job reviews"
        mock_get_all_jobs.return_value = [
            {'title': 'Software Engineer', 'company': 'Company A', 'locations': 'Location 1', 'rating': 4.5},
            {'title': 'Data Scientist', 'company': 'Company B', 'locations': 'Location 2', 'rating': 5.0}
        ]
        mock_get_gemini_feedback.return_value = "para 1: Great job reviews. para 2: [ID_START] 1, 2 [ID_END]"

        result = query_gemini_model(user_message)
        self.assertIn("Based on", result[0])
    # Test Case 5: Test chunk_text function
    def test_chunk_text(self):
        """Test the chunk_text function."""
        text = "This is a long text that needs to be chunked into smaller pieces."
        chunk_size = 10
        expected_output = [
            "This is a",
            "long text",
            "that needs",
            "to be",
            "chunked",
            "into",
            "smaller",
            "pieces."
        ]

        result = chunk_text(text, chunk_size)
        self.assertEqual(result, expected_output)
if __name__ == "__main__":
    unittest.main()
