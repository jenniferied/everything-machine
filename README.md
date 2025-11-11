{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Everything Machine \'97 Minimal Site (Kepler)\
\
**Kurz:** Ein dunkles, GitHub Pages-bereitbares Prozesslog f\'fcr k\'fcnstlerisch-wissenschaftliche Forschung. Eintr\'e4ge in Markdown, lokale Speicherung (localStorage), Export/Import als JSON.\
\
## Struktur\
- `index.html` \'97 Startseite / Single-page\
- `style.css` \'97 Design / Dark palette\
- `scripts/markdown.js` \'97 Einfacher Markdown-Renderer\
- `everything-machine-export.json` \'97 (optional) Exportdatei aus UI\
\
## Lokale Nutzung\
1. Alle Dateien in einen Ordner legen.\
2. `index.html` im Browser \'f6ffnen (Chrome empfohlen).\
3. Neue Eintr\'e4ge: "Neuer Eintrag" \uc0\u8594  Markdown schreiben \u8594  Speichern.\
4. Export \uc0\u8594  JSON herunterladen. Import \u8594  JSON wiederherstellen.\
\
## GitHub Pages Deploy\
1. Neues Git-Repository anlegen (lokal oder auf GitHub).\
2. Dateien committen:\
   ```bash\
   git init\
   git add .\
   git commit -m "Everything Machine \'97 initial site"\
   git branch -M main\
   git remote add origin <DEIN_REMOTE_URL>\
   git push -u origin main\
}