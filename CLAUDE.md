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

# Build thesis PDFs
cd thesis/submission && make all
```

No build step, bundler, or package.json - this is a vanilla JavaScript project with ES6 modules.

## Project Structure

```
/
├── [WEBSITE - Deployed to GitHub Pages]
│   ├── index.html, style.css     # Entry point and styles
│   ├── js/                       # ES6 modules (app.js, core/, audio/, navigation/, etc.)
│   ├── journal/                  # Markdown entries (journal-YYYY-MM-DD-title.md)
│   │   └── TEMPLATE.md           # Template for new journal entries
│   ├── content/                  # Website content pages
│   │   ├── forschungsrahmen.md   # Research framework page
│   │   └── referenzen.md         # References page
│   ├── assets/
│   │   ├── audio/, images/       # Media files
│   │   └── journal/              # Journal assets (YYYY-MM-DD-topic/)
│   └── scripts/                  # Build scripts (journal manifest generator)
│
├── [THESIS - MA Artistic Research]
│   └── thesis/
│       ├── ROADMAP.md            # Thesis progress & deadlines
│       ├── academic/             # Course materials, PDFs, required reading
│       │   ├── Abgabe.md         # Submission requirements
│       │   ├── texts/            # Literature PDFs
│       │   │   └── extracted/    # Pre-extracted .txt files (use for large PDFs!)
│       │   ├── lesson-material/  # Class slides
│       │   └── thilos-straightA-submission/  # Reference A-grade example
│       ├── submission/           # PDF generation (Makefile, LaTeX)
│       │   ├── docs/             # Markdown source files
│       │   └── references/       # bibliography.bib
│       └── literature-review/    # Systematic review workflow
│
├── [DEV DOCUMENTATION]
│   └── docs/                     # Developer docs (IMPLEMENTATION, TESTING, QUICK_START)
│
├── README.md                     # Project overview
├── CLAUDE.md                     # This file
└── WEBSITE_TODO.md               # Website feature tasks
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

When editing journal entries in `journal/`, use the template in `journal/TEMPLATE.md`:
- **Kontext**: Tool/Workflow used, intention
- **Prozess**: Input, iterations, output
- **Erkenntnisse**: Surprises, errors as features, my role vs AI
- **Weiterentwicklung**: Workflow changes, open questions, next steps

Focus on process over results, document failures, use first-person perspective.

## Academic Submission Requirements

The `thesis/academic/` folder contains materials for the MA thesis Artistic Research course. See `thesis/academic/Abgabe.md` for full details.

### Teil 1: Vorbereitung (Preparation)
| Deliverable | Details |
|-------------|---------|
| Exposé | 1-2 pages, practical project description |
| Forschungsfrage | ~5 research questions, choose one with most potential |
| Literaturrecherche | ~10 papers, APA format, 4-sentence summaries, relevance description |
| Methodologie | Description of methods and justification |

### Teil 2: Dokumentation (~10 pages paper)
1. **Einleitung** - Background, motivation, summary (funnel approach: general → specific)
2. **Stand der Forschung** - Literature review results
3. **Methodologie** - Methods used, justification, ethics discussion
4. **"Meine Forschung"** - Decisions, path to results, experiments, reflection
5. **Diskussion** - Summary, implications, limitations, outlook
6. **Literatur** - Bibliography (APA format)
7. **Anhänge** (optional) - Images, transcripts

### Reference: thesis/academic/thilos-straightA-submission/
Contains an A-grade submission example with similar theme (generative AI + media production). Key approaches:
- Autoethnographic methodology with video diary
- Iterative workflow: develop → create → reflect → refine
- Theories: "Suspension of Disbelief", "Uncanny Valley Effect"
- Literature funnel: VFX history → digital effects → AI terminology → disruptive tech theory → synthesis

## Literature Review Workflow

### PDF Processing

Literature PDFs are stored in `thesis/academic/texts/`. Pre-extracted text versions are in `thesis/academic/texts/extracted/`.

**Available texts:**
| Source | PDF | Extracted Text |
|--------|-----|----------------|
| Henke et al. (2019) - Manifest der Künstlerischen Forschung | `texts/Henke2019Manifest.pdf` | `texts/extracted/Henke2019Manifest.txt` |
| Schön (1983) - The Reflective Practitioner | `texts/Schoen1983Practitioner.pdf` | `texts/extracted/Schoen1983Practitioner.txt` |
| Borgdorff (2012) - The Conflict of the Faculties | `texts/Borgdorff2012Conflict.pdf` | `texts/extracted/Borgdorff2012Conflict.txt` |
| Frayling (1993) - Research in Art and Design | `texts/Frayling1993Research.pdf` | `texts/extracted/Frayling1993Research.txt` |
| Wall (2006) - Autoethnography | `texts/Wall2006Autoethnography.pdf` | `texts/extracted/Wall2006Autoethnography.txt` |
| Ellis (2010) - Autoethnografie | `texts/Ellis2010Autoethnografie.pdf` | `texts/extracted/Ellis2010Autoethnografie.txt` |
| Wesseling (2017) - Q&A | `texts/Wesseling2017QandA.pdf` | `texts/extracted/Wesseling2017QandA.txt` |

### Handling "PDF too large" Errors

**IMPORTANT:** When encountering "PDF too large" errors, do NOT ask the user - handle it automatically:

1. **First choice:** Use the pre-extracted `.txt` file from `thesis/academic/texts/extracted/`
2. **If no extracted text exists:** Run `pdftotext` to extract it:
   ```bash
   pdftotext "thesis/academic/texts/SomeFile.pdf" "thesis/academic/texts/extracted/SomeFile.txt"
   ```
3. **Then read the `.txt` file** instead of the PDF

The `poppler` package is installed and provides `pdftotext`, `pdfinfo`, `pdfseparate`, and other PDF tools.

### Literature Review Checkpoint

Current status of literature review work is tracked in `thesis/ROADMAP.md`. When working on literature review:
1. Check `thesis/ROADMAP.md` for current progress
2. Use extracted text files for reading sources
3. Update `thesis/ROADMAP.md` after completing work
4. Output goes to `thesis/submission/` folder
