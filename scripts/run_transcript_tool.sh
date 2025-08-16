#!/bin/bash
# Linux/Mac launcher for YouTube Transcript Tool

echo "Starting YouTube Transcript Tool..."

# Check if python3 is available, fallback to python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python not found. Please install Python 3.6+ first."
    exit 1
fi

# Run the transcript tool
$PYTHON_CMD "$(dirname "$0")/transcript_tool.py"

# Keep terminal open to see any messages
echo "Press Enter to close..."
read
