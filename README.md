# Everything Machine — Minimal Site (Kepler)

**Kurz:** Ein dunkles, GitHub Pages-bereites Prozesslog für künstlerisch-wissenschaftliche Forschung. Einträge in Markdown, lokale Speicherung (localStorage), Export/Import als JSON.

## Struktur
- `index.html` — Startseite / Single-page  
- `style.css` — Design / Dark palette  
- `scripts/markdown.js` — Einfacher Markdown-Renderer  
- `everything-machine-export.json` — (optional) Exportdatei aus UI

## Lokale Nutzung
1. Alle Dateien in einen Ordner legen.  
2. `index.html` im Browser öffnen (Chrome oder Edge empfohlen).  
3. Neue Einträge: „Neuer Eintrag“ → Markdown schreiben → Speichern.  
4. Export → JSON herunterladen. Import → JSON wiederherstellen.

## GitHub Pages Deploy
1. Neues Git-Repository anlegen (z. B. `everything-machine`).  
2. Dateien committen:  
   ```bash
   git init
   git add .
   git commit -m "Everything Machine — initial site"
   git branch -M main
   git remote add origin <DEIN_REMOTE_URL>
   git push -u origin main
