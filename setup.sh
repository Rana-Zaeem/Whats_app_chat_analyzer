#!/bin/bash

# Create streamlit directory
mkdir -p ~/.streamlit/

# Install Python distutils first - this is critical
apt-get update && apt-get install -y python3-distutils python3-setuptools || echo "Failed to install distutils, but continuing"

# Install pip in a way that works on all platforms
pip install --no-cache-dir --ignore-installed pip==20.0.2

# Install basic build tools
pip install --no-cache-dir wheel setuptools==44.0.0

# Install requirements with very basic settings
pip install --no-cache-dir -r requirements.txt

# Download NLTK data with safe options
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True)" || echo "NLTK download failed, but continuing"

# Configure Streamlit simply
cat > ~/.streamlit/config.toml <<EOF
[server]
port = $PORT
headless = true
enableCORS = false
EOF
" > ~/.streamlit/config.toml