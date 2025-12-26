#!/usr/bin/env bash

# Directory of the script
SCRIPT_DIR="$(cd -- $(dirname -- "$0") && pwd)"

# Prefer .venv (common naming), fall back to venv
if [ -d "$SCRIPT_DIR/.venv" ]; then
    # shellcheck source=/dev/null
    source "$SCRIPT_DIR/.venv/bin/activate" || exit 1
elif [ -d "$SCRIPT_DIR/venv" ]; then
    # shellcheck source=/dev/null
    source "$SCRIPT_DIR/venv/bin/activate" || exit 1
else
    echo "No virtualenv found (.venv or venv). Continuing without activating."
fi

# Ensure flet CLI is available
if ! command -v flet >/dev/null 2>&1; then
    echo "flet CLI not found. Install deps via: pip install -r requirements.txt"
    exit 1
fi

# Launch the Flet desktop UI (legacy Streamlit start.sh remains unchanged)
flet run "$SCRIPT_DIR/app/main.py"
