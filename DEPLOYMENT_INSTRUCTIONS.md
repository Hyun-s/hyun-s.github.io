# Deployment Instructions

This document provides instructions for deploying the hyun-s.github.io website.

## Prerequisites

- Node.js (version 14 or higher)
- npm (comes with Node.js)
- Git installed and configured

## Installation Steps

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd hyun-s.github.io
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Building for Production

To create a production build:

```bash
npm run build
```

This will create a `build` directory with all the files needed for deployment.

## Deployment Options

### Option 1: GitHub Pages (Recommended)

1. Create a new repository on GitHub named `hyun-s.github.io`
2. Configure the remote:
   ```bash
   git remote add origin https://github.com/yourusername/hyun-s.github.io.git
   ```
3. Push to GitHub:
   ```bash
   git branch -M main
   git push -u origin main
   ```

### Option 2: Manual Deployment

1. Build the project:
   ```bash
   npm run build
   ```

2. Deploy the contents of the `build` directory to your web server.

## Testing the Deployment

After deployment, you can access your site at:
- GitHub Pages: https://yourusername.github.io/hyun-s.github.io
- Custom domain: your custom domain

## Git Automation Commands

You can also use the provided script to automate the Git setup:

```bash
chmod +x git_commands.sh
./git_commands.sh
```

This will initialize the Git repository, create a .gitignore file, stage all files, and make an initial commit.

## Troubleshooting

If you encounter issues:

1. Make sure all dependencies are installed:
   ```bash
   npm install
   ```

2. Check for any build errors:
   ```bash
   npm run build
   ```

3. Verify your Git configuration:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```