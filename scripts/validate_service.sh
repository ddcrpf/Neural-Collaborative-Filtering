#!/bin/bash
echo "Validating service..."
systemctl status httpd || systemctl status apache2 || exit 1
