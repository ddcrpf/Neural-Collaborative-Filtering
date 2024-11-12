#!/bin/bash
echo "Validating Flask application..."
pgrep -f app.py > /dev/null
if [ $? -ne 0 ]; then
    echo "Flask application is not running."
    exit 1
else
    echo "Flask application is running."
fi
