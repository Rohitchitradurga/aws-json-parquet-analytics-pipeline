#!/bin/bash
set -e

# Create venv if not exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with python3.11..."
    python3.11 -m venv .venv
fi

# Activate
source .venv/bin/activate

# Install deps
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete. To activate run: source .venv/bin/activate"
