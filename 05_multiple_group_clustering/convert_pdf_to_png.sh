#!/bin/bash
# Shell script to convert all PDF files from differential expression analysis to PNG format

# Set script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "PDF to PNG Conversion Script"
echo "============================="
echo ""

# Check if pdf2image is installed
echo "Checking dependencies..."
python3 -c "import pdf2image" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: pdf2image library not found."
    echo "Installing required dependencies..."
    pip install pdf2image pillow tqdm
    
    # Check if poppler-utils is installed (required by pdf2image)
    if ! command -v pdftoppm &> /dev/null; then
        echo ""
        echo "Warning: poppler-utils is not installed."
        echo "On Ubuntu/Debian, install with: sudo apt-get install poppler-utils"
        echo "On Fedora/RHEL, install with: sudo dnf install poppler-utils"
        echo "On macOS, install with: brew install poppler"
        echo ""
        read -p "Press Enter to continue anyway, or Ctrl+C to cancel..."
    fi
fi

# Run the Python script
echo ""
echo "Running conversion script..."
python3 convert_pdf_to_png.py

echo ""
echo "Done!"
