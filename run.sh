#!/bin/bash

# Flask 2FA App Quick Start Script

echo "🔐 Flask 2FA Authentication App Setup"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"

# Set default secret key if not set
if [ -z "$SECRET_KEY" ]; then
    export SECRET_KEY="dev-secret-key-$(date +%s)"
    echo ""
    echo "🔑 Using development SECRET_KEY"
fi

# Run the application
echo ""
echo "🚀 Starting Flask application..."
echo ""
echo "======================================"
echo "Access the app at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "======================================"
echo ""

python app.py

