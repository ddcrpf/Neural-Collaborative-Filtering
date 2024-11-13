#!/bin/bash
set -ex

echo "Starting Flask application on Amazon Linux..."

# Navigate to the application directory
cd /home/ec2-user/flask-app

# Kill any existing Flask application process (if running)
pkill -f app.py || echo "No existing Flask process found."

# Start the Flask application using nohup
nohup python3 app.py > logs/flask_app.log 2>&1 &

# Wait for the application to start and check if it is running
sleep 5
if ! pgrep -f app.py > /dev/null; then
    echo "Failed to start Flask application."
    exit 1
else
    echo "Flask application started successfully."
fi
