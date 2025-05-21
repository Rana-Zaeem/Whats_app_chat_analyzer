#!/bin/bash

mkdir -p ~/.streamlit/

# Handle the distutils issue first - this is critical!
echo "Installing system dependencies..."
apt-get update || true
apt-get install -y python3-distutils python3-dev build-essential || true

# Update pip but pin to a version known to work
echo "Upgrading pip..."
python -m pip install --upgrade pip==21.3.1

# Install core dependencies first with pre-built wheels
echo "Installing build tools..."
pip install --no-cache-dir wheel==0.37.1 setuptools==59.6.0

# Use the ultra-compatible requirements-fixed.txt
echo "Installing requirements..."
pip install -r requirements-fixed.txt --no-dependencies --no-build-isolation

# Install NLTK data separately to avoid timeout issues
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')" || true

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