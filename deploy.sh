#!/bin/bash

# Multilingual Grammar Error Detection & Correction - Deployment Script
echo "🚀 Setting up Multilingual Grammar Error Detection & Correction..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if models exist
echo "🔍 Checking for model files..."
if [ ! -f "models/english/baseline_ft0_fce_3e.pt" ]; then
    echo "⚠️  Warning: Model files not found in models/ directory."
    echo "   The application will use base models for detection."
    echo "   For full functionality, please download the trained models."
fi

if [ ! -f "t5_jfleg/saved_model/model/pytorch_model.bin" ]; then
    echo "⚠️  Warning: T5 model not found."
    echo "   The application will use base T5 model for correction."
fi

# Start the application
echo "🎉 Starting the application..."
echo "   The app will be available at: http://localhost:5002"
echo "   Press Ctrl+C to stop the server"
echo ""

python app_multilingual.py 