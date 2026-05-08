#!/bin/bash

# Final Deployment Script for Hugo Site
# Run this script to prepare your site for deployment

echo "==============================================="
echo "FINAL DEPLOYMENT PREPARATION FOR HUGO SITE"
echo "==============================================="

# Check if we have Hugo installed
echo "Checking Hugo installation..."
if command -v hugo &> /dev/null; then
    echo "✅ Hugo is installed"
else
    echo "⚠️  Hugo is not installed - you'll need to install it first"
    echo "   Ubuntu/Debian: sudo apt-get install hugo"
    echo "   macOS: brew install hugo"
fi

# Show current status
echo ""
echo "Current repository status:"
git status --short

echo ""
echo "Files that will be included in deployment:"
find . -maxdepth 2 -name "*.md" -o -name "*.html" -o -name "*.css" -o -name "*.js" | grep -v node_modules | grep -v ".git"

echo ""
echo "==============================================="
echo "DEPLOYMENT INSTRUCTIONS"
echo "==============================================="

echo "1. INSTALL HUGO (if not installed):"
echo "   Ubuntu/Debian: sudo apt-get install hugo"
echo "   macOS: brew install hugo"
echo "   Windows: choco install hugo"

echo ""
echo "2. TEST LOCALLY:"
echo "   hugo server --disableLiveReload"

echo ""
echo "3. BUILD FOR PRODUCTION:"
echo "   hugo --minify"

echo ""
echo "4. DEPLOY TO GITHUB:"
echo "   git add ."
echo "   git commit -m 'Deploy Hugo site'"
echo "   git push origin main"

echo ""
echo "5. YOUR SITE WILL BE LIVE AT:"
echo "   https://hyun-s.github.io/hyun-s.github.io/"

echo ""
echo "==============================================="
echo "SITE STRUCTURE SUMMARY"
echo "==============================================="

echo "Content files:"
find content/ -name "*.md" -exec echo "  {}" \;

echo ""
echo "Templates:"
find layouts/ -name "*.html" -exec echo "  {}" \;

echo ""
echo "Static assets:"
find static/ -type f -exec echo "  {}" \;

echo ""
echo "Configuration:"
cat config.toml

echo ""
echo "==============================================="
echo "READY TO DEPLOY!"
echo "==============================================="