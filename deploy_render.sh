#!/bin/bash

echo "🚀 Deploying to Render with base models only..."

# Check if we're in the right directory
if [ ! -f "app_render.py" ]; then
    echo "❌ Error: app_render.py not found. Make sure you're in the project directory."
    exit 1
fi

# Add all files
git add .

# Commit changes
git commit -m "Add Render-optimized deployment with base models only"

# Push to GitHub
git push origin main

echo "✅ Code pushed to GitHub!"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://render.com"
echo "2. Sign in with your GitHub account"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select your repository: nicole-mathias/automatic_grammar_error_correction"
echo "5. Use these settings:"
echo "   - Name: grammar-error-correction"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements_render.txt"
echo "   - Start Command: python app_render.py"
echo "   - Plan: Free"
echo "6. Click 'Create Web Service'"
echo ""
echo "🎯 This version uses ONLY base models (~500MB total) and should deploy successfully!" 