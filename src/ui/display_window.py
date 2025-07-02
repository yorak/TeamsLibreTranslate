"""Display window module for showing translations."""

import tkinter as tk
from tkinter import font
import logging
from typing import Optional, Callable
from screeninfo import get_monitors
from ..config.settings import UIConfig


class TranslationDisplayWindow:
    """Main display window for showing translations."""
    
    def __init__(self, config: UIConfig, update_callback: Optional[Callable] = None):
        self.config = config
        self.update_callback = update_callback
        self.logger = logging.getLogger(__name__)
        self.root = None
        self.label = None
        self.is_running = False
    
    def get_screen_size(self) -> tuple[int, int]:
        """Get the size for the display window based on screen configuration."""
        monitors = get_monitors()
        
        if len(monitors) > self.config.screen_index:
            monitor = monitors[self.config.screen_index]
            width = int(monitor.width * self.config.window_width_ratio)
            height = int(monitor.height * self.config.window_height_ratio)
            return width, height
        else:
            self.logger.warning(f"Monitor {self.config.screen_index} not detected, using default size")
            return 600, 200
    
    def create_window(self):
        """Create and configure the main display window."""
        self.root = tk.Tk()
        self.root.title("Teams Translator")
        
        # Set window size
        width, height = self.get_screen_size()
        self.root.geometry(f"{width}x{height}")
        
        # Set window to always be on top
        self.root.attributes('-topmost', True)
        
        # Create font
        display_font = font.Font(
            family=self.config.font_family,
            size=self.config.font_size,
            weight=self.config.font_weight
        )
        
        # Create label for displaying translations
        self.label = tk.Label(
            self.root,
            text="",
            font=display_font,
            wraplength=width,
            justify=tk.LEFT
        )
        self.label.pack(expand=True, fill=tk.BOTH)
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.logger.info(f"Created display window: {width}x{height}")
    
    def update_text(self, text: str):
        """Update the displayed text."""
        if self.label:
            self.label.config(text=text)
    
    def start_countdown(self, seconds: int, on_complete: Callable):
        """Start countdown before beginning translation."""
        self.is_running = True
        self._countdown_recursive(seconds, on_complete)
    
    def _countdown_recursive(self, count: int, on_complete: Callable):
        """Recursive countdown implementation."""
        if not self.is_running:
            return
        
        if count > 0:
            self.update_text(f"Starting in {count} seconds...")
            self.root.after(1000, lambda: self._countdown_recursive(count - 1, on_complete))
        else:
            self.update_text("Starting translation...")
            on_complete()
    
    def start_translation_updates(self, update_interval_ms: int):
        """Start the translation update loop."""
        if not self.is_running:
            return
        
        if self.update_callback:
            translation = self.update_callback()
            if translation:
                self.update_text(translation)
        
        self.root.after(update_interval_ms, lambda: self.start_translation_updates(update_interval_ms))
    
    def on_closing(self):
        """Handle window closing event."""
        self.is_running = False
        if self.root:
            self.root.destroy()
        self.logger.info("Display window closed")
    
    def run(self):
        """Start the main event loop."""
        if self.root:
            self.logger.info("Starting display window main loop")
            self.root.mainloop()
        else:
            self.logger.error("Window not created. Call create_window() first.")
    
    def stop(self):
        """Stop the display window."""
        self.is_running = False
        if self.root:
            self.root.quit()