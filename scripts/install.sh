#!/bin/bash
# Install script for YouTube Transcript Tool

echo "Installing YouTube Transcript Tool dependencies..."

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed. Please install Python 3.6+ first."
    exit 1
fi

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
else
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

echo "Using Python command: $PYTHON_CMD"

# Check if tkinter is available (required for GUI)
$PYTHON_CMD -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Warning: tkinter not found. Installing tkinter..."
    
    # Detect Linux distribution and install tkinter
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        echo "Installing python3-tkinter via apt..."
        sudo apt-get update && sudo apt-get install -y python3-tkinter
    elif command -v yum &> /dev/null; then
        # RHEL/CentOS/Fedora
        echo "Installing tkinter via yum..."
        sudo yum install -y tkinter
    elif command -v dnf &> /dev/null; then
        # Fedora (newer)
        echo "Installing python3-tkinter via dnf..."
        sudo dnf install -y python3-tkinter
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        echo "Installing tk via pacman..."
        sudo pacman -S tk
    else
        echo "Could not auto-install tkinter. Please install manually:"
        echo "  Ubuntu/Debian: sudo apt-get install python3-tkinter"
        echo "  RHEL/CentOS: sudo yum install tkinter"
        echo "  Fedora: sudo dnf install python3-tkinter"
        echo "  Arch: sudo pacman -S tk"
    fi
fi

# Install Python requirements
if [ -f "../requirements.txt" ]; then
    echo "Installing required packages..."
    $PYTHON_CMD -m pip install -r "../requirements.txt"
    
    if [ $? -eq 0 ]; then
        echo "Installation complete!"
        echo ""
        echo "To run the tool:"
        echo "  $PYTHON_CMD scripts/transcript_tool.py"
        echo "  or: ./scripts/run_transcript_tool.sh"
        echo ""
        
        # Make shell script executable
        chmod +x run_transcript_tool.sh
        echo "Made run_transcript_tool.sh executable"
    else
        echo "Error: Failed to install Python packages"
        exit 1
    fi
else
    echo "Error: ../requirements.txt not found"
    exit 1
fi
