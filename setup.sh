#!/bin/bash

# Create streamlit directory
mkdir -p ~/.streamlit/

# Try to install system packages but don't fail if it doesn't work
apt-get update || true
apt-get install -y python3-pip python3-setuptools python3-distutils build-essential || true

# Use a super simple pip installation approach
pip install --upgrade pip || true
pip install wheel setuptools || true

# Install minimal requirements for fastest deployment
pip install -r requirements-simplified.txt

# Configure Streamlit simply
cat > ~/.streamlit/config.toml <<EOF
[server]
port = $PORT
headless = true
enableCORS = false
enableXsrfProtection = false
EOF