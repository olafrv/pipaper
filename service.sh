#!/bin/bash

SERVICE_NAME="pipaper"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
PYTHON_EXEC="/usr/bin/python3"
SCRIPT_PATH="$(pwd)/main.py"

# Create systemd service file
echo "[Unit]
Description=PiPaper Service
After=network.target

[Service]
ExecStart=$PYTHON_EXEC $SCRIPT_PATH
WorkingDirectory=$(pwd)
Restart=always
User=pi
Group=pi

[Install]
WantedBy=multi-user.target" | sudo tee $SERVICE_FILE > /dev/null

# Reload systemd, enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

# Check status
sudo systemctl status $SERVICE_NAME --no-pager