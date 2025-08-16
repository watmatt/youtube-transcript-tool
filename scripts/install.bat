@echo off
echo Installing YouTube Transcript Tool dependencies...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed. Please install Python 3.6+ first.
    pause
    exit /b 1
)

echo Installing required packages...
python -m pip install -r "%~dp0..\requirements.txt"

if %errorlevel% equ 0 (
    echo.
    echo Installation complete!
    echo.
    echo To run the tool, double-click: scripts\run_transcript_tool.bat
    echo Or run: python scripts\transcript_tool.py
) else (
    echo.
    echo Installation failed. Please check your Python installation.
)

pause
