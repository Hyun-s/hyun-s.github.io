#!/bin/bash

# Git automation commands for setting up the project

echo "Initializing Git repository..."
git init

echo "Creating .gitignore file..."
cat > .gitignore << EOF
# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

# Editor
.vscode/
.idea/
*.swp
*.swo

# Local files
.env
EOF

echo "Adding all files to git..."
git add .

echo "Making initial commit..."
git commit -m "Initial commit: Setup project structure and files"

echo "To push to a remote repository, run:"
echo "git remote add origin <your-remote-url>"
echo "git branch -M main"
echo "git push -u origin main"