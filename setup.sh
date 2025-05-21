#!/bin/bash

mkdir -p ~/.streamlit/

# Update pip
python -m pip install --upgrade pip==25.1.1

# Install core dependencies first with specific versions that have pre-built wheels
pip install --no-cache-dir wheel==0.41.2 setuptools==69.0.3

# Use the specially crafted requirements file for reliable deployment
pip install -r requirements-deploy.txt --no-cache-dir

# Install NLTK data with a timeout to prevent hanging
python -c "import nltk; nltk.download('punkt', timeout=60); nltk.download('stopwords', timeout=60); nltk.download('averaged_perceptron_tagger', timeout=60)"

# No need to download spacy model since we're including it in requirements-deploy.txt as a wheel

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