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
| 6 | Section 4 "Meine Forschung" schreiben (~1.500 Wörter) | Subagent: Writer + Jennifer Review | ✅ |
| 7 | Section 5 "Diskussion" schreiben (~800 Wörter) | Subagent: Writer + Jennifer Review | ✅ |
| 8 | Abstract vervollständigen | Subagent: Writer | ✅ |
| 9 | Ethische Überlegungen einfügen | Subagent: Writer | ✅ |
| 10 | Finales Review + PDF bauen | Subagent: Reviewer | 🔄 (formatting iterations) |

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
| fal-ai-kepler-pipeline | ⬜ |

---

## 🎨 Experiment 9: Fal.ai Agentic Kepler Pipeline

> *Systematisches Testen von fal.ai-Modellen mit Kepler-Referenzbildern — automatisiert via Claude Code*

### Verfügbare Inputs

| Input | Datei | Beschreibung |
|-------|-------|-------------|
| **Posed (1024)** | `experiments/fal-pipeline/inputs/kepler-posed-1024.png` | **★ Bester Input** — casual Pose, 1024×1024 |
| Posed (Original) | `~/Desktop/KeplerPosed.png` | 1920×1080, aus Unreal exportiert |
| A-Pose | `assets/journal/2025-11-16-comfyui-consistent-character/reference-kepler.png` | 3840×3840 |
| A-Pose (1024) | `experiments/fal-pipeline/inputs/kepler-a-pose-1024.png` | Resized für API |
| Casual Pose | `assets/images/kepler-squatting.png` | Kepler squatting |

### Phase 1: Schnelle Tests — ABGESCHLOSSEN (15.02.2026)

> **Budget verbraucht: ~$0,50** | **Laufzeit: ~8 Min** | **Script:** `experiments/fal-pipeline/run_phase1.py`

| # | Task | Modell | Status | Ergebnis |
|---|------|--------|--------|----------|
| 1 | Era 3D Multiview | `fal-ai/era-3d` (GRATIS) | ✅ | **6 Multiviews + Normalen, Voxel-Ästhetik erhalten, kein Gesicht** |
| 2 | Z-Image ControlNet Depth | `fal-ai/z-image/turbo/controlnet` ($0,007/MP) | ✅ | **BESTES ERGEBNIS — A-Pose erhalten, kein Gesicht, gute Szenenintegration** |
| 3 | FLUX Depth Control | `fal-ai/flux-control-lora-depth` ($0,04/MP) | ✅ | Gut — A-Pose erhalten, kein Gesicht, aber Voxel-Textur teils geglättet |
| 4 | MiniMax Subject Reference | `fal-ai/minimax/image-01/subject-reference` ($0,01/Bild) | ⚠️ | Minecraft-Stil, halluziniert quadratische Augen, Pose geändert |
| 5 | FLUX Canny Control | `fal-ai/flux-control-lora-canny` ($0,04/MP) | ❌ | **FAIL — halluziniert volles menschliches Gesicht** |

#### Phase 1 Erkenntnisse

- **Depth-basierte Modelle** sind der Schlüssel: Tiefenkarten enthalten nur Geometrie, kein Face-Signal
- **Canny/Kanten** reichen NICHT: Genug Struktur für das Modell, ein Gesicht hineinzuinterpretieren
- **Subject-Reference** (MiniMax) "Minecraft-ifiziert" Kepler — behält blockigen Stil, fügt aber Gesichtszüge hinzu
- **Z-Image Turbo ControlNet** ist 6x günstiger als FLUX und liefert bessere Ergebnisse
- **Era 3D** funktioniert, aber unnötig — Multiviews können manuell in Unreal generiert werden

#### Korrekte API-Parameter (verifiziert)

```python
# Z-Image: image_url + preprocess="depth"
# FLUX Depth/Canny: control_lora_image_url
# MiniMax Subject: image_url + aspect_ratio
# Era 3D: image_url
```

### Phase 2: Thesis-Top-Modelle — ABGESCHLOSSEN (15.02.2026)

