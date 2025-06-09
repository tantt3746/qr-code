# Generate QR Code and then save to image

# Setup env
## Install python3
Download from https://www.python.org/ and then install it

## Setup virtual env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Run script that generate QR code and images
python ./src/generate/generate_qr.py