# Everything Machine (Kepler)

Artistic Research-Projekt von Jennifer Meier (MA Medienproduktion, 2025)

Diese Website dient als interaktives Logbuch und Ausstellungsplattform für einen explorativen Prozess an der Schnittstelle von Generativer KI, Digitaler Identität und Musikproduktion.

## Projektübersicht

Künstler verfügen über eine Fülle von "Inputs" – nicht nur Bilder, sondern auch Musik, Texte und einen schwer fassbaren "Vibe". Generative KI bietet neue "Output"-Werkzeuge, doch es fehlt an etablierten Prozessen, diese Inputs zur Erweiterung einer bestehenden digitalen Identität zu nutzen. Diese Arbeit untersucht dies in einem explorativen Artistic Research-Prozess am Fallbeispiel des Alter Egos "Kepler".

## Projektstruktur

```
everything-machine/
│
├── [WEBSITE - Deployed to GitHub Pages]
│   ├── index.html              # Haupt-HTML-Datei
│   ├── style.css               # Benutzerdefinierte Stile
│   ├── js/                     # ES6 JavaScript Module
│   │   ├── app.js              # Haupt-Orchestrator
│   │   ├── core/               # EventBus, FeatureDetector, ScriptLoader
│   │   ├── audio/              # Musik-Player-System
│   │   ├── navigation/         # Seitennavigation
│   │   ├── journal/            # Journal-Rendering
│   │   ├── viewers/            # 3D/Video Viewer
│   │   ├── animations/         # Floating-Animationen
│   │   ├── media/              # LazyLoader, ImageGallery
│   │   └── ui/                 # UI-Komponenten
│   ├── journal/                # Markdown Journal-Einträge
│   │   ├── TEMPLATE.md         # Vorlage für neue Einträge
│   │   └── journal-*.md        # Einträge (Format: journal-YYYY-MM-DD-titel.md)
│   ├── content/                # Website-Inhalte (Markdown)
│   │   ├── forschungsrahmen.md # Forschungsrahmen-Seite
│   │   └── referenzen.md       # Referenzen-Seite
│   ├── assets/
│   │   ├── images/             # Projektbilder
│   │   ├── audio/              # Musik-Dateien
│   │   └── journal/            # Journal-Assets
│   └── scripts/                # Build-Scripts (journal-manifest.js)
│
├── [THESIS - MA Artistic Research]
│   └── thesis/
│       ├── ROADMAP.md          # Thesis-Fortschritt & Deadlines
│       ├── academic/           # Kursmaterialien, PDFs, Pflichtlektüre
│       ├── submission/         # PDF-Generierung (Makefile, LaTeX)
│       │   ├── docs/           # Markdown-Quelldateien
│       │   └── references/     # bibliography.bib
│       └── literature-review/  # Systematic Review Workflow
│
├── README.md                   # Diese Datei
├── CLAUDE.md                   # AI-Entwicklungsrichtlinien
└── WEBSITE_TODO.md             # Website Feature-Tasks
```

## Technische Umsetzung

Statische Website optimiert für GitHub Pages:

- **HTML5**: Semantische Struktur
- **CSS3**: Benutzerdefiniertes Dark-Theme ("Kepler Vibe") mit IBM Plex Mono Font
- **Tailwind CSS**: Per CDN für Utility-Klassen
- **JavaScript**: Modular ES6+ mit SOLID-Prinzipien und EventBus-Architektur

## Lokale Entwicklung

```bash
# Repository klonen
git clone https://github.com/jenniferied/everything-machine.git
cd everything-machine

# Lokalen Server starten (erforderlich für fetch/CORS)
python3 -m http.server 8001
# oder: npx http-server -p 8001
# oder: VS Code Live Server Extension

# Im Browser öffnen
open http://localhost:8001
```

### Journal-Manifest generieren

Nach dem Hinzufügen neuer Journal-Einträge:
```bash
node scripts/generate-journal-manifest.js
```

### Thesis PDFs generieren

```bash
cd thesis/submission
make all        # Alle PDFs bauen
make literatur  # Nur Literaturrecherche
make clean      # Generierte Dateien löschen
```

## Architektur

Alle Features sind als ES6-Module mit klaren Verantwortlichkeiten und Dependency Injection implementiert:

- **EventBus**: Zentrale Pub/Sub-Kommunikation
- **Single Responsibility**: Jedes Modul hat eine klar definierte Aufgabe
- **Dependency Inversion**: Abhängigkeiten von Abstraktionen, nicht konkreten Klassen

Siehe [CLAUDE.md](CLAUDE.md) für Details.

## Veröffentlichung auf GitHub Pages

1. Änderungen in das Repository pushen
2. Repository Settings > Pages öffnen
3. Source: `Deploy from a branch` wählen
4. Branch: `main`, Ordner: `/ (root)`
5. Nach wenigen Minuten ist die Website unter der generierten URL erreichbar
