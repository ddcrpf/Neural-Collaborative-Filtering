#!/bin/bash
set -ex

echo "Starting Flask application on Amazon Linux..."

# Navigate to the application directory
cd /home/ec2-user/flask-app

# Kill any existing Flask application process (if running)
pkill -f app.py || echo "No existing Flask process found."

# Create the logs directory and ensure proper permissions
sudo mkdir -p /home/ec2-user/flask-app/logs
sudo chmod 755 /home/ec2-user/flask-app/logs

# Ensure the log file is created and has the correct permissions
sudo touch /home/ec2-user/flask-app/logs/flask_app.log
sudo chmod 644 /home/ec2-user/flask-app/logs/flask_app.log

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
