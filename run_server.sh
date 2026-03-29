#!/bin/bash

# Chanlun Pro Startup Script
# This script starts the Chanlun Pro application with proper configuration

echo "Starting Chanlun Pro Application..."
echo "====================================="

# Change to the project directory
cd "$(dirname "$0")"

# Check if Python 3.11 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$PYTHON_VERSION" != "3.11" ]]; then
    echo "Warning: Python 3.11 is recommended, detected: $PYTHON_VERSION"
fi

# Create the data directory if it doesn't exist
mkdir -p ~/.chanlun_pro

# Start the application
echo "Starting server on http://127.0.0.1:9900"
echo "Press Ctrl+C to stop the server"
echo ""

python3 start_app.py