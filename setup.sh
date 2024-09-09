#!/bin/bash

# Update package list silently
echo "Updating package list..."
sudo apt update -y > /dev/null 2>&1

# Install Python3, pip, and npm silently
echo "Installing Python3, pip, and npm..."
sudo apt install -y python3 python3-pip npm > /dev/null 2>&1

# Install Python packages silently
echo "Installing Streamlit and Elastic APM..."
pip install streamlit elastic-apm beautifulsoup4 > /dev/null 2>&1

# Run Localtunnel silently
echo "Running Localtunnel..."
npx localtunnel > /dev/null 2>&1 &

echo "Installation complete. Localtunnel is running in the background."