> **Budget verbraucht: ~$0,80** | **Laufzeit: ~4 Min** | **Script:** `experiments/fal-pipeline/run_phase2.py`

| # | Task | Modell | Status | Ergebnis |
|---|------|--------|--------|----------|
| 6 | **FLUX Kontext [pro]** | `fal-ai/flux-pro/kontext` ($0,04) | ✅ | **★ GESAMTSIEGER — Voxel perfekt, kein Gesicht, neue Posen (sitzen, laufen, performen)** |
| 7 | **GPT-Image-1.5 edit** | `fal-ai/gpt-image-1.5/edit` (~$0,04) | ✅ | **★ #2 — Voxel erhalten, kein Gesicht, neue Posen, Publikum auf Bühne** |
| 8 | **SeedDream v4.5 edit** | `fal-ai/bytedance/seedream/v4.5/edit` ($0,04) | ⚠️ | Stärkste Voxel-Ästhetik, aber halluziniert volles Gesicht (Augen, Nase, Mund) |
| 9 | **NanoBanana Pro edit** | `fal-ai/nano-banana-pro/edit` ($0,15) | ⚠️ | Gemischt — Voxel teils verwässert, Gesichtszüge teils sichtbar, teuer |

#### Phase 2 Erkenntnisse

- **FLUX Kontext [pro]** ist der beste Ansatz für Kepler→neue Szene: explizit für Character Consistency ohne Fine-Tuning gebaut
- **GPT-Image-1.5** überraschend stark — als "Editor" positioniert, aber generiert Kepler zuverlässig in komplett neuen Szenen
- **SeedDream v4.5** hat die kantigste/blockigste Voxel-Ästhetik, kann aber Face-Bias nicht unterdrücken
- **NanoBanana Pro** lohnt sich zum 3,75-fachen Preis nicht — FLUX Kontext liefert bessere Ergebnisse
- Alle 4 Modelle generieren erfolgreich **neue Posen** (sitzen, laufen, Arme hoch) — das war die Kernfrage

#### API-Parameter Phase 2 (verifiziert)

```python
# FLUX Kontext: image_url (1 Bild) + prompt + guidance_scale
# GPT-Image-1.5: image_urls (Liste) + prompt + quality + size
# SeedDream v4.5: image_urls (Liste) + prompt ("Using character from image 1: ...")
# NanoBanana Pro: image_urls (Liste) + prompt + aspect_ratio
```

### Phase 2b: Top-3 mit KeplerPosed — ABGESCHLOSSEN (15.02.2026)

> **Budget: ~$1,15** | **15/15 Tests erfolgreich** | **Script:** `experiments/fal-pipeline/run_phase2b.py`
> **Erkenntnis: KeplerPosed (casual) ist besserer Input als A-Pose**

| # | Modell | Cyberpunk | Park/Herbst | Concert | Rooftop | Studio | Gesamt |
|---|--------|-----------|-------------|---------|---------|--------|--------|
| 10 | **FLUX Kontext** | ✅ Regen | ✅ Herbstlaub | ✅ Mic+Crowd | ✅ Skyline | ✅ Mixing-Desk | **★ Top-Tier** |
| 11 | **GPT-Image-1.5** | ✅ Neon | ✅ Parkbank | ✅ Mic+Fog | ✅ Sunset | ✅ **DAW** (schärfste Voxel) | **★ Top-Tier** |
| 12 | **NanoBanana Pro** | ✅ Neo Tokyo | ✅ Wald | ✅ Crowd | ✅ Skyline | ✅ Akustikpanels | **★ Brauchbar** |

#### Phase 2b Erkenntnisse

- **KeplerPosed > A-Pose**: Casual Pose liefert natürlichere Szenenintegration + Modelle verändern die Pose leichter
- **NanoBanana Pro jetzt brauchbar**: Mit KeplerPosed kein Face-Bias mehr (A-Pose hatte Gesichtszüge)
- **Alle 3 Modelle generieren 5 komplett unterschiedliche Szenen** ohne Fehler
- **FLUX Kontext + GPT-Image-1.5 gleichauf**: Kontext schneller (10s vs 23s), GPT schärfere Voxel-Textur
- **Empfohlene Modelle:** FLUX Kontext ($0,04, schnell), GPT-Image-1.5 ($0,04, schärfere Voxel), NanoBanana ($0,15, cinematische Szenen)

