#!/bin/bash

# Hugo Site Management Script

echo "Hugo Site Management for Hyunsoo Han's Website"
echo "============================================="

# Show current status
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la | grep -E "(hugo|content|layouts|static|config)"

echo ""
echo "Available commands:"
echo "  hugo-server     - Start local Hugo server for development"
echo "  hugo-build      - Build the site"
echo "  hugo-deploy     - Deploy site (via GitHub Actions)"
echo "  backup-react    - Backup current React version"
echo "  restore-react   - Restore React version from backup"
echo ""

case "$1" in
    hugo-server)
        echo "Starting Hugo server for development..."
        hugo server --disableLiveReload
        ;;
    hugo-build)
        echo "Building Hugo site..."
        hugo --minify
        echo "Site built in public/ directory"
        ;;
    hugo-deploy)
        echo "Deploying site via GitHub Actions..."
        echo "Commit and push changes to trigger deployment"
        ;;
    backup-react)
        echo "Backing up current React version..."
        cp -r . /tmp/react_backup_$(date +%Y%m%d_%H%M%S)
        echo "Backup created"
        ;;
    restore-react)
        echo "Restoring React version from backup..."
        echo "Please specify which backup to restore (see /tmp/ for options)"
        ;;
    *)
        echo "Usage: $0 {hugo-server|hugo-build|hugo-deploy|backup-react|restore-react}"
        ;;
esac