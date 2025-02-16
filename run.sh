#!/usr/bin/env sh

# Exit on error
set -e

# Get absolute path of script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"

# Run setup if virtual environment doesn't exist
if [ ! -f "$VENV_PYTHON" ]; then
    (sh "$SCRIPT_DIR/setup.sh")  # Execute in subshell
    printf "\nPress any key to continue..."
    command read -r || read -n 1 -s -r
    clear
fi

# Check if Python in virtual environment is executable
if [ ! -x "$VENV_PYTHON" ]; then
    echo "Error: Python in virtual environment is not executable"
    exit 1
fi

"$VENV_PYTHON" "$SCRIPT_DIR/src/main.py"