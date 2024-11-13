#!/bin/bash
set -ex

echo "Validating Flask application on Amazon Linux..."

# Check if the Flask application process is running
if pgrep -f app.py > /dev/null; then
    echo "Flask application is running."
else
    echo "Flask application is not running."
    exit 1
fi
