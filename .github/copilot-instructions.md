# Everything Machine - AI Coding Agent Instructions

## Project Context

**Everything Machine (Kepler)** is an artistic research website combining generative AI research, digital identity exploration, and music production. It's a static GitHub Pages site built with vanilla ES6 JavaScript, no build tools or bundlers. The project also includes a thesis component with LaTeX-based PDF generation.

## Architecture Overview

### Core Pattern: EventBus + Dependency Injection

All components communicate via a **central EventBus** (pub/sub pattern). Components never query the DOM for other components—dependencies are injected via constructors.

```javascript
// Event naming: category:action (lowercase, colon separator)
this.eventBus.emit('player:play');
this.eventBus.on('journal:loaded', (data) => { /* ... */ });
```

### Module Organization

```
js/
├── core/               # Singleton services
│   ├── EventBus.js         # Pub/sub event system
│   ├── FeatureDetector.js  # Device capabilities (GPU, WebGL, audio)
│   └── ScriptLoader.js     # Lazy load external libraries (Three.js, etc.)
├── audio/              # Music player (MusicPlayer coordinates Playlist, PlaybackController, PlayerUI)
├── journal/            # Journal system (JournalManager coordinates loader, parser, renderer)
├── navigation/         # Page switching (PageNavigator, DropdownController)
├── viewers/            # 3D/video viewers (extend ViewerBase)
├── animations/         # Visual effects (AnimationController, FloatingAnimation)
├── media/              # Image/lazy loading (LazyLoader, ImageGallery)
└── app.js              # Main orchestrator, initializes all systems
```

**Key principle**: One class per file (PascalCase), one responsibility per class. See [MusicPlayer.js](../js/audio/MusicPlayer.js) and [JournalManager.js](../js/journal/JournalManager.js) as examples of coordinators using composition.

### Viewer Pattern

All 3D/video viewers extend [ViewerBase.js](../js/viewers/ViewerBase.js) with lifecycle methods:
- `checkSupport()` - Verify device capabilities
- `loadDependencies()` - Lazy load libraries (Three.js, Video.js)
- `initialize()` - Setup viewer
- `render()` - Display content
- `showFallback()` - Static image fallback
- `dispose()` - Cleanup resources

## Critical Development Workflows

### Local Development
```bash
# Start server (REQUIRED for fetch/CORS with ES6 modules)
python3 -m http.server 8001
# or: npx http-server -p 8001
# or: VS Code Live Server extension

# Access at http://localhost:8001
```

### Adding Journal Entries
1. Create `journal/journal-YYYY-MM-DD-title.md` (see [TEMPLATE.md](../journal/TEMPLATE.md))
2. **After adding entries**, regenerate manifest:
   ```bash
   node scripts/generate-journal-manifest.js
   ```
3. Markdown syntax:
   - `[WORLD_INFO:...]` creates expandable dropdowns
   - Standalone images are full-width; inline images are 50%

### Building Thesis PDFs
```bash
cd thesis/submission
make all        # All PDFs
make literatur  # Literature review only
make clean      # Remove generated files
```

### PDF Handling in Literature Review
If encountering "PDF too large" errors, **automatically**:
1. Use pre-extracted `.txt` files from `thesis/academic/texts/extracted/`
2. If missing, extract with: `pdftotext "path/to/file.pdf" "texts/extracted/File.txt"`
3. Read the `.txt` file instead

## Code Conventions & Patterns

### SOLID Principles (MANDATORY)
- **Single Responsibility**: Each class has ONE clear purpose
- **Dependency Inversion**: Depend on EventBus (abstraction), not concrete classes
- **Open/Closed**: Extend via composition, not modification

### File Naming
- **Classes**: `PascalCase` (e.g., `MusicPlayer.js`, `PlaybackController.js`)
- **Utilities**: `camelCase` (e.g., `timeFormatter.js`)
- **Descriptive**: `PlayerUI.js` not `UI.js`, `JournalLoader.js` not `Loader.js`

### Constructor Injection
```javascript
constructor(container, eventBus, featureDetector) {
  this.container = container;
  this.eventBus = eventBus;
  // NO querying DOM for other components
}
```

### Disposal & Cleanup
Every component must have a `dispose()` method for cleanup:
```javascript
dispose() {
  this.eventBus.off('event:name', this.handleEvent);
  this.observer?.disconnect();
  // cleanup timers, listeners, resources
}
```

### Error Logging
```javascript
console.error('[ComponentName] Description:', error);
```

### Documentation
- JSDoc for public methods (explain WHY, not WHAT)
- Include parameter types and return values
- Self-documenting code preferred over comments

## Commit Workflow (CRITICAL)

**BEFORE committing:**
1. Open browser DevTools (Console + Network tabs)
2. Test the feature manually
3. Verify NO console errors
4. Check EventBus debug logs (enabled on localhost)
5. Test mobile viewport
6. Verify no regressions

**Commit message format:**
```
[Component] Brief description

- Detailed change 1
- Detailed change 2

Tested: [What you tested manually]
```

Example: `[Audio] Implement SOLID music player` with tests listed.

## Important Constraints

- **No bundlers/build steps** - vanilla ES6 modules only
- **No global variables** (except `window.everythingMachineApp` for debugging)
- **External libraries** (Three.js, Video.js, Anime.js) lazy-loaded via ScriptLoader
- **Respects** `prefers-reduced-motion` CSS media query for accessibility
- **Progressive enhancement** - core content works without JavaScript

## System Event Flows

**Audio**:
User clicks play → MusicPlayer.handlePlayPauseClick() → PlaybackController.togglePlay() → `playback:play` event → PlayerUI updates UI

**Navigation**:
User clicks menu → PageNavigator.showPage() → `nav:pageChanged` event → JournalManager.load()

**Journal**:
`nav:pageChanged` → Fetch manifest → Parse markdown → MarkdownParser.parse() → Render with TimelineRenderer/EntryRenderer

## Testing & Debugging

### EventBus Debug Mode
Enable on localhost in browser console:
```javascript
window.everythingMachineApp.eventBus.debugMode = true;
```

### Cache Busting
Viewers in [app.js](../js/app.js) use query params:
```javascript
import { ThreeDViewer } from './viewers/ThreeDViewer.js?v=20241223d';
```
Update version in app.js imports when making viewer changes.

## Thesis Submission Requirements

See [thesis/academic/Abgabe.md](../thesis/academic/Abgabe.md) for full requirements. Key sections:
1. **Exposé** - 1-2 pages
2. **Forschungsfrage** - 5 research questions
3. **Literaturrecherche** - ~10 papers with summaries
4. **Methodologie** - Methods & justification
5. **Dokumentation** - ~10-page paper with introduction, literature review, methodology, research, discussion

Reference: [thesis/academic/thilos-straightA-submission/](../thesis/academic/thilos-straightA-submission/) contains an A-grade submission example using similar themes (generative AI + media production).
