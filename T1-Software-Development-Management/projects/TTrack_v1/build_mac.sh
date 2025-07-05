#!/bin/bash

# TTrack macOS Build Script
# Builds the TTrack application for macOS using PyInstaller

# Output colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}[*] TTrack macOS Build Process Starting...${NC}"
echo -e "${BLUE}[*] $(date)${NC}"

# Error handling function
handle_error() {
    echo -e "${RED}[!] Error: $1${NC}"
    exit 1
}

# Check for Python 3.8+
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    handle_error "Python 3.8+ is required (found $PYTHON_VERSION)"
fi

echo -e "${GREEN}[✓] Python $PYTHON_VERSION detected${NC}"

# Check for PyInstaller
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo -e "${YELLOW}[!] PyInstaller not found. Installing...${NC}"
    python3 -m pip install PyInstaller || handle_error "Failed to install PyInstaller"
fi

echo -e "${GREEN}[✓] PyInstaller installed${NC}"

# Check for requirements.txt and install dependencies
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}[*] Checking dependencies...${NC}"
    python3 -m pip install -r requirements.txt || handle_error "Failed to install dependencies"
    echo -e "${GREEN}[✓] Dependencies installed${NC}"
fi

# Clean previous build artifacts
echo -e "${BLUE}[*] Cleaning previous build artifacts...${NC}"
rm -rf build/ dist/

# Run PyInstaller
echo -e "${BLUE}[*] Building TTrack with PyInstaller...${NC}"
python3 -m PyInstaller TTrack-macOs.spec || handle_error "PyInstaller build failed"

# Check if build was successful
if [ ! -d "dist/TTrack.app" ]; then
    handle_error "Build completed but TTrack.app was not created"
fi

# Build complete
echo -e "${GREEN}[✓] Build complete! Application is available at:${NC}"
echo -e "${BLUE}    $(pwd)/dist/TTrack.app${NC}"
echo -e "${YELLOW}[i] To run the application: open dist/TTrack.app${NC}"
echo -e "${YELLOW}[i] Build completed at $(date)${NC}"