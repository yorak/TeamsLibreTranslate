"""Unit tests for configuration management."""

import unittest
import json
import tempfile
import os
from src.config.settings import AppConfig, TranslationConfig, UIConfig, CaptureConfig


class TestAppConfig(unittest.TestCase):
    """Test cases for AppConfig class."""
    
    def test_default_config_creation(self):
        """Test creating config with default values."""
        config = AppConfig()
        
        # Check that all sub-configs are created
        self.assertIsInstance(config.translation, TranslationConfig)
        self.assertIsInstance(config.ui, UIConfig)
        self.assertIsInstance(config.capture, CaptureConfig)
        
        # Check some default values
        self.assertEqual(config.translation.libretranslate_url, "http://localhost:5000/translate")
        self.assertEqual(config.translation.source_language, "fi")
        self.assertEqual(config.translation.target_language, "en")
        self.assertEqual(config.ui.screen_index, 1)
        self.assertEqual(config.ui.wait_start_time, 10)
    
    def test_from_dict_full_config(self):
        """Test creating config from complete dictionary."""
        config_dict = {
            "translation": {
                "libretranslate_url": "http://custom.example.com/translate",
                "api_key": "custom_key",
                "source_language": "de",
                "target_language": "fr",
                "rate_delay": 2.0,
                "translate_always_after": 10.0
            },
            "ui": {
                "screen_index": 0,
                "wait_start_time": 5,
                "window_width_ratio": 0.5,
                "window_height_ratio": 0.3,
                "font_family": "Arial",
                "font_size": 24,
                "font_weight": "normal"
            },
            "capture": {
                "split_marker": "Custom Speaker",
                "clipboard_delay": 1.0,
                "selection_delay": 0.3
            }
        }
        
        config = AppConfig.from_dict(config_dict)
        
        # Check translation config
        self.assertEqual(config.translation.libretranslate_url, "http://custom.example.com/translate")
        self.assertEqual(config.translation.api_key, "custom_key")
        self.assertEqual(config.translation.source_language, "de")
        self.assertEqual(config.translation.target_language, "fr")
        self.assertEqual(config.translation.rate_delay, 2.0)
        self.assertEqual(config.translation.translate_always_after, 10.0)
        
        # Check UI config
        self.assertEqual(config.ui.screen_index, 0)
        self.assertEqual(config.ui.wait_start_time, 5)
        self.assertEqual(config.ui.window_width_ratio, 0.5)
        self.assertEqual(config.ui.window_height_ratio, 0.3)
        self.assertEqual(config.ui.font_family, "Arial")
        self.assertEqual(config.ui.font_size, 24)
        self.assertEqual(config.ui.font_weight, "normal")
        
        # Check capture config
        self.assertEqual(config.capture.split_marker, "Custom Speaker")
        self.assertEqual(config.capture.clipboard_delay, 1.0)
        self.assertEqual(config.capture.selection_delay, 0.3)
    
    def test_from_dict_partial_config(self):
        """Test creating config from partial dictionary."""
        config_dict = {
            "translation": {
                "source_language": "es",
                "target_language": "en"
            },
            "ui": {
                "screen_index": 2
            }
        }
        
        config = AppConfig.from_dict(config_dict)
        
        # Check overridden values
        self.assertEqual(config.translation.source_language, "es")
        self.assertEqual(config.translation.target_language, "en")
        self.assertEqual(config.ui.screen_index, 2)
        
        # Check default values are preserved
        self.assertEqual(config.translation.libretranslate_url, "http://localhost:5000/translate")
        self.assertEqual(config.ui.wait_start_time, 10)
        self.assertEqual(config.capture.split_marker, "Jussi Rasku (TAU)")
    
    def test_from_dict_empty_config(self):
        """Test creating config from empty dictionary."""
        config = AppConfig.from_dict({})
        
        # Should use all defaults
        self.assertEqual(config.translation.libretranslate_url, "http://localhost:5000/translate")
        self.assertEqual(config.ui.screen_index, 1)
        self.assertEqual(config.capture.split_marker, "Jussi Rasku (TAU)")
    
    def test_from_dict_invalid_keys(self):
        """Test creating config with invalid keys."""
        config_dict = {
            "translation": {
                "invalid_key": "value",
                "source_language": "fi"
            }
        }
        
        config = AppConfig.from_dict(config_dict)
        
        # Valid keys should be set
        self.assertEqual(config.translation.source_language, "fi")
        
        # Invalid keys should be ignored (no error)
        self.assertFalse(hasattr(config.translation, "invalid_key"))
    
    def test_save_and_load_file(self):
        """Test saving and loading configuration file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            # Create config and modify some values
            config = AppConfig()
            config.translation.source_language = "de"
            config.translation.target_language = "en"
            config.ui.screen_index = 2
            config.capture.split_marker = "Test Speaker"
            
            # Save to file
            config.save_to_file(temp_path)
            
            # Load from file
            loaded_config = AppConfig.load_from_file(temp_path)
            
            # Check that values were preserved
            self.assertEqual(loaded_config.translation.source_language, "de")
            self.assertEqual(loaded_config.translation.target_language, "en")
            self.assertEqual(loaded_config.ui.screen_index, 2)
            self.assertEqual(loaded_config.capture.split_marker, "Test Speaker")
            
            # Check that defaults are still there
            self.assertEqual(loaded_config.translation.libretranslate_url, "http://localhost:5000/translate")
            self.assertEqual(loaded_config.ui.wait_start_time, 10)
            
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_load_from_nonexistent_file(self):
        """Test loading from non-existent file."""
        config = AppConfig.load_from_file("nonexistent.json")
        
        # Should return default config
        self.assertEqual(config.translation.libretranslate_url, "http://localhost:5000/translate")
        self.assertEqual(config.ui.screen_index, 1)
    
    def test_load_from_invalid_json(self):
        """Test loading from invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_path = f.name
        
        try:
            with self.assertRaises(json.JSONDecodeError):
                AppConfig.load_from_file(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_config_file_format(self):
        """Test that saved config file has correct format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            config = AppConfig()
            config.save_to_file(temp_path)
            
            # Read and parse the file
            with open(temp_path, 'r') as f:
                saved_data = json.load(f)
            
            # Check structure
            self.assertIn("translation", saved_data)
            self.assertIn("ui", saved_data)
            self.assertIn("capture", saved_data)
            
            # Check translation section
            translation = saved_data["translation"]
            self.assertIn("libretranslate_url", translation)
            self.assertIn("api_key", translation)
            self.assertIn("source_language", translation)
            self.assertIn("target_language", translation)
            self.assertIn("rate_delay", translation)
            self.assertIn("translate_always_after", translation)
            
            # Check UI section
            ui = saved_data["ui"]
            self.assertIn("screen_index", ui)
            self.assertIn("wait_start_time", ui)
            self.assertIn("window_width_ratio", ui)
            self.assertIn("window_height_ratio", ui)
            self.assertIn("font_family", ui)
            self.assertIn("font_size", ui)
            self.assertIn("font_weight", ui)
            
            # Check capture section
            capture = saved_data["capture"]
            self.assertIn("split_marker", capture)
            self.assertIn("clipboard_delay", capture)
            self.assertIn("selection_delay", capture)
            
        finally:
            os.unlink(temp_path)


class TestTranslationConfig(unittest.TestCase):
    """Test cases for TranslationConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = TranslationConfig()
        
        self.assertEqual(config.libretranslate_url, "http://localhost:5000/translate")
        self.assertEqual(config.api_key, "")
        self.assertEqual(config.source_language, "fi")
        self.assertEqual(config.target_language, "en")
        self.assertEqual(config.rate_delay, 1.0)
        self.assertEqual(config.translate_always_after, 5.0)


class TestUIConfig(unittest.TestCase):
    """Test cases for UIConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = UIConfig()
        
        self.assertEqual(config.screen_index, 1)
        self.assertEqual(config.wait_start_time, 10)
        self.assertEqual(config.window_width_ratio, 5/6)
        self.assertEqual(config.window_height_ratio, 1/5)
        self.assertEqual(config.font_family, "Helvetica")
        self.assertEqual(config.font_size, 20)
        self.assertEqual(config.font_weight, "bold")


class TestCaptureConfig(unittest.TestCase):
    """Test cases for CaptureConfig."""
    
    def test_default_values(self):
        """Test default configuration values."""
        config = CaptureConfig()
        
        self.assertEqual(config.split_marker, "Jussi Rasku (TAU)")
        self.assertEqual(config.clipboard_delay, 0.5)
        self.assertEqual(config.selection_delay, 0.2)


if __name__ == '__main__':
    unittest.main()