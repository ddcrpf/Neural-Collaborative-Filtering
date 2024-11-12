#!/bin/bash
echo "Installing dependencies..."
yum update -y
yum install -y python3-pip
pip3 install -r /home/ec2-user/flask-app/requirements.txt
