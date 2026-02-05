# ROADMAP: Everything Machine

> *Kepler's identity workshop — emergent aesthetics through human-AI collaboration*

## 📋 Aktive Aufgaben

### Literature Review (2026-01-22) ✅
| Domain | Papers | Downloaded | Missing | Status |
|--------|--------|------------|---------|--------|
| Human-AI Collaboration | 8 | 5 | 3 | ✅ Search + download |
| Digital Identity / Virtual Personas | 9 | 1 | 8 | ✅ Search + download |
| Generative Art Theory | 10 | 5 | 5 | ✅ Search + download |
| Practice-Based Research | 7 | — | — | ✅ Already have |
| **Total** | **27** | **11** | **16** | |

**Downloaded (11):** Shneiderman 2007, Deterding 2017, Rezwana & Maher 2022, Ha & Eck 2018, Wang 2023, Molin & Nordgren 2019, Galanter 2003, Colton & Wiggins 2012, Jordanous 2012, Elgammal 2017, Gatys 2016

**Missing (16) — need university proxy:**
- Davis 2016 (Co-Creative Design) — ACM
- Koch 2019 (Creative AI) — ACM
- Turkle 1984, 1995 — books (library)
- Arsenyan & Mirowska 2021, Mori 2012, Sands 2022, Thomas & Fowler 2021 — journals
- boyd 2014 — book (library)
- Boden 1990, 1998 — book + Elsevier
- McCormack 2012, 2019, Colton 2012 (Painting Fool) — Springer chapters

See full list: `thesis/literature-review/papers-index.md`

**Files:**
- `thesis/literature-review/papers-index.md`
- `thesis/literature-review/outputs/*.md`

**iCloud:** `~/Library/Mobile Documents/com~apple~CloudDocs/papers/everything-machine/`

**PDF Download Strategy:**
1. **Author websites** — search `[author] [title] PDF site:[university].edu`
2. **University repositories** — White Rose, Kent, DiVA, Figshare
3. **Conference sites** — computationalcreativity.net, ICCC proceedings
4. **arXiv** — ML/AI papers (best coverage)
5. **OpenAlex API** — check `is_oa:true` before searching
6. **University proxy** — for ACM, Springer, Elsevier (see below)

**Using University Proxy:**
- Log in via TH OWL library portal → EZproxy
- Download PDFs through proxy, then give me the files to organize
- Or: use browser extension (EZproxy Redirect) for direct downloads

### Thesis
| Task | Status |
|------|--------|
| KI-Experimente durchführen & dokumentieren | 🔄 |
| Interviews mit Gavin | 🔄 |
| Assets sammeln (MP3s, Portrait-Reels) | ⬜ |
| Video-Reflexion aufnehmen | ⬜ |
| Paper schreiben (~10 Seiten) | ⬜ |
| 3D-Renders → Gaussian Splat Generator testen | ⬜ |

### Website Features
| Feature | Status |
|---------|--------|
| Splat Viewer fertigstellen | ⬜ |
| Point Cloud Viewer | ⬜ |
| Alle Unterseiten reviewen | ⬜ |

### Reflexionen mit /reflection-interview
| Journal | Status |
|---------|--------|
| referenzen-sammeln | ✅ |
| comfyui-consistent-character | ✅ |
| marble-worldlabs | ✅ |
| cursor-build | ✅ |
| ki-verstehen | ✅ |
| suno-experiment | ✅ |

---

## 🔧 Website Bugs

| Bug | Details |
|-----|---------|
| ~~AudioViewer Bubble Resize~~ | ✅ Fixed with ResizeObserver |
| ~~Gallery-Navigation~~ | ✅ Fixed: Chat avatars excluded |
| ~~Refresh Glitchy~~ | ✅ Fixed: unregisterGallery() added |

---

## 📅 Deadlines

| Datum | Was |
|-------|-----|
| ✅ 30.10.2025 | Exposé |
| TBD | Lightning-Talk |
| Ende Semesterferien | Teil 2: Dokumentation |

---

## 📁 Key Files

| Bereich | Pfad |
|---------|------|
| Forschungsfrage | `submission/docs/01-forschungsfrage.md` |
| Literatur | `submission/docs/02-literaturrecherche.md` |
| Methodologie | `submission/docs/03-methodologie.md` |
| Abgabe-Anforderungen | `academic/Abgabe.md` |

---

## 📝 Retrospektiven

### 2026-01-13: Roadmap Skill & Session Management
- Created `/roadmap` skill for interactive task selection
- Learning: Interactive tasks (interviews) work better in dedicated sessions, not sub-agents
- Interviews continuing in separate chat window

### 2026-01-13: Website Bugs Fixed
- AudioViewer Bubble Resize → ResizeObserver solution
- Gallery Chat Avatars → Filter `.chat-avatar` images
- Refresh Glitchy → Added `unregisterGallery()` method

### 2026-01-12: AudioViewer & Suno
- Journal "Suno-Experiment" + AudioViewer-Komponente erstellt

### 2026-01-11: Chat-Format & Interview-Skill
- Chat-Bubble-Styling, Reflection Interview Skill

---

## ✅ Erledigt

### Thesis
- [x] Phase 0: Grundlagen komplett
- [x] Exposé, Forschungsfrage, Literaturrecherche, Methodologie
- [x] Literature Review (Agent-based)
- [x] Pflichtlektüre (7 Texte): Borgdorff, Henke, Schön, Frayling, Wall, Ellis, Wesseling
- [x] Reflection Interview Skill

### Website
- [x] EventBus-Architektur
- [x] Journal-System
- [x] Music Player
- [x] AudioViewer-Komponente
- [x] Matrix-Ästhetik
- [x] Animierte Texte / Typing-Effekte
- [x] Chat-Bubble-Format
- [x] content/forschungsrahmen.md
- [x] content/referenzen.md
- [x] Journal-Template

**Forschungsfrage:**
> Wie verändert der Einsatz multimodaler KI-Systeme (Text, Bild, Audio) den kreativen Prozess bei der Entwicklung einer digitalen Künstleridentität?

**Kernerkenntnisse Artistic Research:**
- Frayling (1993): Research INTO / THROUGH / FOR art
- Borgdorff (2012): Kunstpraxis als epistemologischer Ort
- Henke (2019): "Ästhetisches Wissen" als Erkenntnisform
- Schön (1983): Reflection-in-Action als Methode
