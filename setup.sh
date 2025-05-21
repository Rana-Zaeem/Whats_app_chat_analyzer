#!/bin/bash

mkdir -p ~/.streamlit/

# Handle the distutils issue first - this is critical!
if [ ! -d "/usr/local/lib/python3.9/distutils" ]; then
  echo "Installing Python distutils..."
  apt-get update && apt-get install -y python3-distutils
fi

# Update pip - use an older but stable version
python -m pip install --upgrade pip==23.0.1

# Install core dependencies first with pre-built wheels
pip install --no-cache-dir wheel setuptools

# Use requirements.txt with compatible versions
pip install -r requirements.txt --no-cache-dir

# Install NLTK data with a timeout to prevent hanging
python -c "import nltk; nltk.download('punkt', timeout=60); nltk.download('stopwords', timeout=60); nltk.download('averaged_perceptron_tagger', timeout=60)"

# No need to download spacy model since we're including it in requirements.txt as a wheel

# Setup Streamlit config for deployment
cat > ~/.streamlit/config.toml <<EOF
[server]
headless = true
enableCORS = true
enableXsrfProtection = true

[theme]
base = "dark"
primaryColor = "#4CAF50"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#1f2937"
textColor = "#ffffff"
font = "sans serif"
EOF

# Setup port for Heroku and other platforms
echo "\
[server]\n\
port = $PORT\n\
" > ~/.streamlit/config.toml