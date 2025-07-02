# Teams Translator

A real-time translation tool for Microsoft Teams meetings that captures live captions and translates them using LibreTranslate.

![Teams Translator Screenshot](docs/fake_screenshot.png)

## Features

- **Real-time Translation**: Automatically captures and translates text from Teams meetings
- **Configurable Languages**: Support for multiple source and target languages
- **Overlay Display**: Shows translations in an always-on-top window
- **Smart Caching**: Avoids re-translating the same text
- **Modular Architecture**: Clean, maintainable code structure
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## Prerequisites

1. **LibreTranslate Server**: You need a running LibreTranslate instance
   ```bash
   # Install LibreTranslate
   pip install libretranslate
   
   # Start with specific languages (example: Finnish and English)
   libretranslate --load-only fi,en --update-models
   ```

2. **Python Dependencies**: See `requirements.txt`

## Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a configuration file:
   ```bash
   python main.py --create-config
   ```

## Usage

### Basic Usage

```bash
# Start with default settings
python main.py

# Specify languages
python main.py --source-lang fi --target-lang en

# Use custom LibreTranslate URL
python main.py --libretranslate-url http://your-server:5000/translate

# Use different screen for display
python main.py --screen 0
```

### Configuration

The application uses a JSON configuration file (`config.json` by default):

```json
{
  "translation": {
    "libretranslate_url": "http://localhost:5000/translate",
    "api_key": "",
    "source_language": "fi",
    "target_language": "en",
    "rate_delay": 1.0,
    "translate_always_after": 5.0
  },
  "ui": {
    "screen_index": 1,
    "wait_start_time": 10,
    "window_width_ratio": 0.8333333333333334,
    "window_height_ratio": 0.2,
    "font_family": "Helvetica",
    "font_size": 20,
    "font_weight": "bold"
  },
  "capture": {
    "split_marker": "Jussi Rasku (TAU)",
    "clipboard_delay": 0.5,
    "selection_delay": 0.2
  }
}
```

### Configuration Parameters

#### Translation Settings
- `libretranslate_url`: LibreTranslate API endpoint
- `api_key`: API key for LibreTranslate (if required)
- `source_language`: Source language code (e.g., 'fi', 'en')
- `target_language`: Target language code
- `rate_delay`: Delay between translation requests (seconds)
- `translate_always_after`: Force translation after this many seconds

#### UI Settings
- `screen_index`: Which monitor to display the translation window
- `wait_start_time`: Countdown before starting translation
- `window_width_ratio`: Window width as ratio of screen width
- `window_height_ratio`: Window height as ratio of screen height
- `font_family`: Font family for display
- `font_size`: Font size for display
- `font_weight`: Font weight (normal, bold)

#### Capture Settings
- `split_marker`: Text marker to identify speaker changes
- `clipboard_delay`: Delay after clipboard operations
- `selection_delay`: Delay after text selection

## How It Works

1. **Text Capture**: The application captures text from the active window using clipboard operations
2. **Text Processing**: Identifies new text that needs translation by looking for speaker markers
3. **Translation**: Sends text to LibreTranslate API for translation
4. **Display**: Shows translated text in an overlay window
5. **Caching**: Remembers translated text to avoid duplicate API calls

## Architecture

The application follows a modular architecture:

```
src/
├── config/          # Configuration management
├── core/           # Core business logic
│   ├── app.py      # Main application
│   ├── translator.py    # Translation service
│   └── text_capture.py  # Text capture logic
├── ui/             # User interface
│   └── display_window.py   # Translation display window
└── utils/          # Utility functions
```

For detailed architecture documentation, see:
- [Architecture Overview](docs/architecture.md) - System design and component details
- [API Documentation](docs/api.md) - Class interfaces and usage examples
- [System Diagrams](docs/diagrams/) - Visual system architecture and data flow diagrams

## Command Line Options

- `--config`: Path to configuration file
- `--source-lang`: Source language code
- `--target-lang`: Target language code
- `--screen`: Screen index for display window
- `--libretranslate-url`: LibreTranslate API URL
- `--create-config`: Create default configuration file

## Troubleshooting

### Common Issues

1. **LibreTranslate not available**
   - Ensure LibreTranslate is running on the specified URL
   - Check if the required language models are loaded

2. **Text not being captured**
   - Verify the split marker matches your Teams username
   - Check if the application has permission to access clipboard

3. **Translation window not visible**
   - Try different screen index values
   - Check if the window is minimized or behind other windows

### Logging

The application logs to both console and `teams_translator.log` file. Check logs for detailed error information.

## Development

### Project Structure

```
teams-translator/
├── src/                    # Source code
│   ├── config/            # Configuration management
│   ├── core/              # Core business logic
│   ├── ui/                # User interface components
│   └── utils/             # Utility functions
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── examples/              # Example configurations
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── setup.py             # Package setup
```

### Running Tests

```bash
python -m pytest tests/
```

## Funding and Acknowledgments

This project was created as part of the GPT-Lab Seinäjoki project, co-financed by the AKKE instrument of Regional Council of South Ostrobothnia.

<img src="EPLiitto_logo_cropped.jpg" alt="Regional Council of South Ostrobothnia" width="200"/>

## License

This project is open source. See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions, please use the project's issue tracker.