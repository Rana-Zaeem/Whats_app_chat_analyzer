#!/bin/bash

# This script fixes common deployment issues by installing essential packages
# Run this if your deployment is failing

echo "==== WhatsApp Chat Analyzer Deployment Fix ===="
echo "Installing essential system packages..."

# Install system dependencies
apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    build-essential \
    python3-distutils \
    python3-setuptools \
    python3-wheel

echo "Upgrading pip..."
pip install --upgrade pip

# Install core build dependencies to avoid wheel building issues
echo "Installing core build tools..."
pip install --no-cache-dir setuptools wheel

echo "Installing requirements with version constraints..."
pip install --no-cache-dir -r requirements.txt

echo "==== Fix Complete ===="
echo "Try deploying your app again now!"