### Phase 3: Signature Scenes (Portrait 9:16 + Landscape 16:9) — ABGESCHLOSSEN (15.02.2026)

> **Budget: ~$1,84** | **16/16 erfolgreich** | **Script:** `experiments/fal-pipeline/run_phase3_scenes.py`
> **Modelle:** GPT-Image-1.5 (high quality) + NanoBanana Pro | **Input:** KeplerPosed

| Szene | GPT Portrait | GPT Landscape | NB Portrait | NB Landscape |
|-------|-------------|---------------|-------------|--------------|
| **Studio** (Mixing-Desk) | ✅ Voxel scharf, DAW | ✅ Warm, Kopfhörer | ✅ Akustikpanels | ✅ Breit, atmospheric |
| **Retro Car Bridge** (Nacht) | ✅ Mond + Berge | ✅ Convertible, Film-Grain | ✅ Dramatisch | ✅ Brücke + Stadt |
| **Spiral Staircase** (Endlos) | ✅ Träumerisch, Wolken | ✅ Galaxien | ✅ **Stärkste Voxel** | ✅ Surreal, Nebel |
| **Pool Floaty** (Vogelperspektive) | ✅ Flamingo, Caustics | ✅ Top-Down perfekt | ✅ **Bester Reel-Shot** | ✅ Palmen-Schatten |

#### Phase 3 Erkenntnisse (buggy — Phase 3b behebt)

- GPT-Sizes `1024x1792` / `1792x1024` existieren NICHT → Output war heimlich 1:1
- NanoBanana ignoriert `aspect_ratio` auf Edit-Endpoint → Input vorher resizen
- Bridge-Szene war inkonsistent, einige Bilder hatten Nasen/Sonnenbrillen

### Phase 3b: Fixed Signature Scenes — ABGESCHLOSSEN (15.02.2026)

> **Budget: ~$1,84** | **16/16 erfolgreich** | **Script:** `experiments/fal-pipeline/run_phase3b_fixed.py`

**Fixes angewandt:**
- GPT-Sizes: `1024x1536` (portrait) / `1536x1024` (landscape) — korrekte Werte
- NanoBanana: Pre-resized Inputs statt `aspect_ratio` Parameter
- Model-spezifische Prompts: Strukturiert (GPT) vs. konversationell (NanoBanana) per Chapter 4
- Stärkere Face-Negation: "NO face, NO eyes, NO nose, NO mouth, NO sunglasses"
- Bridge ersetzt durch Tokyo Rain, Pool Floaty: Donut-Ring mit Loch explizit beschrieben

| Szene | GPT Portrait | GPT Landscape | NB Portrait | NB Landscape |
|-------|-------------|---------------|-------------|--------------|
| **Studio** | ✅ DAW, Voxel scharf | ✅ Cinematic 16:9 | ✅ Akustikpanels | ✅ Warm, breit |
| **Tokyo Rain** (neu) | ✅ ラーメン-Schilder, Regen | ✅ Neon-Gasse | ✅ Neon, atmospheric | ✅ Cinematisch |
| **Spiral Staircase** | ✅ Wolken + Galaxien | ✅ Endlos-Treppe | ✅ Surreal | ✅ Space + Wolken |
| **Pool Floaty** | ✅ **Donut-Ring mit Loch** | ✅ Top-Down, Caustics | ✅ Ring-Shape | ✅ Palmenschatten |

#### Phase 3b Erkenntnisse

