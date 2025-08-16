@echo off
setlocal
echo Starting YouTube Transcript Tool (Headless CLI)...
pushd "%~dp0..\py"
python transcript_tool_cli.py
popd
echo.
echo Done.
pause
