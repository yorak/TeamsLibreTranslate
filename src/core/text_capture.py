"""Text capture module for grabbing text from screen."""

import pyautogui
import pyperclip
import time
import logging
from typing import Optional, Dict, Set
from ..config.settings import CaptureConfig


class TextCapture:
    """Handles text capture from screen using clipboard operations."""
    
    def __init__(self, config: CaptureConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.already_translated: Set[str] = set()
        self.prev_translated_complete_line: str = ""
        self.prev_translation_at: float = time.time()
    
    def grab_text(self) -> str:
        """
        Grab text from current window by selecting all and copying to clipboard.
        
        Returns:
            Text from clipboard
        """
        try:
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(self.config.selection_delay)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(self.config.clipboard_delay)
            
            return pyperclip.paste()
        except Exception as e:
            self.logger.error(f"Failed to grab text: {e}")
            return ""
    
    def mark_all_previous_translated(self):
        """Mark all existing text as already translated."""
        copied_text = self.grab_text()
        all_past_text = [p.strip() for p in copied_text.split(self.config.split_marker)]
        
        for text in all_past_text:
            if text:
                self.already_translated.add(text)
        
        if all_past_text:
            self.prev_translated_complete_line = all_past_text[-1]
        self.prev_translation_at = time.time()
        
        self.logger.info(f"Marked {len(all_past_text)} previous texts as translated")
    
    def get_transcript_to_translate(self, translate_always_after: float) -> Optional[str]:
        """
        Extract new text that needs translation.
        
        Args:
            translate_always_after: Time in seconds after which to always translate incomplete lines
            
        Returns:
            Text to translate or None if no new text
        """
        copied_text = self.grab_text()
        split_pos = copied_text.rfind(self.config.split_marker)
        
        if split_pos < 0:
            return None
        
        # Extract the incomplete line after the split marker
        new_incomplete_line = copied_text[split_pos + len(self.config.split_marker):] \
            .replace("Close caption has started.", "").strip()
        
        # Find the previous complete line
        prev_split_pos = copied_text.rfind(self.config.split_marker, 0, split_pos)
        if prev_split_pos < 0:
            new_prev_complete_line = ""
        elif prev_split_pos + len(self.config.split_marker) < split_pos:
            new_prev_complete_line = copied_text[prev_split_pos + len(self.config.split_marker):split_pos].strip()
        else:
            new_prev_complete_line = ""
        
        # Check what needs translation
        prev_line_changed = new_prev_complete_line != self.prev_translated_complete_line
        prev_already_translated = new_prev_complete_line in self.already_translated
        incomplete_already_translated = new_incomplete_line in self.already_translated
        time_to_translate_incomplete = (time.time() - self.prev_translation_at) > translate_always_after
        
        # Decide what to translate
        if prev_line_changed and not prev_already_translated and new_prev_complete_line:
            self.prev_translated_complete_line = new_prev_complete_line
            self.prev_translation_at = time.time()
            self.logger.debug(f"Translating complete line: {new_prev_complete_line[:50]}...")
            return new_prev_complete_line
        elif not incomplete_already_translated and time_to_translate_incomplete and new_incomplete_line:
            self.prev_translation_at = time.time()
            self.logger.debug(f"Translating incomplete line: {new_incomplete_line[:50]}...")
            return new_incomplete_line
        else:
            return None
    
    def mark_as_translated(self, text: str):
        """Mark text as already translated."""
        if text:
            self.already_translated.add(text)
    
    def reset_translation_cache(self):
        """Reset the translation cache."""
        self.already_translated.clear()
        self.prev_translated_complete_line = ""
        self.prev_translation_at = time.time()
        self.logger.info("Translation cache reset")