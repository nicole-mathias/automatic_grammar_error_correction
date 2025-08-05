#!/bin/bash

echo "🚀 Deploying Grammar Error Correction with Docker..."

# Check if we're in the right directory
if [ ! -f "Dockerfile" ]; then
    echo "❌ Error: Dockerfile not found. Make sure you're in the project directory."
    exit 1
fi

# Add all files
git add .

# Commit changes
git commit -m "Add Docker deployment for grammar error correction"

# Push to GitHub
git push origin main

echo "✅ Code pushed to GitHub!"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://render.com"
echo "2. Sign in with your GitHub account"
echo "3. Click 'New +' and select 'Web Service'"
echo "4. Connect your GitHub repository"
echo "5. Set the following:"
echo "   - Name: grammar-error-correction"
echo "   - Environment: Docker"
echo "   - Branch: main"
echo "6. Click 'Create Web Service'"
echo ""
echo "🎯 This version uses Docker which should avoid the tokenizers compilation issues!"
echo "🐳 Docker will handle all the dependency compilation in a controlled environment." 