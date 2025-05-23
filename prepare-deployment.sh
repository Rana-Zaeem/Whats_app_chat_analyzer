#!/bin/bash

echo "Preparing WhatsApp Chat Analyzer for deployment..."

# Check if we want minimal or full deployment
if [ "$1" == "minimal" ]; then
  echo "Setting up MINIMAL deployment..."
  cp -f requirements.txt requirements.backup.txt
  cp -f Procfile Procfile.backup
  echo "streamlit==1.10.0
pandas==1.1.5
numpy==1.19.5
matplotlib==3.3.4
seaborn==0.11.2
nltk==3.6.2" > requirements.txt
  echo "web: bash setup.sh && streamlit run minimal_app.py" > Procfile
  echo "python-3.7.16" > runtime.txt
  echo "Minimal deployment prepared!"
else
  echo "Setting up FULL deployment..."
  # Check if backups exist and restore them
  if [ -f "requirements.backup.txt" ]; then
    cp -f requirements.backup.txt requirements.txt
    rm requirements.backup.txt
  fi
  if [ -f "Procfile.backup" ]; then
    cp -f Procfile.backup Procfile
    rm Procfile.backup
  fi
  echo "web: bash setup.sh && streamlit run app.py" > Procfile
  echo "python-3.8.10" > runtime.txt
  echo "Full deployment prepared!"
fi

echo "Done! Now you can commit and push these changes to deploy."
