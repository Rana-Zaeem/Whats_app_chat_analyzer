#!/bin/bash

# Create the streamlit config directory
mkdir -p ~/.streamlit/

# Install dependencies with optimized settings
echo "Installing dependencies..."
pip install --upgrade pip
pip install --no-cache-dir wheel setuptools
pip install -r requirements.txt

# Install NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')" || echo "NLTK download failed but continuing"

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
" > ~/.streamlit/config.toml