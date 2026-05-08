# Project Structure

This document outlines the folder structure and file organization for the hyun-s.github.io project, following the Hugo static site generator approach.

## Folder Structure

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
├── .gitignore
└── README.md
```

## Files Description

### Content Files
- `content/_index.md` - Home page content
- `content/cv/_index.md` - CV page content
- `content/calendar/_index.md` - Calendar page content

### Templates
- `layouts/_default/baseof.html` - Base HTML template
- `layouts/index.html` - Homepage template
- `layouts/_default/single.html` - Single page template
- `layouts/partials/nav.html` - Navigation partial
- `layouts/partials/footer.html` - Footer partial

### Static Assets
- `static/css/style.css` - CSS styles (copied from React version)
- `static/js/main.js` - JavaScript with calendar functionality

### Configuration
- `config.toml` - Hugo configuration file
- `.gitignore` - Git ignore patterns
- `README.md` - Project documentation

### Services and Hooks (Placeholder)
- All functionality moved to Markdown content and Hugo templates