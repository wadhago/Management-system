#!/bin/bash

# Medical Laboratory Management System Installation Script

echo "Medical Laboratory Management System Installation"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

echo "✓ Python 3 is installed"

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo "pip is not installed. Please install pip and try again."
    exit 1
fi

echo "✓ pip is installed"

# Create virtual environment (optional but recommended)
echo "Creating virtual environment..."
python3 -m venv medical_lab_env

if [ $? -eq 0 ]; then
    echo "✓ Virtual environment created"
else
    echo "✗ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source medical_lab_env/bin/activate

if [ $? -eq 0 ]; then
    echo "✓ Virtual environment activated"
else
    echo "✗ Failed to activate virtual environment"
    exit 1
fi

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Required packages installed"
else
    echo "✗ Failed to install required packages"
    exit 1
fi

echo ""
echo "Installation completed successfully!"
echo ""
echo "To run the application:"
echo "1. Activate the virtual environment: source medical_lab_env/bin/activate"
echo "2. Run the application: python main.py"
echo ""
echo "Default login credentials:"
echo "Username: admin"
echo "Password: admin123"