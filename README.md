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
- **JavaScript**: Natives ES6+ für SPA-ähnliche Seitennavigation

## Projektstruktur

```
├── index.html          # Haupt-HTML-Datei
├── style.css           # Benutzerdefinierte Stile
├── scripts.js          # JavaScript-Logik
├── README.md           # Diese Datei
└── assets/
    ├── images/         # Projektbilder
    └── videos/         # Videos
```

## Lokale Entwicklung

1. Repository klonen
2. Assets hinzufügen: Bilder und Videos in den entsprechenden `assets/`-Ordnern ablegen
3. Pfade in `index.html` anpassen
4. Lokale Vorschau: `index.html` direkt im Browser öffnen oder einen lokalen Server verwenden (z.B. VS Code Live Server)

## Veröffentlichung auf GitHub Pages

1. Änderungen in das Repository pushen
2. Repository Settings > Pages öffnen
3. Source: `Deploy from a branch` wählen
4. Branch: `main`, Ordner: `/ (root)`
5. Nach wenigen Minuten ist die Website unter der generierten URL erreichbar
