#!/bin/bash

set -euo pipefail
if command -v python3 &>/dev/null; then
    echo "Python 3 is installed."
else
    echo "Python 3 is not installed. Installing..."
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
fi

python3 -m venv chat/venv/
source chat/venv/bin/activate

pip3 install -r chat/requirements.txt
python3 chat/app.py