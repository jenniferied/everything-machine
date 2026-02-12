# ROADMAP: Everything Machine

> *Kepler's identity workshop — emergent aesthetics through human-AI collaboration*

## 📋 Thesis-Abschluss (2026-02-12 → 2026-02-14)

### Zeitplan: 2 Tage

**Tag 1 (12.02.): Experimente + Quellen**
| # | Task | Agent | Status |
|---|------|-------|--------|
| 1 | Experiment 7: FLUX 2 + PuLID Character Consistency | Jennifer (hands-on) | ⬜ |
| 2 | Experiment 8: Agentic Creative Pipeline | Claude Code schreibt Script | ⬜ |
| 3 | Journal-Einträge für Exp. 7+8 schreiben | /reflection-interview | ⬜ |
| 4 | TroublingGAN (Hámošová & Rusnák) lesen + einordnen | Subagent: Recherche | ⬜ |
| 5 | Quellen auf 7 Kern-Quellen reduzieren | Subagent: Lit Review | ⬜ |

**Tag 2 (13.02.): Synthese + Schreiben**
| # | Task | Agent | Status |
|---|------|-------|--------|
| 6 | Section 4 "Meine Forschung" schreiben (~1.500 Wörter) | Subagent: Writer + Jennifer Review | ⬜ |
| 7 | Section 5 "Diskussion" schreiben (~800 Wörter) | Subagent: Writer + Jennifer Review | ⬜ |
| 8 | Abstract vervollständigen | Subagent: Writer | ⬜ |
| 9 | Ethische Überlegungen einfügen | Subagent: Writer | ⬜ |
| 10 | Finales Review + PDF bauen | Subagent: Reviewer | ⬜ |

### Agent-Orchestrierung (Opus 4.6)

**Wie wir die Arbeit aufteilen:**

| Agent | Typ | Aufgabe |
|-------|-----|---------|
| **Orchestrator** (Hauptchat) | Opus 4.6 | Koordination, high-level Entscheidungen, Feedback |
| **Writer** | Opus 4.6 Subagent | Schreibt Sektionen auf Deutsch, autoethnographischer Stil |
| **Reviewer** | Opus 4.6 Subagent | Prüft gegen Thilos 1,0-Standard, AR-Qualität, Quellencheck |
| **Researcher** | Sonnet Subagent | Recherchiert Tools, Quellen, technische Details |
| **Experiment-Helper** | Sonnet Subagent | Schreibt Python-Scripts für Experiment 8 |

**Workflow pro Sektion:**
1. Orchestrator gibt Briefing (Struktur, Ton, Quellen)
2. Writer-Agent schreibt ersten Entwurf
3. Jennifer reviewt und gibt Feedback
4. Reviewer-Agent prüft akademische Qualität
5. Writer überarbeitet → fertig

### 7 Kern-Quellen (reduziert von 31)

| # | Quelle | Funktion in der Arbeit |
|---|--------|----------------------|
| 1 | Borgdorff (2013) | AR-Definition, Praxis als Forschung |
| 2 | Candy (2006) | Practice-based vs practice-led |
| 3 | Boden (2004) | Kreativitäts-Framework (explorativ, kombinatorisch, transformativ) |
| 4 | Ellis (2011) | Autoethnographie-Methodik |
| 5 | Schön (1983) | Reflection-in-Action |
| 6 | Mori (2012) | Uncanny Valley + Suspension of Disbelief (Coleridge) |
| 7 | TroublingGAN — Hámošová & Rusnák (JAR 31) | GAN + AR, "exposing to failure," Scheitern als Ästhetik |

### 2 Neue Experimente

**Experiment 7: FLUX 2 + PuLID Multi-Reference Character Consistency**
- Tool: ComfyUI + FLUX 2 + PuLID-Flux-II
- Ziel: Testen ob neuere Modelle (2026) Keplers Maske besser respektieren
- Erwartung: Besser als Nov 2025, aber immer noch Nischenproblem
- Dauer: ~2h
- Forschungsbeitrag: Bestätigt/widerlegt "Training Data Bias" These

**Experiment 8: Agentic Creative Pipeline**
- Tool: Claude Code + Python + FLUX API oder lokales ComfyUI
- Ziel: KI schreibt Script das automatisiert Kepler-Varianten testet
- Einzigartig: Dreistufige Kollaboration (Jennifer → Claude Code → Bildmodell)
- Dauer: ~2h
- Forschungsbeitrag: Neue Autorschaftsform "Orchestratorin"

### Reflexionen
| Journal | Status |
|---------|--------|
| referenzen-sammeln | ✅ |
| comfyui-consistent-character | ✅ |
| marble-worldlabs | ✅ |
| cursor-build | ✅ |
| ki-verstehen | ✅ |
| suno-experiment | ✅ |
| flux2-character-consistency | ⬜ |
| agentic-creative-pipeline | ⬜ |

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
