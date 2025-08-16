#!/usr/bin/env bash
# Headless launcher for the YouTube Transcript Tool (CLI, timestamped always)
# Usage: ./run_transcript_tool_cli.sh [video_url]
# If no URL argument is provided, the script will prompt interactively (same as Python script).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_DIR="${SCRIPT_DIR}/../py"
SCRIPT_NAME="transcript_tool_cli.py"

# Choose python interpreter
if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Error: Python is not installed." >&2
    exit 1
fi

cd "${PY_DIR}" || { echo "Failed to enter ${PY_DIR}" >&2; exit 1; }

# Pass through any arguments (e.g., you could later adapt script to accept a URL directly)
exec "$PYTHON" "$SCRIPT_NAME" "$@"
