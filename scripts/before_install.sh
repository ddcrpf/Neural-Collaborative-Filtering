#!/bin/bash
set -ex

echo "Installing dependencies on Amazon Linux..."

# Update the package list
sudo yum update -y

# Install Python 3 and pip if not already installed
sudo yum install -y python3 python3-pip

# Ensure pip is upgraded
sudo pip3 install --upgrade pip

# Check if requirements.txt exists and install dependencies
if [ -f /home/ec2-user/flask-app/requirements.txt ]; then
    sudo pip3 install -r /home/ec2-user/flask-app/requirements.txt || { echo 'Dependency installation failed'; exit 1; }
else
    echo "requirements.txt not found. Skipping dependency installation."
fi
