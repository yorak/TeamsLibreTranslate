# Examples

This directory contains example configurations and usage patterns for Teams Translator.

## Configuration Examples

### `config_finnish_to_english.json`
Default configuration for Finnish to English translation. This is the most common use case and matches the original script's behavior.

**Key settings:**
- Source language: Finnish (fi)
- Target language: English (en)
- Split marker: "Jussi Rasku (TAU)"
- Standard timing and display settings

### `config_german_to_english.json`
Configuration for German to English translation with customized settings.

**Key settings:**
- Source language: German (de)
- Target language: English (en)
- Split marker: "Klaus Mueller"
- Faster translation rate (1.5s delay)
- Primary screen (index 0)
- Smaller font size (18)

### `config_remote_server.json`
Configuration for using a remote LibreTranslate server with API key authentication.

**Key settings:**
- Remote server URL with HTTPS
- API key authentication
- Auto-detect source language
- Longer delays for network latency
- Larger display window
- Extended startup time (15s)

## Usage Examples

### `usage_examples.py`
Comprehensive Python script demonstrating various usage patterns:

1. **Basic usage** - Default configuration
2. **Custom configuration** - Programmatic configuration
3. **Config file loading** - Loading from JSON files
4. **Config file saving** - Saving custom configurations
5. **Direct service usage** - Using translation service independently
6. **Text capture usage** - Using text capture service independently
7. **Configuration sections** - Working with individual config sections
8. **Error handling** - Graceful error handling patterns
9. **Batch configurations** - Creating multiple configurations
10. **Environment-specific** - Different configs for dev/prod

## Running the Examples

### Run Usage Examples
```bash
cd examples
python usage_examples.py
```

### Use Configuration Files
```bash
# Finnish to English
python ../main.py --config config_finnish_to_english.json

# German to English
python ../main.py --config config_german_to_english.json

# Remote server
python ../main.py --config config_remote_server.json
```

### Create Custom Configuration
```bash
# Create a default configuration file
python ../main.py --create-config my_config.json

# Edit my_config.json as needed, then use it
python ../main.py --config my_config.json
```

## Configuration Tips

### Language Codes
Use ISO 639-1 language codes:
- `fi` - Finnish
- `en` - English
- `de` - German
- `es` - Spanish
- `fr` - French
- `auto` - Auto-detect (requires LibreTranslate support)

### Split Markers
The split marker should match the name that appears in your Teams captions. Common patterns:
- "FirstName LastName (Organization)"
- "FirstName LastName"
- "username"

### Screen Selection
- `0` - Primary screen
- `1` - Secondary screen
- `2` - Third screen (if available)

### Timing Settings
- `rate_delay` - Time between translation requests (seconds)
- `translate_always_after` - Force translation after this time (seconds)
- `wait_start_time` - Countdown before starting (seconds)

### Display Settings
- `window_width_ratio` - Window width as fraction of screen width (0.0-1.0)
- `window_height_ratio` - Window height as fraction of screen height (0.0-1.0)
- `font_size` - Font size in points
- `font_family` - Font family name ("Helvetica", "Arial", "Times", etc.)

### API Settings
- `libretranslate_url` - LibreTranslate API endpoint
- `api_key` - API key for authentication (if required)

## Troubleshooting Common Issues

### Wrong Split Marker
If translations aren't appearing, check that your split marker matches exactly what appears in Teams captions.

### LibreTranslate Connection
Test your LibreTranslate connection:
```bash
curl -X POST "http://localhost:5000/translate" \
  -H "Content-Type: application/json" \
  -d '{"q": "Hello", "source": "en", "target": "fi"}'
```

### Display Issues
- Try different screen indices (0, 1, 2)
- Adjust window ratios if the window is too small/large
- Check font family availability on your system

### Performance Tuning
- Increase `rate_delay` if API requests are too frequent
- Decrease `translate_always_after` for more responsive incomplete line translation
- Adjust clipboard delays if text capture is unreliable