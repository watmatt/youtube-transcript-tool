@echo off
setlocal
echo Starting YouTube Transcript Tool (GUI)...
REM Move to the py script directory so relative/absolute imports work
pushd "%~dp0..\py"
python transcript_tool.py
popd
echo.
echo Done.
pause
