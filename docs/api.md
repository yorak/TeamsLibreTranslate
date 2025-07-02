# API Documentation

## Core Classes and Methods

### TeamsTranslatorApp

Main application class that orchestrates the translation workflow.

#### Constructor

```python
TeamsTranslatorApp(config: Optional[AppConfig] = None)
```

**Parameters:**
- `config`: Application configuration object. If None, defaults will be used.

#### Methods

##### `grab_and_translate() -> Optional[str]`

Captures text from screen and translates it if necessary.

**Returns:**
- `str`: Translated text if translation was performed
- `None`: If no translation was needed

**Raises:**
- `Exception`: For capture or translation errors

##### `check_prerequisites() -> bool`

Verifies that all required services are available.

**Returns:**
- `bool`: True if all prerequisites are met

##### `start_translation_session()`

Initializes a new translation session by resetting caches and marking existing text as translated.

##### `run() -> int`

Runs the main application loop.

**Returns:**
- `int`: Exit code (0 for success, 1 for error)

---

### TranslationService

Handles communication with LibreTranslate API.

#### Constructor

```python
TranslationService(config: TranslationConfig)
```

**Parameters:**
- `config`: Translation configuration object

#### Methods

##### `translate(text: str, source_lang: Optional[str] = None, target_lang: Optional[str] = None) -> Optional[str]`

Translates text using LibreTranslate API.

**Parameters:**
- `text`: Text to translate
- `source_lang`: Source language code (optional, uses config default)
- `target_lang`: Target language code (optional, uses config default)

**Returns:**
- `str`: Translated text
- `None`: If translation failed

**Raises:**
- `requests.exceptions.RequestException`: For network errors
- `json.JSONDecodeError`: For response parsing errors

##### `is_service_available() -> bool`

Checks if LibreTranslate service is available.

**Returns:**
- `bool`: True if service is accessible

---

### TextCapture

Handles text capture and change detection.

#### Constructor

```python
TextCapture(config: CaptureConfig)
```

**Parameters:**
- `config`: Capture configuration object

#### Methods

##### `grab_text() -> str`

Captures text from the active window using clipboard operations.

**Returns:**
- `str`: Captured text

**Raises:**
- `Exception`: For clipboard or screen capture errors

##### `get_transcript_to_translate(translate_always_after: float) -> Optional[str]`

Determines what text needs translation based on change detection.

**Parameters:**
- `translate_always_after`: Time in seconds to force translation of incomplete lines

**Returns:**
- `str`: Text that needs translation
- `None`: If no translation is needed

##### `mark_all_previous_translated()`

Marks all existing captured text as already translated.

##### `mark_as_translated(text: str)`

Marks specific text as translated.

**Parameters:**
- `text`: Text to mark as translated

##### `reset_translation_cache()`

Resets the translation cache and tracking state.

---

### TranslationDisplayWindow

Manages the translation display window.

#### Constructor

```python
TranslationDisplayWindow(config: UIConfig, update_callback: Optional[Callable] = None)
```

**Parameters:**
- `config`: UI configuration object
- `update_callback`: Function to call for translation updates

#### Methods

##### `create_window()`

Creates and configures the display window.

##### `update_text(text: str)`

Updates the displayed translation text.

**Parameters:**
- `text`: Text to display

##### `start_countdown(seconds: int, on_complete: Callable)`

Starts countdown timer before beginning translation.

**Parameters:**
- `seconds`: Countdown duration
- `on_complete`: Function to call when countdown completes

##### `start_translation_updates(update_interval_ms: int)`

Starts the translation update loop.

**Parameters:**
- `update_interval_ms`: Update interval in milliseconds

##### `run()`

Starts the main UI event loop.

##### `stop()`

Stops the display window and event loop.

---

### AppConfig

Configuration management class with support for JSON files.

#### Constructor

```python
AppConfig()
```

Creates configuration with default values.

#### Class Methods

##### `from_dict(config_dict: Dict[str, Any]) -> AppConfig`

Creates configuration from dictionary.

**Parameters:**
- `config_dict`: Configuration dictionary

**Returns:**
- `AppConfig`: Configuration object

##### `load_from_file(config_path: str) -> AppConfig`

Loads configuration from JSON file.

