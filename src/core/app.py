"""Main application module."""

import logging
import sys
from typing import Optional, Dict
from ..config.settings import AppConfig
from ..core.translator import TranslationService
from ..core.text_capture import TextCapture
from ..ui.display_window import TranslationDisplayWindow


class TeamsTranslatorApp:
    """Main application class for Teams Translator."""
    
    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig()
        self.logger = self._setup_logging()
        
        # Initialize services
        self.translation_service = TranslationService(self.config.translation)
        self.text_capture = TextCapture(self.config.capture)
        self.display_window = TranslationDisplayWindow(self.config.ui, self.grab_and_translate)
        
        # Translation cache
        self.translation_cache: Dict[str, str] = {}
        
        self.logger.info("Teams Translator initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('teams_translator.log')
            ]
        )
        return logging.getLogger(__name__)
    
    def grab_and_translate(self) -> Optional[str]:
        """
        Grab text from screen and translate it.
        
        Returns:
            Translated text or None if no translation needed
        """
        try:
            text_to_translate = self.text_capture.get_transcript_to_translate(
                self.config.translation.translate_always_after
            )
            
            if not text_to_translate:
                return None
            
            self.logger.info(f"Text to translate: {text_to_translate[:100]}...")
            
            # Check cache first
            if text_to_translate in self.translation_cache:
                self.logger.debug("Using cached translation")
                return self.translation_cache[text_to_translate]
            
            # Translate
            translation = self.translation_service.translate(text_to_translate)
            
            if translation:
                # Cache the translation
                self.translation_cache[text_to_translate] = translation
                self.text_capture.mark_as_translated(text_to_translate)
                
                self.logger.info(f"Translation: {translation}")
                return translation
            else:
                self.logger.warning("Translation failed")
                return None
                
        except Exception as e:
            self.logger.error(f"Error in grab_and_translate: {e}")
            return None
    
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met."""
        if not self.translation_service.is_service_available():
            self.logger.error("LibreTranslate service is not available")
            return False
        
        self.logger.info("All prerequisites met")
        return True
    
    def start_translation_session(self):
        """Start a new translation session."""
        self.logger.info("Starting translation session")
        
        # Reset caches
        self.text_capture.reset_translation_cache()
        self.translation_cache.clear()
        
        # Mark existing text as translated
        self.text_capture.mark_all_previous_translated()
        
        # Start translation updates
        update_interval_ms = int(self.config.translation.rate_delay * 1000)
        self.display_window.start_translation_updates(update_interval_ms)
    
    def run(self):
        """Run the main application."""
        self.logger.info("Starting Teams Translator")
        
        # Check prerequisites
        if not self.check_prerequisites():
            self.logger.error("Prerequisites not met. Exiting.")
            return 1
        
        try:
            # Create and show display window
            self.display_window.create_window()
            
            # Start countdown and then translation
            self.display_window.start_countdown(
                self.config.ui.wait_start_time,
                self.start_translation_session
            )
            
            # Start the main loop
            self.display_window.run()
            
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
            return 0
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            return 1
        
        self.logger.info("Application finished")
        return 0