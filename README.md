# Personal Habit Tracker

A lightweight, password-protected habit tracking application built with HTML, CSS, and JavaScript. Perfect for Vercel deployment and easy migration to React/Next.js.

## Features

- 🔐 Password protection (password: `pass8`)
- 📊 Dashboard with habit metrics
- 🎯 Atomic Habits framework integration
- 📱 Responsive design
- 💾 Local storage for data persistence
- 🎨 Beautiful, modern UI
- ⚡ Lightweight and fast

## Quick Start

### Local Development

1. Clone the repository
2. Open `index.html` in your browser
3. Enter password: `pass8`

### Deploy to Vercel

1. Push to GitHub
2. Connect to Vercel
3. Deploy automatically (no build step needed!)

## Structure

```
project_consistency/
├── index.html          # Main application
├── vercel.json         # Vercel configuration
├── .vercelignore       # Files to ignore in deployment
└── README.md           # This file
```

## Migration to React/Next.js

This HTML/JS version is designed to be easily converted to React:

### Data Structure

- All habit data is stored in `SAMPLE_HABITS` array
- Local storage keys: `habits`, `authenticated`
- State management is simple and can be replaced with React state

### Components to Create

- `AuthScreen` - Password protection
- `Dashboard` - Main metrics view
- `HabitList` - Sidebar habit list
- `HabitDetail` - Individual habit view
- `GoalsSection` - Long/short term goals

### Benefits of This Approach

- ✅ No serverless function size limits
- ✅ Instant deployment on Vercel
- ✅ Easy to test and iterate
- ✅ Perfect foundation for React migration
- ✅ Works offline
- ✅ No backend dependencies

## Password

Default password: `pass8`

## Local Storage

The app uses browser local storage to persist:

- Habit data and progress
- Authentication state
- User preferences

## Future Enhancements

- [ ] Add new habits functionality
- [ ] Data export/import
- [ ] Habit streaks and statistics
- [ ] Dark mode toggle
- [ ] Mobile app version
