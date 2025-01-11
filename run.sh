#!/usr/bin/env sh

# Get absolute path of script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"

python "$SCRIPT_DIR/src/main.py"