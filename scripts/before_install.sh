#!/bin/bash
set -ex

echo "Installing dependencies on Amazon Linux..."

# Update system packages
sudo yum update -y

# Install Python 3 and pip if not already installed
sudo yum install -y python3 python3-pip

# Use yum to ensure pip is up to date (do not use pip upgrade to avoid RPM conflicts)
sudo yum reinstall -y python3-pip

# Check if requirements.txt exists and install dependencies
if [ -f /home/ec2-user/flask-app/requirements.txt ]; then
    # Use the system pip3 to install requirements
    sudo /usr/bin/pip3 install -r /home/ec2-user/flask-app/requirements.txt || { echo 'Dependency installation failed'; exit 1; }
else
    echo "requirements.txt not found. Skipping dependency installation."
fi
