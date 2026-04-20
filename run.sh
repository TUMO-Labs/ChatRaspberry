#!/bin/bash

set -euo pipefail

# -- Check for Python 3 --
if command -v python3 &>/dev/null; then
    echo "Python 3 is installed."
else
    echo "Python 3 is not installed. Installing..."
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
fi

# -- Setup nginx --
if command -v nginx &>/dev/null; then
    echo "nginx is installed."
else
    echo "nginx is not installed. Installing..."
    sudo apt update
    sudo apt install -y nginx
fi

sudo cp nginx/chat.conf /etc/nginx/sites-available/chat.conf
sudo ln -s /etc/nginx/sites-available/chat.conf /etc/nginx/sites-enabled
sudo systemctl restart nginx

# -- Setup Flask app --
python3 -m venv chat/venv/
source chat/venv/bin/activate
pip3 install -r chat/requirements.txt

# -- Setup systemd service --
sudo cp chat.service /etc/systemd/system/chat.service
sudo systemctl daemon-reload
sudo systemctl enable chat
sudo systemctl restart chat