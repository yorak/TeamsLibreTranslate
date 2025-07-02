#!/bin/bash

# Generate all PlantUML diagrams for Teams Translator
# Usage: ./generate_all.sh

echo "🎨 Generating Teams Translator Diagrams..."

# Check if plantuml is available
if ! command -v plantuml &> /dev/null; then
    echo "❌ Error: plantuml is not installed or not in PATH"
    echo "Please install plantuml first:"
    echo "  Ubuntu/Debian: sudo apt install plantuml"
    echo "  macOS: brew install plantuml"
    echo "  Or download from: https://plantuml.com/download"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p output

# List of diagrams to generate
diagrams=(
    "system_architecture"
    "data_flow"
    "class_diagram"
    "sequence_diagram"
    "deployment_diagram"
    "state_diagram"
)

# Generate each diagram
for diagram in "${diagrams[@]}"; do
    echo "📊 Generating ${diagram}..."
    
    if plantuml -tpng "${diagram}.pu" -o output/; then
        echo "✅ ${diagram}.png generated successfully"
    else
        echo "❌ Failed to generate ${diagram}.png"
    fi
done

echo ""
echo "🎉 Diagram generation complete!"
echo "📁 Output files are in the 'output' directory:"
echo ""

# List generated files
for diagram in "${diagrams[@]}"; do
    if [ -f "output/${diagram}.png" ]; then
        echo "   ✓ ${diagram}.png"
    else
        echo "   ✗ ${diagram}.png (failed)"
    fi
done

echo ""
echo "🖼️  To view the diagrams:"
echo "   eog output/*.png"
echo "   # or"
echo "   firefox output/*.png"
echo "   # or use your preferred image viewer"