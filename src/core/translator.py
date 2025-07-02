"""Translation service module."""

import requests
import json
import logging
from typing import Optional, Dict, Any
from ..config.settings import TranslationConfig


class TranslationService:
    """Service for handling text translation via LibreTranslate API."""
    
    def __init__(self, config: TranslationConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def translate(self, text: str, source_lang: Optional[str] = None, target_lang: Optional[str] = None) -> Optional[str]:
        """
        Translate text using LibreTranslate API.
        
        Args:
            text: Text to translate
            source_lang: Source language code (defaults to config)
            target_lang: Target language code (defaults to config)
            
        Returns:
            Translated text or None if translation failed
        """
        if not text.strip():
            return None
        
        source_lang = source_lang or self.config.source_language
        target_lang = target_lang or self.config.target_language
        
        data = {
            "q": text,
            "source": source_lang,
            "target": target_lang,
            "format": "text",
            "api_key": self.config.api_key
        }
        
        try:
            response = requests.post(
                self.config.libretranslate_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                payload = response.json()
                self.logger.debug(f"Translation response: {payload}")
                return payload.get("translatedText")
            else:
                self.logger.error(f"Translation failed with status {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Translation request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse translation response: {e}")
            return None
    
    def is_service_available(self) -> bool:
        """Check if LibreTranslate service is available."""
        try:
            response = requests.get(
                self.config.libretranslate_url.replace("/translate", "/languages"),
                timeout=5
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False