- **Aspect Ratios NICHT korrekt**: GPT `size` wird auf Edit-Endpoint ignoriert → Phase 3d behebt das mit padded Inputs
- **NanoBanana Input gestretcht** statt gepaddet (`sips -z` stretcht!) → Phase 3d behebt mit PIL-Padding
- **Kein Gesicht, keine Nase, keine Sonnenbrille** in allen 16 Bildern
- **GPT-Image-1.5**: Strukturierte Prompts (Background→Center→Details→Constraints) = bestes Ergebnis
- **NanoBanana Pro**: Konversationeller Stil + "IMPORTANT:" Prefix für Constraints
- **Pool Floaty Donut-Loch**: Explizit "donut shape with hole in center" nötig, sonst solide Disc
- **→ Superseded by Phase 3d** — alle Fixes dort konsolidiert

### Phase 3d: Final Signature Scenes (Padded Inputs) — TEILWEISE (15.02.2026)

> **Budget: ~$1,50 (von ~$3,70 geplant)** | **7/16 erfolgreich, 9 ausstehend (Balance leer)** | **Script:** `experiments/fal-pipeline/run_phase3d_final.py`

**Finale Fixes (alle Probleme behoben):**
- **Padded Inputs** für BEIDE Modelle (kein Stretchen mehr) — `kepler-posed-portrait-padded.png` (1024×1536), `kepler-posed-landscape-padded.png` (1536×1024)
- **GPT `size: "auto"`** — matched Input-Dimensionen, Output jetzt korrekt 1024×1536 / 1536×1024
- **NanoBanana: Padded Input + `aspect_ratio`** als Belt-and-Suspenders
- **Voxel-Treppe** statt Marmor — "blocky geometric steps, not smooth marble"
- **Donut-Ring mit Loch** — explizit "donut shape with hole in center, not solid disc"
- **Pixel-Dimensionen im Log** — `save_image()` prüft jetzt tatsächliche Output-Größe

| Szene | GPT Portrait | GPT Landscape | NB Portrait | NB Landscape |
|-------|-------------|---------------|-------------|--------------|
| **Studio** | ✅ 1024×1536 | ⬜ Balance leer | ✅ 768×1376 | ⬜ Balance leer |
| **Tokyo Rain** | ✅ 1024×1536 | ⬜ Balance leer | ✅ 768×1376 | ⬜ Balance leer |
| **Spiral Staircase** | ✅ 1024×1536 Voxel-Stufen | ⬜ Balance leer | ✅ 768×1376 | ⬜ Balance leer |
| **Pool Floaty** | ✅ 1024×1536 Donut-Loch | ⬜ Balance leer | ⬜ Balance leer | ⬜ Balance leer |

#### Phase 3d Erkenntnisse

- **GPT `size` wird auf Edit-Endpoint IGNORIERT** — `size: "auto"` + vorformatierter Input ist die einzige Lösung
- **NanoBanana `aspect_ratio` unzuverlässig** auf Edit-Endpoint — Padded Input ist Pflicht
- **`sips -z` STRETCHT** statt zu padden — PIL/Pillow mit Letterboxing verwenden
- **Voxel-Ästhetik in Prompts**: "voxel blocks", "blocky geometric" statt "marble", "smooth"
- **Alle 7 Portraits bestätigen**: Kein Gesicht, korrekte Ratio, Voxel-Stil erhalten

#### Nächster Schritt: fal.ai Balance aufladen → `run_phase3d_final.py` erneut starten (überspringt vorhandene Bilder nicht — manuell die fehlenden 9 starten oder Resume-Script nutzen)

### Phase 3e: Refined Signature Scenes (Posed Input) — ABGESCHLOSSEN (15.02.2026)

> **Budget: ~$1,50** | **24/24 erfolgreich** | **Script:** `experiments/fal-pipeline/run_phase3e_refined.py`
> **Modelle:** GPT-Image-1.5 + NanoBanana Pro | **Input:** KeplerPosed (padded)

**Verbesserungen gegenüber Phase 3d:**
- Bridge/Tokyo Rain → Night Drive (Retro-Auto, Film-Grain)
- "galaxies" → "clouds" (Spiral Staircase)
- Pool Floaty: Enriched poolside details (drink, sunscreen, magazine)
- Studio entfernt → 3 Signature Scenes final

