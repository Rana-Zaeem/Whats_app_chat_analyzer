#!/bin/bash

mkdir -p ~/.streamlit/

# Update pip
python -m pip install --upgrade pip

# Install core dependencies first
pip install --no-cache-dir wheel setuptools

# Install NLTK data
python -m nltk.downloader punkt
python -m nltk.downloader stopwords
python -m nltk.downloader averaged_perceptron_tagger

# Install spaCy model
python -m pip install --no-cache-dir spacy
python -m spacy download en_core_web_sm

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