#!/bin/bash
set -ex

echo "Configuring application on Amazon Linux..."

# Create the logs directory with sudo and set proper permissions
sudo mkdir -p /home/ec2-user/flask-app/logs
sudo chmod 755 /home/ec2-user/flask-app/logs

echo "Logs directory created successfully with proper permissions."