| Szene | GPT Portrait | GPT Landscape | NB Portrait | NB Landscape |
|-------|-------------|---------------|-------------|--------------|
| **Night Drive** | ✅ Retro-Auto, Mond | ✅ Film-Grain, Highway | ✅ Neon, atmospheric | ✅ Cinematic |
| **Spiral Staircase** | ✅ Wolken, Voxel-Stufen | ✅ Endlos, surreal | ✅ Dramatic | ✅ Nebel |
| **Pool Floaty** | ✅ Donut-Ring, Drink | ✅ Top-Down, Caustics | ✅ Palmenschatten | ✅ Details |

### Phase 3f: A-Pose Vergleich — ABGESCHLOSSEN (15.02.2026)

> **Budget: ~$1,50** | **24/24 erfolgreich** | **Script:** `experiments/fal-pipeline/run_phase3f_apose.py`
> **Gleiche Prompts wie Phase 3e, aber mit A-Pose Input statt KeplerPosed**

| Szene | GPT Portrait | GPT Landscape | NB Portrait | NB Landscape |
|-------|-------------|---------------|-------------|--------------|
| **Night Drive** | ✅ | ✅ | ✅ | ✅ |
| **Spiral Staircase** | ✅ | ✅ | ✅ | ✅ |
| **Pool Floaty** | ✅ | ✅ | ✅ | ✅ |

#### Phase 3e + 3f Erkenntnisse

- **Alle 24 Bilder korrekte Dimensionen** — Padded Input + size=auto funktioniert zuverlässig
- **A-Pose vs. Posed**: Evaluierung ausstehend (→ Bewertungstabelle)
- **3 Signature Scenes final**: Night Drive, Spiral Staircase, Pool Floaty

### Phase 5: Hallucination Cleanup (~$2-4)

| # | Task | Status |
|---|------|--------|
| 1 | Favorites aus Bewertung auswählen | ⬜ |
| 2 | GPT-Image-1.5 edit: Halluzinationen gezielt korrigieren | ⬜ |
| 3 | NanoBanana edit: Alternative Korrekturen | ⬜ |
| 4 | Clean Versions für Website + Thesis | ⬜ |

### Phase 6: Video Generation (~$5-15)

| # | Task | Modell | Status |
|---|------|--------|--------|
| 1 | DreamActor v2 Motion Transfer | `fal-ai/bytedance/dreamactor/v2` | ⬜ |
| 2 | Wan 2.1 Image-to-Video | `fal-ai/wan-i2v` | ⬜ |
| 3 | Wan 2.6 Ref-to-Video | `wan/v2.6/reference-to-video/flash` | ⬜ |

### Phase 7: Documentation & Thesis Integration

| # | Task | Status |
|---|------|--------|
| 1 | Thesis-Text: Experiment 5 in 04-dokumentation.md | ⬜ |
| 2 | Journal-Eintrag #8 schreiben | ⬜ |
| 3 | Bewertungstabelle (CSV) erstellen | ⬜ |
| 4 | [N]-Platzhalter ersetzen | ⬜ |

### Erfolgskriterien

- ✅ Kepler behält Voxel-Ästhetik ohne hinzugefügtes Gesicht (FLUX Kontext, GPT-Image-1.5, Z-Image)
- ✅ Neue Posen generierbar (sitzen, laufen, performen) — FLUX Kontext + GPT-Image-1.5
- ✅ Mindestens 1 Modell liefert konsistente Ergebnisse über 10+ Variationen — Phase 3e: 24/24 erfolgreich
- ✅ Pipeline ist automatisierbar (API-basiert, Python-Script funktioniert)

### Output-Verzeichnis

