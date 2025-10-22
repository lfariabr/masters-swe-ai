#!/bin/bash

echo "===================================="
echo "  EigenAI - Launching Application"
echo "===================================="
echo

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

# Run the launcher
python3 run_eigenai.py