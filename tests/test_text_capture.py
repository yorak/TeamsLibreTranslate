"""Unit tests for TextCapture."""

import unittest
from unittest.mock import Mock, patch, MagicMock
import time
from src.core.text_capture import TextCapture
from src.config.settings import CaptureConfig


class TestTextCapture(unittest.TestCase):
    """Test cases for TextCapture class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = CaptureConfig()
        self.config.split_marker = "Test Speaker"
        self.config.clipboard_delay = 0.1
        self.config.selection_delay = 0.1
        self.capture = TextCapture(self.config)
    
    @patch('src.core.text_capture.pyperclip.paste')
    @patch('src.core.text_capture.pyautogui.hotkey')
    @patch('src.core.text_capture.pyautogui.click')
    @patch('src.core.text_capture.time.sleep')
    def test_grab_text_success(self, mock_sleep, mock_click, mock_hotkey, mock_paste):
        """Test successful text capture."""
        mock_paste.return_value = "Test captured text"
        
        result = self.capture.grab_text()
        
        self.assertEqual(result, "Test captured text")
        mock_click.assert_called_once()
        self.assertEqual(mock_hotkey.call_count, 2)
        mock_hotkey.assert_any_call('ctrl', 'a')
        mock_hotkey.assert_any_call('ctrl', 'c')
    
    @patch('src.core.text_capture.pyperclip.paste')
    @patch('src.core.text_capture.pyautogui.hotkey')
    @patch('src.core.text_capture.pyautogui.click')
    def test_grab_text_exception(self, mock_click, mock_hotkey, mock_paste):
        """Test text capture with exception."""
        mock_click.side_effect = Exception("Click failed")
        
        result = self.capture.grab_text()
        
        self.assertEqual(result, "")
    
    @patch.object(TextCapture, 'grab_text')
    def test_mark_all_previous_translated(self, mock_grab_text):
        """Test marking all previous text as translated."""
        mock_grab_text.return_value = "Previous text Test Speaker New text"
        
        self.capture.mark_all_previous_translated()
        
        # Should have marked previous text as translated
        self.assertIn("Previous text", self.capture.already_translated)
        self.assertIn("New text", self.capture.already_translated)
        self.assertEqual(self.capture.prev_translated_complete_line, "New text")
    
    @patch.object(TextCapture, 'grab_text')
    def test_get_transcript_to_translate_new_complete_line(self, mock_grab_text):
        """Test getting transcript when there's a new complete line."""
        # Set up initial state
        self.capture.prev_translated_complete_line = "Old line"
        
        # Mock captured text with new complete line
        mock_grab_text.return_value = "Old line Test Speaker New complete line Test Speaker Incomplete"
        
        result = self.capture.get_transcript_to_translate(5.0)
        
        self.assertEqual(result, "New complete line")
        self.assertEqual(self.capture.prev_translated_complete_line, "New complete line")
    
    @patch.object(TextCapture, 'grab_text')
    def test_get_transcript_to_translate_incomplete_line_timeout(self, mock_grab_text):
        """Test getting transcript when incomplete line should be translated due to timeout."""
        # Set up initial state - simulate time passing
        self.capture.prev_translation_at = time.time() - 6.0  # 6 seconds ago
        
        mock_grab_text.return_value = "Previous Test Speaker Incomplete line"
        
        result = self.capture.get_transcript_to_translate(5.0)
        
        self.assertEqual(result, "Incomplete line")
    
    @patch.object(TextCapture, 'grab_text')
    def test_get_transcript_to_translate_no_translation_needed(self, mock_grab_text):
        """Test getting transcript when no translation is needed."""
        # Set up state where text is already translated
        self.capture.already_translated.add("Same text")
        
        mock_grab_text.return_value = "Previous Test Speaker Same text"
        
        result = self.capture.get_transcript_to_translate(5.0)
        
        self.assertIsNone(result)
    
    @patch.object(TextCapture, 'grab_text')
    def test_get_transcript_to_translate_no_split_marker(self, mock_grab_text):
        """Test getting transcript when split marker is not found."""
        mock_grab_text.return_value = "Text without split marker"
        
        result = self.capture.get_transcript_to_translate(5.0)
        
        self.assertIsNone(result)
    
    @patch.object(TextCapture, 'grab_text')
    def test_get_transcript_to_translate_clean_caption_message(self, mock_grab_text):
        """Test that 'Close caption has started.' message is cleaned."""
        mock_grab_text.return_value = "Test Speaker Close caption has started. Real text here"
        
        result = self.capture.get_transcript_to_translate(5.0)
        
        self.assertEqual(result, "Real text here")
    
    def test_mark_as_translated(self):
        """Test marking text as translated."""
        text = "Test text"
        
        self.capture.mark_as_translated(text)
        
        self.assertIn(text, self.capture.already_translated)
    
    def test_mark_as_translated_empty_text(self):
        """Test marking empty text as translated."""
        initial_size = len(self.capture.already_translated)
        
        self.capture.mark_as_translated("")
        
        # Should not add empty text
        self.assertEqual(len(self.capture.already_translated), initial_size)
    
    def test_reset_translation_cache(self):
        """Test resetting translation cache."""
        # Add some data to cache
        self.capture.already_translated.add("Test")
        self.capture.prev_translated_complete_line = "Test line"
        
        self.capture.reset_translation_cache()
        
        # Cache should be cleared
        self.assertEqual(len(self.capture.already_translated), 0)
        self.assertEqual(self.capture.prev_translated_complete_line, "")


if __name__ == '__main__':
    unittest.main()