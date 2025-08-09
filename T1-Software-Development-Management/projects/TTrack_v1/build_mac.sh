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

# Detect the correct Python executable
# Priority: python (if in pyenv), python3, then system python3
if command -v python &> /dev/null && python --version 2>&1 | grep -q "Python 3"; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    handle_error "No suitable Python 3 installation found"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    handle_error "Python 3.8+ is required (found $PYTHON_VERSION)"
fi

echo -e "${GREEN}[✓] Using Python $PYTHON_VERSION at $(which $PYTHON_CMD)${NC}"

# Check if we're in a virtual environment or pyenv
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo -e "${GREEN}[✓] Virtual environment detected: $VIRTUAL_ENV${NC}"
elif [[ -n "$PYENV_VERSION" ]] || command -v pyenv &> /dev/null; then
    echo -e "${GREEN}[✓] pyenv environment detected${NC}"
fi

# Check for PyInstaller
if ! $PYTHON_CMD -c "import PyInstaller" &> /dev/null; then
    echo -e "${YELLOW}[!] PyInstaller not found. Installing...${NC}"
    
    # Try pip install with different strategies
    if $PYTHON_CMD -m pip install PyInstaller; then
        echo -e "${GREEN}[✓] PyInstaller installed successfully${NC}"
    elif $PYTHON_CMD -m pip install --user PyInstaller; then
        echo -e "${GREEN}[✓] PyInstaller installed with --user flag${NC}"
    else
        handle_error "Failed to install PyInstaller. Please install manually: $PYTHON_CMD -m pip install PyInstaller"
    fi
else
    echo -e "${GREEN}[✓] PyInstaller already installed${NC}"
fi

# Verify all dependencies are installed
echo -e "${YELLOW}[*] Verifying dependencies...${NC}"
if ! $PYTHON_CMD -c "import PyQt5, pandas, openpyxl, dotenv, supabase" &> /dev/null; then
    echo -e "${YELLOW}[!] Some dependencies missing. Installing from requirements.txt...${NC}"
    $PYTHON_CMD -m pip install -r requirements.txt || handle_error "Failed to install dependencies"
fi

echo -e "${GREEN}[✓] All dependencies verified${NC}"

# Clean previous build artifacts
echo -e "${BLUE}[*] Cleaning previous build artifacts...${NC}"
rm -rf build/ dist/

# Build the application
echo -e "${YELLOW}[*] Building TTrack application...${NC}"
$PYTHON_CMD -m PyInstaller TTrack-macOs.spec --noconfirm || handle_error "PyInstaller build failed"

echo -e "${GREEN}[✓] Build completed successfully${NC}"

# Copy .env.example to app bundle for user setup
echo -e "${YELLOW}[*] Setting up environment template...${NC}"
cp .env.example "dist/TTrack.app/Contents/MacOS/.env.example" || echo -e "${YELLOW}[!] Warning: Could not copy .env.example${NC}"

# Create setup instructions
cat > "dist/SETUP.md" << EOF
# TTrack Setup Instructions

## Database Configuration
1. Navigate to: TTrack.app/Contents/MacOS/
2. Rename \`.env.example\` to \`.env\`
3. Edit \`.env\` with your Supabase credentials:
   \`\`\`
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key-here
   \`\`\`
4. Save and run TTrack.app

## Security Note
Never share your .env file - it contains your private database credentials.
EOF

echo -e "${GREEN}[✓] Created user setup instructions${NC}"
echo -e "${GREEN}[🎉] Build process complete!${NC}"
echo ""
echo -e "${BLUE}Distribution files:${NC}"
echo -e "  ${GREEN}✓${NC} dist/TTrack.app (main application)"
echo -e "  ${GREEN}✓${NC} dist/SETUP.md (user setup guide)"
echo -e "  ${GREEN}✓${NC} TTrack.app/Contents/MacOS/.env.example (credential template)"
echo ""
echo -e "${YELLOW}To test the build:${NC}"
echo -e "  1. Copy your .env to: dist/TTrack.app/Contents/MacOS/.env"
echo -e "  2. Run: open dist/TTrack.app"