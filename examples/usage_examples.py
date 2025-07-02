#!/usr/bin/env python3
"""Usage examples for Teams Translator."""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config.settings import AppConfig, TranslationConfig, UIConfig, CaptureConfig
from core.app import TeamsTranslatorApp
from core.translator import TranslationService
from core.text_capture import TextCapture


def example_basic_usage():
    """Example: Basic usage with default configuration."""
    print("Example 1: Basic usage with default configuration")
    
    # Create app with default configuration
    app = TeamsTranslatorApp()
    
    # Run the application
    # app.run()  # Uncomment to actually run
    print("App created with default configuration")


def example_custom_configuration():
    """Example: Custom configuration from code."""
    print("\nExample 2: Custom configuration from code")
    
    # Create custom configuration
    config = AppConfig()
    
    # Modify translation settings
    config.translation.source_language = "de"
    config.translation.target_language = "en"
    config.translation.rate_delay = 2.0
    
    # Modify UI settings
    config.ui.screen_index = 0
    config.ui.font_size = 24
    config.ui.wait_start_time = 5
    
    # Modify capture settings
    config.capture.split_marker = "Hans Schmidt"
    
    # Create app with custom configuration
    app = TeamsTranslatorApp(config)
    print("App created with custom configuration")


def example_config_file():
    """Example: Load configuration from file."""
    print("\nExample 3: Load configuration from file")
    
    # Load configuration from file
    config_path = os.path.join(os.path.dirname(__file__), "config_german_to_english.json")
    config = AppConfig.load_from_file(config_path)
    
    # Create app with loaded configuration
    app = TeamsTranslatorApp(config)
    print(f"App created with configuration from {config_path}")


def example_save_configuration():
    """Example: Save configuration to file."""
    print("\nExample 4: Save configuration to file")
    
    # Create and customize configuration
    config = AppConfig()
    config.translation.source_language = "fr"
    config.translation.target_language = "en"
    config.ui.screen_index = 2
    config.capture.split_marker = "Marie Dubois"
    
    # Save to file
    config_path = "my_custom_config.json"
    config.save_to_file(config_path)
    print(f"Configuration saved to {config_path}")


def example_translation_service():
    """Example: Using translation service directly."""
    print("\nExample 5: Using translation service directly")
    
    # Create translation configuration
    config = TranslationConfig()
    config.libretranslate_url = "http://localhost:5000/translate"
    config.source_language = "fi"
    config.target_language = "en"
    
    # Create translation service
    translator = TranslationService(config)
    
    # Check if service is available
    if translator.is_service_available():
        print("LibreTranslate service is available")
        
        # Example translation
        result = translator.translate("Hei maailma")
        if result:
            print(f"Translation: 'Hei maailma' -> '{result}'")
        else:
            print("Translation failed")
    else:
        print("LibreTranslate service is not available")


def example_text_capture():
    """Example: Using text capture service directly."""
    print("\nExample 6: Using text capture service directly")
    
    # Create capture configuration
    config = CaptureConfig()
    config.split_marker = "Test Speaker"
    config.clipboard_delay = 0.3
    config.selection_delay = 0.1
    
    # Create text capture service
    capture = TextCapture(config)
    
    # Example of marking existing text as translated
    capture.mark_all_previous_translated()
    print("Marked all previous text as translated")
    
    # Example of checking for new text (would normally capture from screen)
    # new_text = capture.get_transcript_to_translate(5.0)
    # if new_text:
    #     print(f"New text to translate: {new_text}")
    # else:
    #     print("No new text to translate")


def example_configuration_sections():
    """Example: Working with configuration sections."""
    print("\nExample 7: Working with configuration sections")
    
    # Create configurations for different sections
    translation_config = TranslationConfig()
    translation_config.libretranslate_url = "https://api.example.com/translate"
    translation_config.api_key = "your_api_key"
    translation_config.source_language = "es"
    translation_config.target_language = "en"
    
    ui_config = UIConfig()
    ui_config.screen_index = 1
    ui_config.font_size = 16
    ui_config.font_family = "Courier New"
    
    capture_config = CaptureConfig()
    capture_config.split_marker = "Juan Pérez"
    capture_config.clipboard_delay = 0.4
    
    # Create main configuration
    config = AppConfig()
    config.translation = translation_config
    config.ui = ui_config
    config.capture = capture_config
    
    print("Configuration created with custom sections")
    print(f"Translation URL: {config.translation.libretranslate_url}")
    print(f"UI Screen: {config.ui.screen_index}")
    print(f"Capture marker: {config.capture.split_marker}")


def example_error_handling():
    """Example: Error handling in translation."""
    print("\nExample 8: Error handling in translation")
    
    # Create configuration with invalid URL
    config = TranslationConfig()
    config.libretranslate_url = "http://invalid.url/translate"
    
    translator = TranslationService(config)
    
    # Check service availability
    if not translator.is_service_available():
        print("Service is not available - handling gracefully")
    
    # Try translation with error handling
    result = translator.translate("Test text")
    if result:
        print(f"Translation successful: {result}")
    else:
        print("Translation failed - handled gracefully")


def example_batch_configuration():
    """Example: Creating multiple configurations for different scenarios."""
    print("\nExample 9: Batch configuration creation")
    
    scenarios = [
        {
            "name": "Finnish to English",
            "source": "fi",
            "target": "en",
            "marker": "Jussi Rasku"
        },
        {
            "name": "German to English",
            "source": "de",
            "target": "en",
            "marker": "Klaus Mueller"
        },
        {
            "name": "Spanish to English",
            "source": "es",
            "target": "en",
            "marker": "María García"
        }
    ]
    
    for scenario in scenarios:
        config = AppConfig()
        config.translation.source_language = scenario["source"]
        config.translation.target_language = scenario["target"]
        config.capture.split_marker = scenario["marker"]
        
        filename = f"config_{scenario['name'].lower().replace(' ', '_')}.json"
        config.save_to_file(filename)
        print(f"Created configuration: {filename}")


def example_environment_specific_config():
    """Example: Environment-specific configuration."""
    print("\nExample 10: Environment-specific configuration")
    
    # Development configuration
    dev_config = AppConfig()
    dev_config.translation.libretranslate_url = "http://localhost:5000/translate"
    dev_config.translation.rate_delay = 0.5  # Faster for development
    dev_config.ui.wait_start_time = 3  # Shorter wait time
    
    # Production configuration
    prod_config = AppConfig()
    prod_config.translation.libretranslate_url = "https://translate.production.com/translate"
    prod_config.translation.api_key = "prod_api_key"
    prod_config.translation.rate_delay = 2.0  # More conservative
    prod_config.ui.wait_start_time = 10  # Standard wait time
    
    print("Development and production configurations created")


if __name__ == "__main__":
    print("Teams Translator - Usage Examples")
    print("=" * 40)
    
    # Run all examples
    example_basic_usage()
    example_custom_configuration()
    example_config_file()
    example_save_configuration()
    example_translation_service()
    example_text_capture()
    example_configuration_sections()
    example_error_handling()
    example_batch_configuration()
    example_environment_specific_config()
    
    print("\n" + "=" * 40)
    print("All examples completed!")