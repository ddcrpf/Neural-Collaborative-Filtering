#!/bin/bash
set -ex

echo "Starting Flask application on Amazon Linux..."

# Navigate to the application directory
cd /home/ec2-user/flask-app

# Kill any existing Flask application process (if running)
pkill -f app.py || echo "No existing Flask process found."

# Create the logs directory if it doesn't exist
mkdir -p /home/ec2-user/flask-app/logs

# Give the ec2-user write access to the logs directory without changing ownership of other files
chmod 755 /home/ec2-user/flask-app/logs

# Ensure the log file exists and is writable by ec2-user
touch /home/ec2-user/flask-app/logs/flask_app.log
chmod 644 /home/ec2-user/flask-app/logs/flask_app.log

# Start the Flask application using nohup
nohup python3 app.py > /home/ec2-user/flask-app/logs/flask_app.log 2>&1 &

# Wait for the application to start and check if it is running
sleep 5
if ! pgrep -f app.py > /dev/null; then
    echo "Failed to start Flask application."
    exit 1
else
    echo "Flask application started successfully."
fi