```
experiments/fal-pipeline/
├── inputs/
│   ├── kepler-a-pose-1024.png
│   └── kepler-posed-1024.png       (★ bester Input)
├── outputs/
│   ├── 01_minimax_subject/          (3 — Minecraft-Stil, Gesichtszüge)
│   ├── 02_zimage_controlnet/        (3 — ControlNet depth)
│   ├── 03_flux_depth/               (3 — FLUX depth)
│   ├── 04_flux_canny/               (2 — FAIL, Gesichtshalluzination)
│   ├── 05_era3d/                    (6 — Multiviews)
│   ├── 06_flux_kontext/             (3 — A-Pose, ★ Kontext)
│   ├── 07_gpt_image_15/             (3 — A-Pose, GPT)
│   ├── 08_seeddream/                (3 — Face-Bias)
│   ├── 09_nanobanana_pro/           (3 — A-Pose, gemischt)
│   ├── 10_flux_kontext_posed/       (5 — ★★ KeplerPosed, BEST)
│   ├── 11_gpt15_posed/             (5 — ★★ KeplerPosed, schärfste Voxel)
│   ├── 12_nanobanana_posed/         (5 — ★ KeplerPosed, cinematisch)
│   ├── 13_gpt15_scenes_portrait/   (4 — ★★ Signature Scenes 9:16)
│   ├── 13_gpt15_scenes_landscape/  (4 — ★★ Signature Scenes 16:9)
│   ├── 14_nanobanana_scenes_portrait/ (4 — ★★ Signature Scenes 9:16)
│   ├── 14_nanobanana_scenes_landscape/ (4 — Signature Scenes 16:9, buggy ratios)
│   ├── 15_gpt15_fixed_portrait/     (4 — Fixed Portrait 1024×1536)
│   ├── 15_gpt15_fixed_landscape/    (4 — Fixed Landscape 1536×1024)
│   ├── 16_nanobanana_fixed_portrait/ (4 — Fixed Portrait, pre-resized)
│   ├── 16_nanobanana_fixed_landscape/ (4 — Fixed Landscape, pre-resized)
│   ├── 19_gpt15_final_portrait/     (4 — ★★★ Finale Portraits 1024×1536, padded)
│   ├── 19_gpt15_final_landscape/    (⬜ ausstehend — Balance leer)
│   ├── 20_nanobanana_final_portrait/ (3 — ★★★ Finale Portraits 768×1376, padded)
│   ├── 20_nanobanana_final_landscape/ (⬜ ausstehend — Balance leer)
│   ├── 21_gpt15_refined_portrait/     (3 — ★★★ Refined Posed 9:16)
│   ├── 21_gpt15_refined_landscape/    (3 — ★★★ Refined Posed 16:9)
│   ├── 22_nanobanana_refined_portrait/ (3 — ★★★ Refined Posed 9:16)
│   ├── 22_nanobanana_refined_landscape/ (3 — ★★★ Refined Posed 16:9)
│   ├── 23_gpt15_apose_portrait/       (3 — A-Pose Vergleich 9:16)
│   ├── 23_gpt15_apose_landscape/      (3 — A-Pose Vergleich 16:9)
│   ├── 24_nanobanana_apose_portrait/   (3 — A-Pose Vergleich 9:16)
│   └── 24_nanobanana_apose_landscape/  (3 — A-Pose Vergleich 16:9)
├── inputs/
│   ├── kepler-posed-portrait-padded.png  (1024×1536, gray padding)
│   └── kepler-posed-landscape-padded.png (1536×1024, gray padding)
├── run_phase1.py
├── run_phase1_retry.py
├── run_phase2.py
├── run_phase2b.py
├── run_phase3_scenes.py          (buggy ratios)
├── run_phase3b_fixed.py          (stretched inputs)
├── run_phase3d_final.py          (★ production-ready)
├── run_phase3e_refined.py        (★ Phase 3e — refined scenes, posed input)
└── run_phase3f_apose.py          (Phase 3f — a-pose comparison)
```

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

### 2026-02-12: Thesis Sections Written + PDF Pipeline Fixed
- Sections 4+5, Abstract, Ethik geschrieben via 3 parallele Writer-Agents + Reviewer
- 7 Runden PDF-Formatting: Überschriften, Light/Dark Theme, Zitate, Indent
- biblatex/citeproc Konflikt gelöst: biblatex entfernt, APA CSL heruntergeladen
- Noch offen: Experimente 7+8, Journal-Einträge, [N]-Platzhalter ersetzen

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
- [x] Repo-Root aufgeräumt: Test-HTMLs → testing/, style.css → dist/, manifest → journal/
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
