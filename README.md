# Hyunsoo Han's Personal Website

This is a personal website for Hyunsoo Han, featuring a CV and calendar. The site is built using React and follows the structure of the JJ000n.github.io project.

## Features

- Personal CV with education, experience, and publications
- Interactive calendar with event management
- Add, view, and manage daily tasks and events
- Persistent storage using localStorage
- Responsive design for all device sizes

## Technologies Used

- React.js
- React Router
- CSS Modules

## Structure

The project follows the standard React project structure:

```
src/
├── components/
│   └── Header.js
├── pages/
│   ├── Home.js
│   ├── CV.js
│   └── Calendar.js
├── assets/
├── hooks/
├── services/
└── types/
```

## Getting Started

1. Clone the repository
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

## Deployment

### Manual Deployment
```bash
# Install gh-pages dependency
npm install --save-dev gh-pages

# Deploy to GitHub Pages
npm run deploy
```

### GitHub Actions Deployment (Automated)
This repository is configured to automatically deploy to GitHub Pages on every push to the main branch.

## Access
Once deployed, your site will be accessible at:
- Main Page: https://hyun-s.github.io/hyun-s.github.io
- Calendar: https://hyun-s.github.io/hyun-s.github.io/calendar

## Calendar Features
- Click on any date to add events/tasks
- View events for each day
- Events are saved locally in your browser

## Author

Hyunsoo Han - Researcher in AI Diffusion Model Compression