#!/bin/bash
echo "Installing dependencies..."
yum install -y httpd || apt-get install -y apache2
