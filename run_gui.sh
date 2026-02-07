#!/bin/bash
# Launch the Comick Merger GUI

cd "$(dirname "$0")"

if [ ! -f ".venv/bin/python" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run: uv sync"
    exit 1
fi

.venv/bin/python -m comick_merger.main
