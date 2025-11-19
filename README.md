# Everything Machine (Kepler)

Artistic Research-Projekt von Jennifer Meier (MA Medienproduktion, 2025)

Diese Website dient als interaktives Logbuch und Ausstellungsplattform für einen explorativen Prozess an der Schnittstelle von Generativer KI, Digitaler Identität und Musikproduktion.

## Projektübersicht

Künstler verfügen über eine Fülle von "Inputs" – nicht nur Bilder, sondern auch Musik, Texte und einen schwer fassbaren "Vibe". Generative KI bietet neue "Output"-Werkzeuge, doch es fehlt an etablierten Prozessen, diese Inputs zur Erweiterung einer bestehenden digitalen Identität zu nutzen. Diese Arbeit untersucht dies in einem explorativen Artistic Research-Prozess am Fallbeispiel des Alter Egos "Kepler".

Die Website ist in drei Hauptbereiche gegliedert:

- **Projektübersicht**: Das formale Exposé, einschließlich Abstract, Forschungsfragen und Methodik
- **Prozess-Logbuch**: Ein detailliertes Tagebuch der technischen Experimente (ComfyUI, AnimateDiff), der Input-Analyse und der Reflexionen
- **Künstler-Dialoge**: Transkripte der semi-strukturierten Dialoge mit dem "Künstler-Klienten" (Gavin Just), die als Meilensteine des Projekts dienen

## Technische Umsetzung

Statische Website optimiert für GitHub Pages:

- **HTML5**: Semantische Struktur
- **CSS3**: Benutzerdefiniertes Dark-Theme ("Kepler Vibe") mit IBM Plex Mono Font, CSS Grid Layout
- **Tailwind CSS**: Per CDN für Utility-Klassen
- **JavaScript**: Modular ES6+ mit SOLID-Prinzipien

## Architektur

Dieses Projekt folgt konsequent SOLID-Prinzipien für wartbaren, testbaren Code:

- **Single Responsibility**: Jedes Modul hat eine klar definierte Aufgabe
- **Open/Closed**: Erweiterbar durch Komposition, nicht durch Modifikation
- **Liskov Substitution**: Alle Viewer/Player implementieren Basis-Interfaces
- **Interface Segregation**: Minimale, fokussierte Schnittstellen
- **Dependency Inversion**: Abhängigkeiten von Abstraktionen (EventBus), nicht von konkreten Klassen

Alle Features sind als ES6-Module mit klaren Verantwortlichkeiten und Dependency Injection implementiert. Siehe [IMPLEMENTATION.md](IMPLEMENTATION.md) für Details zur Architektur.

## Projektstruktur

```
├── index.html              # Haupt-HTML-Datei
├── style.css               # Benutzerdefinierte Stile
├── .cursorrules            # KI-Entwicklungsrichtlinien (SOLID)
├── README.md               # Diese Datei
├── IMPLEMENTATION.md       # Architektur-Dokumentation
├── js/                     # Modulare JavaScript-Architektur
│   ├── app.js              # Haupt-Orchestrator
│   ├── core/               # Kern-Services (EventBus, FeatureDetector, ScriptLoader)
│   ├── audio/              # Musik-Player-System
│   │   ├── MusicPlayer.js          # Haupt-Koordinator
│   │   ├── Playlist.js             # Playlist-Daten
│   │   ├── PlaybackController.js   # Wiedergabe-Logik
│   │   ├── PlayerUI.js             # UI-Updates & Marquee
│   │   └── timeFormatter.js        # Zeit-Formatierung
│   ├── navigation/         # Navigations-System
│   │   ├── PageNavigator.js        # Seitenwechsel
│   │   ├── DropdownController.js   # Dropdown-Verwaltung
│   │   └── NavigationState.js      # localStorage-Persistenz
│   ├── journal/            # Journal-System
│   │   ├── JournalManager.js       # Haupt-Koordinator
│   │   ├── JournalLoader.js        # Datei-Laden
│   │   ├── MarkdownParser.js       # Markdown → HTML
│   │   ├── TimelineRenderer.js     # Timeline-Anzeige
│   │   ├── EntryRenderer.js        # Eintrags-Darstellung
│   │   ├── TypingAnimation.js      # Tipp-Animation
│   │   ├── GridLayoutOptimizer.js  # Grid-Layout
│   │   └── WorldInfoComponent.js   # Welt-Info-Widgets
│   ├── viewers/            # 3D/Video-Viewer
│   ├── animations/         # Floating-Animationen
│   ├── media/              # LazyLoader, ImageGallery
│   └── ui/                 # UI-Komponenten (AIAttribution)
├── journal/                # Journal-Einträge (Markdown)
│   └── *.md                # Format: journal-YYYY-MM-DD-titel.md
└── assets/
    ├── images/             # Projektbilder
    ├── audio/              # Musik-Dateien
    └── journal/            # Journal-Assets
```

## Lokale Entwicklung

1. Repository klonen
2. Assets hinzufügen: Bilder und Videos in den entsprechenden `assets/`-Ordnern ablegen
3. Pfade in `index.html` anpassen
4. **WICHTIG**: Lokale Vorschau erfordert einen lokalen Server, da die Journal-Einträge per `fetch()` geladen werden (CORS-Beschränkungen bei `file://` Protokoll)
   
   **Optionen für lokalen Server:**
   - VS Code: Live Server Extension verwenden
   - Python: `python3 -m http.server 8001` im Projektverzeichnis (Port 8000 ist oft von ComfyUI belegt)
   - Node.js: `npx http-server -p 8001` im Projektverzeichnis
   - Dann im Browser öffnen: `http://localhost:8001`

## Veröffentlichung auf GitHub Pages

1. Änderungen in das Repository pushen
2. Repository Settings > Pages öffnen
3. Source: `Deploy from a branch` wählen
4. Branch: `main`, Ordner: `/ (root)`
5. Nach wenigen Minuten ist die Website unter der generierten URL erreichbar
