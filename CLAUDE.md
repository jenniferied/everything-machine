# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Everything Machine (Kepler) is an artistic research website for Jennifer Meier's MA thesis. It's a static website for GitHub Pages combining generative AI research, digital identity exploration, and music production documentation.

## Development Commands

```bash
# Local development (required for ES6 modules and fetch)
python3 -m http.server 8001
# or
npx http-server -p 8001
# or use VS Code Live Server extension

# Generate journal manifest after adding entries
node scripts/generate-journal-manifest.js
```

No build step, bundler, or package.json - this is a vanilla JavaScript project with ES6 modules.

## Project Structure

```
/
├── README.md, CLAUDE.md      # Root documentation
├── index.html, style.css     # Entry point and styles
├── docs/                     # Documentation (IMPLEMENTATION, TESTING, research docs)
├── scripts/                  # Utility scripts (journal manifest generator)
├── js/                       # ES6 modules (app.js, core/, audio/, navigation/, etc.)
├── journal/                  # Markdown entries (journal-YYYY-MM-DD-title.md)
└── assets/
    ├── audio/, images/       # Media files
    ├── journal/              # Journal assets (YYYY-MM-DD-topic/)
    └── archive/              # Unused/archived assets
```

## Architecture

### Core Pattern: EventBus + Dependency Injection

All components communicate via a central pub/sub EventBus. Components receive dependencies through constructor injection, never query the DOM directly for other components.

```javascript
// Event naming: category:action (lowercase, colon separator)
// Examples: player:play, nav:pageChanged, journal:loaded

// Constructor injection pattern
constructor(container, eventBus, featureDetector) {
  this.container = container;
  this.eventBus = eventBus;
  // ...
}
```

### Application Bootstrap (js/app.js)

The `Application` class initializes in phases:
1. Core services (EventBus, FeatureDetector, ScriptLoader)
2. Capability detection
3. Controllers (AnimationController, LazyLoader, ImageGallery)
4. Viewers (ThreeDViewer, PointCloudViewer, VideoViewer)
5. Animations
6. UI components
7. Audio player
8. Navigation
9. Journal
10. Markdown pages

Debug mode auto-enables on localhost.

### Module Organization

- **js/core/**: Singleton services (EventBus, FeatureDetector, ScriptLoader)
- **js/audio/**: Music player (MusicPlayer facade coordinates Playlist, PlaybackController, PlayerUI)
- **js/navigation/**: Page switching (PageNavigator, DropdownController, NavigationState)
- **js/journal/**: Markdown journal system (JournalManager coordinates loading, parsing, rendering)
- **js/viewers/**: 3D/video viewers extend ViewerBase abstract class
- **js/animations/**: FloatingAnimation managed by AnimationController
- **js/media/**: LazyLoader (IntersectionObserver), ImageGallery (lightbox)

### Viewer Pattern

All viewers extend `ViewerBase` with lifecycle methods:
```javascript
async checkSupport()     // Verify device capabilities
async loadDependencies() // Lazy load libraries (Three.js, etc.)
async initialize()       // Setup viewer
async render()           // Display content
showFallback()          // Static image fallback
dispose()               // Cleanup
```

### Journal System

Journal entries are markdown files in `journal/` loaded via `journal-manifest.json`. Custom syntax:
- `[WORLD_INFO:...]` creates expandable world-info dropdowns
- Images are auto-formatted (full-width standalone, 50% inline)

## Code Conventions

- One class per file (PascalCase for classes, camelCase for utilities)
- Every component must have a `dispose()` method for cleanup
- Error logging format: `console.error('[ComponentName] Message:', error)`
- JSDoc comments for public methods
- Use `requestAnimationFrame` for visual updates
- Debounce expensive operations

## Important Constraints

- No global variables (except `window.everythingMachineApp` for debugging)
- Components depend on abstractions (EventBus), not concrete classes
- External libraries (Three.js, Anime.js, Video.js) are lazy-loaded via ScriptLoader
- Respects `prefers-reduced-motion` for animations
- Progressive enhancement: core content works without JavaScript

## Testing

Manual browser testing required before commits:
1. Open DevTools Console + Network tabs
2. Test feature manually
3. Verify no console errors
4. Check EventBus debug logs on localhost
5. Test mobile viewport

## Journal Entry Writing

When editing journal entries in `journal/`, use this structure:
- **Intention**: What was the goal?
- **Prozess**: What was done? (screenshots, prompts)
- **Ergebnis**: What happened?
- **Reflexion**: What was learned? Surprises? Workflow changes?
- **Nächste Schritte**: What's next?

Focus on process over results, document failures, use first-person perspective.
