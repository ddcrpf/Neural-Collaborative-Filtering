#!/bin/bash
echo "Starting application..."
systemctl start httpd || systemctl start apache2
