# Spiral Staircase Video — Projektstand

Stand: 2026-05-18 · Verzeichnis: `experiments/fal-pipeline/`

## Ziel
Aus dem alten Bild `outputs/18_nanobanana_v2_landscape/spiral_staircase.png` (Voxel-Charakter
auf glühender Treppe im Kosmos) ein **loopbares 16:9 Video** machen, in dem der Charakter
nach oben steigt — ohne dass Cap, Gesicht oder Treppen-Stufen morphen.

---

## Aktuell bestes Asset

| Typ | Datei | Notiz |
|---|---|---|
| Basis-Bild | `outputs/spiral_upscale/spiral_upscale_clarity_edited.png` | 2752×1536, manuell von Jennifer nachbearbeitet. **Das ist der Input für alle weiteren Generationen.** |
| Bestes Video bisher | `outputs/spiral_videos/kling3_pro_loop_20260513_003513.mp4` und `kling3_pro_loop_20260513_015425_v4.mp4` | "Not bad" — Treppe rotiert, Cap bleibt Cap, aber Stufen slippen manchmal |
| Pwnisher Greyplate (16:9 re-rendered) | `outputs/ea_greyplate/ea_greyplate_16x9.mp4` | **Framing noch off** — muss Kamera angepasst werden |

---

## Bild-Generierung — was funktioniert / nicht funktioniert

### Funktioniert
- **`fal-ai/nano-banana-pro/edit`** mit `aspect_ratio: "16:9"` und Source-Bild als `image_urls` → behält Composition + Color Grading, ändert nur was prompted ist
- **Clarity Upscaler** (`fal-ai/clarity-upscaler`) mit `creativity: 0.25, resemblance: 1.0` → bringt echte Schärfe ohne Cap zu mutieren
- Prompt explizit: *"The staircase is NOT marble. The steps themselves are luminous — they emit a soft warm-white light from within, like frosted glass lit from inside."*

### Funktioniert nicht / Müll
- **Topaz Upscale** (`fal-ai/topaz/upscale/image`) — zu konservativ, JPG-Komprimierungs-Look bleibt
- **CCSR** — okay, aber Clarity gewinnt klar
- Prompts mit "marble" → Modell macht's wieder zu Marmor
- Prompts mit "neon" / "multi-color" / "cyan, purple, pink" → buntes Neon-Disaster
- "softly glowing" allein war zu zahm → Modell ignorierte den Glow

---

## Video-Generierung — Modell-Ratings

### Gut
- **Kling 3 Pro Loop** (`fal-ai/kling-video/v3/pro/image-to-video`) mit `cfg_scale: 0.9`, Start=End-Frame, "ENTIRE staircase rotates as one rigid unit" — bestes Resultat bisher
- **Kling O3** war früher in `video_test_02` der Spiral-Sieger ("Leuchten gefällt", "Gut")

### Mittel / Mixed
- **Veo 3.1 Fast** — Kamera bewegt sich (interessant!), aber Charakter morpht stark
- **Kling 3 Pro Endframe-Lock** (Start=End identisch, ohne explizite Motion) — Cap bleibt, aber kein Movement
- **Seedance 1.0 Pro** — war früher okay für Night-Drive, weniger gut für Spiral

### Schlecht / Müll
- **Sora 2 Pro** — Cap wurde zu Bowler Hat / Bowl-Hat. Vermeiden.
- **Seedance 1.5 Pro** — selbes Cap-Morph Problem
- **Kling 3 Pro Standard V3** (NICHT Pro) — Stufen + Leuchten + Kamerabewegung waren komisch
- **LTX-2** — Aspect Ratio änderte sich, Charakter lief von Stufe
- **PixVerse v5.5** — Gesicht-Generierung, instabil

---

## Strategien (von Jennifer probiert / priorisiert)

### Strategie 1 — Rotating World, Character marches in place [bisheriger Champion]
- Welt rotiert um Charakter, Charakter bleibt zentriert
- Start=End Frame → Loop
- Kling 3 Pro, `cfg_scale: 0.9`
- **Pro:** Loopbar, Treppe rotiert sichtbar
- **Contra:** Stufen slippen, manchmal nur untere Hälfte rotiert
- Script: `run_spiral_loop.py`

### Strategie 2 — Camera Orbit 360° + natural walk [unbewertet]
- Kamera orbitet um die Treppe, Charakter läuft natürlich
- Welt physikalisch statisch
- Start=End Frame, 10s
- **Pro:** Charakter muss nicht künstlich marschieren
- **Contra:** weniger getestet
- Script: `run_spiral_orbit.py` — Outputs vom 18.05.: `kling3_pro_orbit_20260518_180202_v1/v2.mp4`, `kling_o3_orbit_20260518_180202.mp4`