**Parameters:**
- `config_path`: Path to configuration file

**Returns:**
- `AppConfig`: Configuration object

#### Instance Methods

##### `save_to_file(config_path: str)`

Saves configuration to JSON file.

**Parameters:**
- `config_path`: Path to save configuration file

---

## Configuration Schema

### TranslationConfig

Translation service configuration.

```python
@dataclass
class TranslationConfig:
    libretranslate_url: str = "http://localhost:5000/translate"
    api_key: str = ""
    source_language: str = "fi"
    target_language: str = "en"
    rate_delay: float = 1.0
    translate_always_after: float = 5.0
```

### UIConfig

User interface configuration.

```python
@dataclass
class UIConfig:
    screen_index: int = 1
    wait_start_time: int = 10
    window_width_ratio: float = 5/6
    window_height_ratio: float = 1/5
    font_family: str = "Helvetica"
    font_size: int = 20
    font_weight: str = "bold"
```

### CaptureConfig

Text capture configuration.

```python
@dataclass
class CaptureConfig:
    split_marker: str = "Jussi Rasku (TAU)"
    clipboard_delay: float = 0.5
    selection_delay: float = 0.2
```

## Error Handling

### Exception Types

The application handles several types of exceptions:

#### Translation Errors
- `requests.exceptions.RequestException`: Network connectivity issues
- `json.JSONDecodeError`: API response parsing errors
- `TimeoutError`: API request timeouts

#### Capture Errors
- `Exception`: Generic clipboard or screen capture errors
- `PermissionError`: Clipboard access denied

#### Configuration Errors
- `FileNotFoundError`: Configuration file not found
- `json.JSONDecodeError`: Configuration file parsing errors
- `ValueError`: Invalid configuration values

### Error Handling Pattern

```python
try:
    # Operation that might fail
    result = risky_operation()
except SpecificException as e:
    # Log the error
    logger.error(f"Specific error occurred: {e}")
    # Handle gracefully
    return default_value
except Exception as e:
    # Log unexpected errors
    logger.error(f"Unexpected error: {e}")
    # Re-raise or handle as appropriate
    raise
```

## Usage Examples

### Basic Usage

```python
from src.config.settings import AppConfig
from src.core.app import TeamsTranslatorApp

# Create configuration
config = AppConfig()
config.translation.source_language = "fi"
config.translation.target_language = "en"

# Create and run application
app = TeamsTranslatorApp(config)
exit_code = app.run()
```

### Custom Configuration

```python
from src.config.settings import AppConfig, TranslationConfig

# Load configuration from file
config = AppConfig.load_from_file("my_config.json")

# Modify configuration
config.translation.libretranslate_url = "http://my-server:5000/translate"
config.ui.screen_index = 0

# Save modified configuration
config.save_to_file("my_config.json")

# Use configuration
app = TeamsTranslatorApp(config)
app.run()
```

### Manual Translation

```python
from src.core.translator import TranslationService
from src.config.settings import TranslationConfig

# Create translation service
config = TranslationConfig()
translator = TranslationService(config)

# Check service availability
if translator.is_service_available():
    # Translate text
    result = translator.translate("Hei maailma", "fi", "en")
    print(result)  # "Hello world"
```

### Custom Text Capture

```python
from src.core.text_capture import TextCapture
from src.config.settings import CaptureConfig

# Create capture service
config = CaptureConfig()
config.split_marker = "Your Name"
capture = TextCapture(config)

# Mark existing text as translated
capture.mark_all_previous_translated()

# Get new text to translate
new_text = capture.get_transcript_to_translate(5.0)
if new_text:
    print(f"New text: {new_text}")
```

## Integration Points

### Custom Translation Services

To integrate a different translation service:

1. Create a new service class implementing the same interface as `TranslationService`
2. Update the `TeamsTranslatorApp` to use your service
3. Modify configuration to include your service settings

### Custom UI Components

To use a different UI framework:

1. Create a new display class implementing the same interface as `TranslationDisplayWindow`
2. Update the `TeamsTranslatorApp` to use your display class
3. Ensure proper callback integration

### Configuration Extensions

To add new configuration options:

1. Extend the appropriate configuration dataclass
2. Update the `from_dict` and `save_to_file` methods
3. Add command-line argument support in `main.py`