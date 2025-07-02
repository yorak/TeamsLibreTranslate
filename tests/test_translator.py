"""Unit tests for TranslationService."""

import unittest
from unittest.mock import Mock, patch, MagicMock
import requests
import json
from src.core.translator import TranslationService
from src.config.settings import TranslationConfig


class TestTranslationService(unittest.TestCase):
    """Test cases for TranslationService class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = TranslationConfig()
        self.config.libretranslate_url = "http://test.example.com/translate"
        self.config.api_key = "test_key"
        self.config.source_language = "fi"
        self.config.target_language = "en"
        self.service = TranslationService(self.config)
    
    @patch('src.core.translator.requests.post')
    def test_translate_success(self, mock_post):
        """Test successful translation."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"translatedText": "Hello world"}
        mock_post.return_value = mock_response
        
        result = self.service.translate("Hei maailma")
        
        # Verify result
        self.assertEqual(result, "Hello world")
        
        # Verify request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]['json']['q'], "Hei maailma")
        self.assertEqual(call_args[1]['json']['source'], "fi")
        self.assertEqual(call_args[1]['json']['target'], "en")
    
    @patch('src.core.translator.requests.post')
    def test_translate_with_custom_languages(self, mock_post):
        """Test translation with custom languages."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"translatedText": "Hola mundo"}
        mock_post.return_value = mock_response
        
        result = self.service.translate("Hello world", "en", "es")
        
        self.assertEqual(result, "Hola mundo")
        
        # Verify custom languages were used
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]['json']['source'], "en")
        self.assertEqual(call_args[1]['json']['target'], "es")
    
    @patch('src.core.translator.requests.post')
    def test_translate_empty_text(self, mock_post):
        """Test translation with empty text."""
        result = self.service.translate("")
        
        # Should return None without making request
        self.assertIsNone(result)
        mock_post.assert_not_called()
    
    @patch('src.core.translator.requests.post')
    def test_translate_api_error(self, mock_post):
        """Test translation with API error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response
        
        result = self.service.translate("Test text")
        
        self.assertIsNone(result)
    
    @patch('src.core.translator.requests.post')
    def test_translate_network_error(self, mock_post):
        """Test translation with network error."""
        mock_post.side_effect = requests.exceptions.RequestException("Network error")
        
        result = self.service.translate("Test text")
        
        self.assertIsNone(result)
    
    @patch('src.core.translator.requests.post')
    def test_translate_invalid_json(self, mock_post):
        """Test translation with invalid JSON response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_post.return_value = mock_response
        
        result = self.service.translate("Test text")
        
        self.assertIsNone(result)
    
    @patch('src.core.translator.requests.get')
    def test_is_service_available_success(self, mock_get):
        """Test service availability check success."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = self.service.is_service_available()
        
        self.assertTrue(result)
        mock_get.assert_called_once_with(
            "http://test.example.com/languages",
            timeout=5
        )
    
    @patch('src.core.translator.requests.get')
    def test_is_service_available_failure(self, mock_get):
        """Test service availability check failure."""
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")
        
        result = self.service.is_service_available()
        
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()