### Strategie 3 — Pwnisher Eternal Ascent Greyplate als Vid2Vid Reference [NEU, in Arbeit]
- Pwnishers offizielles Walk-Loop-Template (5s, 24fps, perfekter Loop) als Motion-Reference
- Greyplate via Blender auf 16:9 re-rendern (statt original 9:16 Portrait)
- Dann Vid2Vid (Runway Aleph / Wan / Kling Effects) mit unserem Spiral-Bild als Style
- **Pro:** Garantierter Loop, garantiert sauberer Walk, kein Cap-Morph
- **Contra:** Framing der re-renderten Greyplate sitzt noch nicht, muss Kamera anpassen
- Files: `inputs/eternal_ascent/Eternal Ascent Starter Files v4/`
- Render-Script: `blender/render_greyplate_16x9.py`

---

## Was als nächstes ansteht

1. **Greyplate-Kamera anpassen** so dass Framing zu `spiral_upscale_clarity_edited.png` passt:
   - aktuell: Standard EA-Kamera, 85mm, Sensor jetzt landscape 36×20.25mm
   - Zielwinkel/Distanz/Höhe sind unbekannt — entweder per Trial-and-Error oder via Blender MCP live anpassen
2. **Blender MCP testen**: ist installiert, Addon ist im Blender enabled, MCP Server muss in Blender 3D Viewport via `N` → "BlenderMCP" → "Start MCP Server" gestartet werden. Claude Code-Restart nötig damit MCP-Tools geladen werden.
3. **Vid2Vid Pipeline bauen** sobald Greyplate-Framing passt:
   - Modelle: `fal-ai/runway-aleph`, `fal-ai/wan/v2.2-a14b/vid2vid`, oder `fal-ai/kling-video/v1.6/pro/effects`
   - Output: stylisiertes Loop-Video mit Walk vom Template + Aesthetic vom Spiral-Bild

---

## Script-Übersicht

| Script | Zweck | Outputs |
|---|---|---|
| `run_spiral_neon.py` | Spiral-Bild regenerieren (16:9, soft glow) | `outputs/spiral_neon/spiral_softglow_*` |
| `run_spiral_endframe_gen.py` | End-Frame Varianten (Charakter weiter oben) | `outputs/spiral_neon/spiral_softglow_endframe_*` |
| `run_spiral_upscale.py` | Upscale-Test (Topaz/Clarity/CCSR) | `outputs/spiral_upscale/spiral_upscale_*` |
| `run_spiral_video_test.py` | I2V Multi-Model Test (kurzer Prompt) | `outputs/spiral_videos/*` |
| `run_spiral_video_endframe.py` | End-Frame Lock I2V (Start=End) | `outputs/spiral_videos/*_endlock_*` |
| `run_spiral_loop.py` | Walk-in-place + rotating stairs Loop | `outputs/spiral_videos/*_loop_*` |
| `run_spiral_orbit.py` | Camera orbit 360° + walking | `outputs/spiral_videos/*_orbit_*` |
| `blender/inspect_scene.py` | EA Blend-File Inspektion | stdout |
| `blender/render_greyplate_16x9.py` | EA Greyplate auf 16:9 re-rendern | `outputs/ea_greyplate/ea_greyplate_16x9.mp4` |

Alle Video- und Bild-Scripts schreiben **niemals über bestehende Outputs** — jeder Run kriegt
einen Timestamp.

---

## Prompts die funktionieren

### Bild-Edit (nano-banana-pro/edit)
> Edit this image. Keep the character, pose, background (space, stars, galaxies, clouds) and the overall cosmic color grading. Make these changes: 1) Reframe to a true 16:9 landscape — wider, more cinematic. 2) The character's shoes should be white. 3) The spiral staircase is NOT marble. The steps themselves are luminous — they emit a soft, even warm-white light from within, like frosted glass lit from inside. The whole staircase glows gently. Keep the glow soft and uniform — single color (warm white), not bright, not pulsing, not neon, no multi-color. The dreamy blue/purple cosmic atmosphere of the original must be preserved.

### Video Loop (Kling 3 Pro, Strategie 1)
> Endless-climb illusion. The voxel character marches in place — his legs lift and step rhythmically, but his body stays exactly in the same spot in the frame. The ENTIRE spiral staircase rotates as one single rigid object around its central vertical axis. EVERY part of the staircase rotates uniformly at the same speed — bottom, middle, AND upper part of the spiral — ALL rotate together as one unit, like a carousel. The whole spiral scrolls downward past the character, so it looks like he's endlessly ascending. The staircase glow stays constant. Stars and galaxies drift very slowly. Camera is completely static — no zoom, no pan, no tilt. He wears a baseball cap with a flat brim — cap shape stays identical throughout.

**Negative Prompt:**
> character moving up, character translating, body moving in frame, bowler hat, top hat, fedora, helmet, dome head, sphere head, hat changing shape, face features, eyes, mouth, camera movement, zoom, pan, tilt, flickering, color shift

### Settings für Kling 3 Pro Loop (beste Werte)
- `duration: "5"` (Test) oder `"10"` (Vollversion)
- `aspect_ratio: "16:9"`
- `generate_audio: false`
- `cfg_scale: 0.9`
- `start_image_url = end_image_url` (selbe Datei zweimal) → Loop garantiert
