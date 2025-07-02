"""Configuration management for Teams Translator."""

import os
from dataclasses import dataclass
from typing import Dict, Any
import json


@dataclass
class TranslationConfig:
    """Configuration for translation settings."""
    libretranslate_url: str = "http://localhost:5000/translate"
    api_key: str = ""
    source_language: str = "fi"
    target_language: str = "en"
    rate_delay: float = 1.0
    translate_always_after: float = 5.0


@dataclass
class UIConfig:
    """Configuration for UI settings."""
    screen_index: int = 1
    wait_start_time: int = 10
    window_width_ratio: float = 5/6
    window_height_ratio: float = 1/5
    font_family: str = "Helvetica"
    font_size: int = 20
    font_weight: str = "bold"


@dataclass
class CaptureConfig:
    """Configuration for text capture settings."""
    split_marker: str = "Jussi Rasku (TAU)"
    clipboard_delay: float = 0.5
    selection_delay: float = 0.2


@dataclass
class AppConfig:
    """Main application configuration."""
    translation: TranslationConfig
    ui: UIConfig
    capture: CaptureConfig
    
    def __init__(self):
        self.translation = TranslationConfig()
        self.ui = UIConfig()
        self.capture = CaptureConfig()
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'AppConfig':
        """Create configuration from dictionary."""
        instance = cls()
        
        if 'translation' in config_dict:
            for key, value in config_dict['translation'].items():
                if hasattr(instance.translation, key):
                    setattr(instance.translation, key, value)
        
        if 'ui' in config_dict:
            for key, value in config_dict['ui'].items():
                if hasattr(instance.ui, key):
                    setattr(instance.ui, key, value)
        
        if 'capture' in config_dict:
            for key, value in config_dict['capture'].items():
                if hasattr(instance.capture, key):
                    setattr(instance.capture, key, value)
        
        return instance
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'AppConfig':
        """Load configuration from JSON file."""
        if not os.path.exists(config_path):
            return cls()
        
        with open(config_path, 'r') as f:
            config_dict = json.load(f)
        
        return cls.from_dict(config_dict)
    
    def save_to_file(self, config_path: str):
        """Save configuration to JSON file."""
        config_dict = {
            'translation': {
                'libretranslate_url': self.translation.libretranslate_url,
                'api_key': self.translation.api_key,
                'source_language': self.translation.source_language,
                'target_language': self.translation.target_language,
                'rate_delay': self.translation.rate_delay,
                'translate_always_after': self.translation.translate_always_after
            },
            'ui': {
                'screen_index': self.ui.screen_index,
                'wait_start_time': self.ui.wait_start_time,
                'window_width_ratio': self.ui.window_width_ratio,
                'window_height_ratio': self.ui.window_height_ratio,
                'font_family': self.ui.font_family,
                'font_size': self.ui.font_size,
                'font_weight': self.ui.font_weight
            },
            'capture': {
                'split_marker': self.capture.split_marker,
                'clipboard_delay': self.capture.clipboard_delay,
                'selection_delay': self.capture.selection_delay
            }
        }
        
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)