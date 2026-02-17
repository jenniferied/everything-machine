# ROADMAP: Everything Machine

> *Kepler's identity workshop — emergent aesthetics through human-AI collaboration*

## Thesis-Abschluss (Stand 2026-02-17)

**Status: Haupttext fertig. 6 Experimente dokumentiert. 21 Zitate im Haupttext.**

### Erledigt
- [x] Sections 4 (Dokumentation) + 5 (Diskussion) geschrieben
- [x] Abstract, Zusammenfassung, Ethische Überlegungen
- [x] Practice-led throughout, Borgdorff 3×, Frayling 1993
- [x] Experiment 5 (fal.ai Pipeline) + Experiment 6 (Video) dokumentiert
- [x] TroublingGAN (Hámošová) in Exp 6 eingebaut
- [x] Quellenbasis: 21 unique Zitate (Ziel 15-20 übertroffen)
- [x] Identitätstheorie: Turkle "identity workshop" in Einleitung
- [x] Journal-Zitate inline in Beobachtungen
- [x] [N]-Platzhalter → "sechs" Experimente
- [x] "Garbage in, garbage out" von 4× auf 2× reduziert
- [x] Audio-Links: Alle PLATZHALTER entfernt
- [x] "Inweit" Typo behoben
- [x] PDF-Pipeline: Pandoc + LuaLaTeX, APA CSL

### Offen — HOCH
- [ ] **Leerer Journaleintrag** — "KI wirklich verstehen – Teil 2" (nur Intro)
  - Option A: `/reflection-interview` | Option B: Aus Anhang entfernen

### Offen — NIEDRIG
- [ ] Teil-1-Dokumente auf Konsistenz prüfen (Exposé, Forschungsfrage, Lit, Methodo)
- [ ] GLB-Dateigröße optimieren (49MB)
- [ ] Präsentation weiter bearbeiten (`presentation/index.html`)

---

## Experiment 5: Fal.ai Agentic Kepler Pipeline (abgeschlossen)

> **7 Phasen, 134+ Bilder, ~$10 Budget** | Scripts: `experiments/fal-pipeline/`

### Ergebnisse
- **FLUX Kontext [pro]** + **GPT-Image-1.5**: Beste Modelle (kein Gesicht, Voxel erhalten)
- **KeplerPosed > A-Pose**: Casual Pose = bessere Szenenintegration
- **Depth-basierte Kontrolle** ist Schlüssel (vs. Canny = Face-Halluzination)
- **3 Signature Scenes**: Night Drive, Spiral Staircase, Pool Floaty

### Phasen (alle abgeschlossen)
| Phase | Was | Status |
|-------|-----|--------|
| 1 | Schnelle Tests (5 Modelle) | ✅ |
| 2 | Top-Modelle (FLUX Kontext, GPT-1.5, SeedDream, NanoBanana) | ✅ |
| 2b | KeplerPosed Vergleich (15/15) | ✅ |
| 3/3b | Signature Scenes (bugfix iterations) | ✅ |
| 3d | Padded Inputs (7/16 — Balance leer) | ⚠️ partial |
| 3e | Refined Scenes Posed (24/24) | ✅ |
| 3f | A-Pose Vergleich (24/24) | ✅ |

### Nicht umgesetzt (deprioritized)
- Phase 5: Hallucination Cleanup (nicht nötig — genug gute Bilder)
- Phase 6: Video Generation (stattdessen → Experiment 6 als separater Test)

---

## Experiment 6: Video-Generierung (abgeschlossen)

> **Script:** `experiments/fal-pipeline/run_video_test.py` | **CSV:** `video_test_02_bewertung.csv`

- 7 Modelle × 4 Szenen = 28 Videos
- **Kling O3** best (3/4 Gut), **LTX-2** worst
- Portrait-Inputs deutlich schwieriger als Landscape
- Dokumentiert in Thesis Exp 6 mit Bewertungstabellen

---

## Website (Stand 2026-02-17)

### Erledigt
- [x] EventBus-Architektur, Journal-System, Music Player
- [x] AudioViewer, PointCloud + 3D Viewer
- [x] Chat-Bubble-Format, Matrix-Ästhetik
- [x] Bugs: AudioViewer Resize, Gallery Nav, Refresh Glitch

### Offen
- [ ] GLB 49MB optimieren

---

## Reflexionen

| Journal | Status |
|---------|--------|
| referenzen-sammeln | ✅ |
| comfyui-consistent-character | ✅ |
| marble-worldlabs | ✅ |
| cursor-build | ✅ |
| ki-verstehen | ✅ |
| suno-experiment | ✅ |
| ki-verstehen-teil-2 | ⬜ nur Intro |

---

## Key Files

| Bereich | Pfad |
|---------|------|
| Haupttext | `thesis/submission/docs/04-dokumentation.md` |
| Forschungsfrage | `thesis/submission/docs/01-forschungsfrage.md` |
| Literatur | `thesis/submission/docs/02-literaturrecherche.md` |
| Methodologie | `thesis/submission/docs/03-methodologie.md` |
| Abgabe-Anforderungen | `thesis/academic/Abgabe.md` |
| Bibliography | `thesis/submission/references/bibliography.bib` (29 Einträge) |
| Pipeline Scripts | `experiments/fal-pipeline/` |
| Video Test | `experiments/fal-pipeline/run_video_test.py` |

---

## Forschungsfrage

> Wie verändert der Einsatz multimodaler KI-Systeme (Text, Bild, Audio) den kreativen Prozess bei der Entwicklung einer digitalen Künstleridentität?

**5 Subfragen:** Workflow, Autorschaft, Iteration, Scheitern, Ästhetik
