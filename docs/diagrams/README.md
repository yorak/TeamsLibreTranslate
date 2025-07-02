# Architecture Diagrams

This directory contains PlantUML diagrams that visualize the Teams Translator architecture and workflows.

## Generated Diagrams

### 🏗️ System Architecture (`system_architecture.png`)
Shows the overall system architecture with all components, layers, and their relationships:
- User Interface Layer (TranslationDisplayWindow)
- Application Layer (TeamsTranslatorApp)
- Business Logic Layer (TranslationService, TextCapture)
- Configuration Layer (AppConfig)
- External Dependencies (LibreTranslate API, System Clipboard)

### 📊 Class Diagram (`class_diagram.png`)
UML class diagram showing all classes, their attributes, methods, and relationships:
- Configuration classes (AppConfig, TranslationConfig, UIConfig, CaptureConfig)
- Core application classes (TeamsTranslatorApp)
- Business logic classes (TranslationService, TextCapture)
- UI classes (TranslationDisplayWindow)

### 🔄 Sequence Diagram (`sequence_diagram.png`)
Shows the interaction flow between components over time:
- Application initialization
- Countdown and setup
- Main translation loop
- Error handling scenarios
- Shutdown sequence

### 🌐 Deployment Diagram (`deployment_diagram.png`)
Illustrates deployment scenarios and infrastructure:
- User workstation components
- Translation server options
- Network requirements
- Alternative deployment scenarios (Docker, Cloud)

### 📈 State Diagram (`state_diagram.png`)
Shows application states and transitions:
- Initialization states
- Countdown phase
- Main translation loop states
- Error handling states
- Shutdown process

### 🔀 Data Flow Diagrams
- `data_flow.png` - Complex activity diagram showing detailed workflow
- `simple_data_flow.png` - Simplified data flow for easier understanding

## Viewing the Diagrams

### Command Line
```bash
# View all diagrams
eog *.png

# View specific diagram
eog system_architecture.png

# View in Firefox
firefox *.png
```

### File Browser
Navigate to this directory and double-click any `.png` file to open with your default image viewer.

## Regenerating Diagrams

If you modify any `.pu` files, regenerate the diagrams:

```bash
# Generate all diagrams
plantuml -tpng *.pu

# Generate specific diagram
plantuml -tpng system_architecture.pu

# Generate with different format
plantuml -tsvg *.pu  # SVG format
plantuml -tpdf *.pu  # PDF format
```

## PlantUML Source Files

- `system_architecture.pu` - System architecture diagram source
- `class_diagram.pu` - Class diagram source
- `sequence_diagram.pu` - Sequence diagram source
- `deployment_diagram.pu` - Deployment diagram source
- `state_diagram.pu` - State diagram source
- `data_flow.pu` - Complex data flow diagram source
- `simple_data_flow.pu` - Simplified data flow diagram source

## Diagram Features

All diagrams include:
- **Professional styling** with consistent color schemes
- **Detailed annotations** explaining key concepts
- **Clear visual hierarchy** with proper grouping
- **Informative notes** providing additional context
- **High resolution** suitable for documentation and presentations

## Usage in Documentation

These diagrams are referenced in:
- `../architecture.md` - Technical architecture documentation
- `../api.md` - API documentation
- `../../README.md` - Main project documentation

## Customization

To customize the diagrams:
1. Edit the corresponding `.pu` file
2. Modify colors, fonts, or layout in the skinparam sections
3. Add or remove components as needed
4. Regenerate with PlantUML

Example color customization:
```plantuml
skinparam component {
    BackgroundColor #YOUR_COLOR
    BorderColor #YOUR_BORDER_COLOR
    FontColor #YOUR_FONT_COLOR
}
```