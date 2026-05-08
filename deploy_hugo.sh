#!/bin/bash

# Script to deploy Hugo site to GitHub Pages

echo "Building Hugo site..."
hugo --minify

echo "Deploying to GitHub Pages..."
echo "Make sure you have configured your GitHub remote and have push permissions"

# The GitHub Actions workflow will handle the actual deployment
# This script just builds the site locally for testing

echo "Site built successfully. You can now push to GitHub to trigger deployment via GitHub Actions."
echo "Remember to:"
echo "1. Update your content in the content/ directory"
echo "2. Test locally with 'hugo server'"
echo "3. Commit and push changes to trigger GitHub Actions deployment"