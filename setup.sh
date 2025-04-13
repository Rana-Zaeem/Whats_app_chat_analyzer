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