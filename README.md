# Hyunsoo Han - Personal Website (Hugo Version)

This is a Hugo-based personal website for Hyunsoo Han, following the structure inspired by JJ000n.github.io.

## Features

- Personal CV with education, experience, and publications
- Interactive calendar with event management
- Add, view, and manage daily tasks and events
- Persistent storage using localStorage
- Responsive design for all device sizes

## Structure

```
hyun-s-hugo-site/
├── content/
│   ├── _index.md              # Home page
│   ├── cv/
│   │   └── _index.md          # CV page
│   └── calendar/
│       └── _index.md          # Calendar page
├── layouts/
│   ├── _default/
│   │   ├── baseof.html        # Base template
│   │   ├── single.html        # Single page template
│   │   └── list.html          # List page template
│   ├── partials/
│   │   ├── header.html        # Header partial
│   │   ├── footer.html        # Footer partial
│   │   └── nav.html           # Navigation partial
│   └── index.html             # Homepage template
├── static/
│   ├── css/
│   │   └── style.css          # Styles
│   └── js/
│       └── main.js            # Scripts
├── config.toml                # Hugo configuration
└── README.md                  # This file
```

## Getting Started

1. Install Hugo (version 0.124.1 or later)
2. Clone this repository
3. Run `hugo server` to start development server
4. Build with `hugo` for production

## Deployment

### GitHub Actions Deployment (Automated)
This repository is configured to automatically deploy to GitHub Pages on every push to the main branch.

The deployment process:
1. Hugo builds the site (hugo --minify)
2. GitHub Actions deploys the built site to the gh-pages branch
3. GitHub Pages serves content from the gh-pages branch

### Manual Deployment
```bash
# Install Hugo
# Run hugo to build the site
hugo

# The built site will be in the 'public' directory
# Push to GitHub to trigger automated deployment
```

## Technologies Used

- Hugo (static site generator)
- HTML5/CSS3
- JavaScript with localStorage
- Responsive design

## Author

Hyunsoo Han - Researcher in AI Diffusion Model Compression