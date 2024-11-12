#!/bin/bash
echo "Starting Flask application..."
cd /home/ec2-user/flask-app
nohup python3 app.py > logs/flask_app.log 2>&1 &
