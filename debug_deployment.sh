#!/bin/bash

# Debug script to help identify deployment issues
echo "DEBUG: Starting diagnostic script..."

# Check Python version
echo "Python version:"
python --version

# Check pip version
echo "Pip version:"
pip --version

# Check available disk space
echo "Disk space:"
df -h

# Check available memory
echo "Memory status:"
free -m

# Test installation of key packages
echo "Testing basic package installation..."
pip install --no-cache-dir wheel==0.41.2 setuptools==69.0.3 numpy==1.24.3

# Verify numpy installation
echo "Checking numpy installation:"
python -c "import numpy; print(f'Numpy version: {numpy.__version__}')"

# Check for spaCy model
echo "Checking for spaCy model availability:"
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl --no-cache-dir
python -c "import spacy; print('SpaCy model installation:', 'Success' if spacy.util.is_package('en_core_web_sm') else 'Not found')"

echo "DEBUG: Diagnostics complete."
