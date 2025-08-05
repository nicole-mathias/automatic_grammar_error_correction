#!/bin/bash

echo "🚀 Deploying Grammar Error Correction to Render..."

# Check if we're in the right directory
if [ ! -f "app_multilingual.py" ]; then
    echo "❌ Error: app_multilingual.py not found. Make sure you're in the project directory."
    exit 1
fi

# Add all files
git add .

# Commit changes
git commit -m "Configure for Render deployment with Docker"

# Push to GitHub
git push origin main

echo "✅ Code pushed to GitHub!"
echo ""
echo "📋 Next steps for Render deployment:"
echo "1. Go to https://render.com"
echo "2. Sign in with your GitHub account"
echo "3. Click 'New +' and select 'Web Service'"
echo "4. Connect your GitHub repository: automatic_grammar_error_correction"
echo "5. Set the following configuration:"
echo "   - Name: grammar-error-correction"
echo "   - Environment: Docker"
echo "   - Branch: main"
echo "   - Root Directory: ./ (leave empty)"
echo "6. Click 'Create Web Service'"
echo ""
echo "🎯 This will deploy your full deep learning models with:"
echo "   - T5 for grammar correction"
echo "   - BERT models for 5 languages (English, Czech, German, Italian, Swedish)"
echo "   - Full multilingual support"
echo ""
echo "⏱️  First deployment may take 10-15 minutes to build and start" 