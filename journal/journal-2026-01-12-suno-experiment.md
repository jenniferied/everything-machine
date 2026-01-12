# KI-Musik für prozedurale Spielwelten: Ein Suno-Experiment

**12. Januar 2026**

Heute ein kleines Experiment außerhalb des Kepler-Kontexts. Ich arbeite an einem anderen Projekt – einer prozedural generierten Spielwelt mit sowjetischer Ästhetik – und wollte testen, wie gut KI-Musikgenerierung für spezifische Game-Audio-Anforderungen funktioniert.

![Houdini-Workflow mit den drei prozeduralen Generatoren: terrain_generator, building_generator und street_generator für die sowjetisch inspirierte Spielwelt.](assets/journal/2026-01-12-suno-experiment/houdini-generators.png)

## Prozeduralismus und Pattern-basiertes Design

Das Projekt "ПАНЕЛЬКИ" (Panelki) ist eine Masterarbeit über prozedurale Weltgenerierung. Der Kern: Anstatt jeden Straßenzug manuell zu platzieren, definiere ich *Regeln* und *Muster*, aus denen die Welt emergent entsteht. In Houdini habe ich drei HDAs (Houdini Digital Assets) entwickelt:

- **terrain_generator**: Echte Höhendaten aus Neryungi, Russland (ALOS PALSAR DEM)
- **building_generator**: Modulare Chruschtschowka-Architektur aus OSM-Footprints
- **street_generator**: Straßennetzwerke, die die Gebäude verbinden

Das Ergebnis ist eine dystopische Winterstadt, bevölkert von anthropomorphen Tierfiguren im Stil sowjetischer Zeichentrickfilme.

![Konzeptkunst: Wolf unter einer Straßenlaterne im ewigen Winter.](assets/journal/2026-01-12-suno-experiment/concept-wolf-streetlamp.png)

## KI-Musik: Näher an "professional quality" als Bilder?

Was mich zu diesem Experiment gebracht hat: Ich höre seit einiger Zeit kommerziell produzierte Musik und bin überrascht, wie viel davon inzwischen KI-generiert ist – ohne dass es auffällt. Bei Bildern und Videos sehe ich noch deutliche Artefakte und Inkonsistenzen. Bei Audio? Erschreckend nah am professionellen Standard.

Suno ist aktuell der Marktführer:
- **Version 4.5** (kostenlos) bzw. **v5** (Pro, $10/Monat)
- Studioqualität bei 44.1 kHz
- 8-minütige Songs möglich
- Vollständige Arrangements mit Vocals

Warner Music hat bereits einen Deal abgeschlossen. Sony klagt noch. Die Musikindustrie ist nervös – und ich verstehe warum.

## Das Experiment: Zwei Prompts

Ich brauchte Hintergrundmusik für ein Pixel-Game: loopbar, atmosphärisch, sowjetisch-dystopisch. Keine Vocals. Also habe ich zwei Ansätze getestet.

### Versuch 1: "Lo-fi"

<div data-audio-viewer
     data-prompt="Soviet-inspired dystopian winter lo fi game music loop, no vocals"
     data-artist="Suno AI v4.5"
     data-tracks='[
       {"src": "assets/journal/2026-01-12-suno-experiment/red-snow-protocol.mp3", "title": "Red Snow Protocol", "cover": "assets/journal/2026-01-12-suno-experiment/red-snow-protocol-cover.jpg", "description": "Cold-war lo-fi loop with dusty vinyl crackle, tape-warbled strings, and a low, pulsing bass. Minimal piano figures trade with distant metallic hits, like factory echoes under falling snow. Muffled snare and soft rim knocks keep a slow, hypnotic groove; saturated synth pads swell in and out to suggest looming surveillance. Arrangement cycles subtly so it can loop seamlessly in-game, building a quiet, relentless tension."},
       {"src": "assets/journal/2026-01-12-suno-experiment/frozen-terminals.mp3", "title": "Frozen Terminals", "description": "Glacial lo-fi loop built on a bed of detuned tape-warped synth strings and distant radio static. A sparse, muted kick-and-rim pattern pulses like a frozen heartbeat, while an icy Rhodes piano plays melancholic two-note motifs. Reverb-drenched pads and subtle vinyl crackle add analog warmth amid the cold atmosphere. Arrangement is intentionally minimal and repetitive for seamless in-game looping, evoking empty corridors under flickering fluorescent lights."}
     ]'>
</div>

**Ergebnis:** Klingt zu kommerziell. "Lo-fi" war der falsche Begriff – ich wollte etwas Minimalistischeres, Roheres. Die generierte Beschreibung klingt besser als der tatsächliche Output.

### Versuch 2: "Minimal"

<div data-audio-viewer
     data-prompt="pixel game soundtrack, soviet inspired, winter and snow, dystopian and lonely, slow, minimal, no vocals"
     data-artist="Suno AI v4.5"
     data-tracks='[
       {"src": "assets/journal/2026-01-12-suno-experiment/frozen-relay.mp3", "title": "Frozen Relay", "description": "Bitcrushed chiptune pads over a sparse, detuned synth choir; slow, mechanical pulse with occasional metallic hits and distant wind FX. Melody is minimal and repetitive, using cold-square leads and low, droning bass. Reverb-drenched bells hint at Soviet-era clock towers in a buried city, with the energy staying restrained and lonely throughout; mix is narrow and mono-leaning, like an aging arcade cabinet in an abandoned bunker."},
       {"src": "assets/journal/2026-01-12-suno-experiment/iron-frost-protocol.mp3", "title": "Iron Frost Protocol", "description": "Sparse 8-bit pads drift over a muted, dusty beat, while detuned synth strings add a ghostly Soviet-era chill. A simple, repetitive melody plays on cold square-wave leads, occasionally punctuated by distant metallic chimes and lo-fi static. Slow tempo and limited note range evoke isolation and decay. The arrangement is intentionally monotonous, looping seamlessly as if echoing through an abandoned Siberian facility."}
     ]'>
</div>

**Ergebnis:** Näher dran. "Minimal" funktioniert besser als "lo-fi". Aber immer noch nicht ganz das, was ich im Kopf hatte. Die Beschreibungen sind evokativ ("aging arcade cabinet in an abandoned bunker"), der Sound selbst bleibt generisch.

## Die Beschreibungs-Output-Diskrepanz

![Pixel-Art-Ästhetik: Das Schaf auf sowjetischer Straße – genau dieser Stil bräuchte passende Musik.](assets/journal/2026-01-12-suno-experiment/concept-sheep-pixel.png)

Was auffällt: Suno generiert wunderbar detaillierte Beschreibungen. "Bitcrushed chiptune pads over a sparse, detuned synth choir" klingt exakt nach dem, was ich will. Der tatsächliche Output? Klingt wie generische Stock-Music.

Das ist dasselbe Muster wie bei meinen ComfyUI-Experimenten mit Kepler: Ich wollte einen voxelisierten, pixeligen Charakter ohne erkennbares Gesicht. Die KI lieferte immer wieder fotorealistisch anmutende Ergebnisse, obwohl der Prompt explizit "voxel", "blocky", "no face" enthielt.

**Die Erkenntnis:** Generalistische KI-Tools sind auf kommerzielle Mehrheitsästhetik trainiert. Spezialisierte Nischen – Pixel-Game-Soundtracks, voxelisierte Charaktere – erfordern entweder:
- Sehr viele Iterationen
- Spezialisierte Fine-Tunes
- Manuelle Nachbearbeitung

Das Tool erfüllt 80% der Anforderungen sofort. Die letzten 20% – der Teil, der einen kreativen Output *einzigartig* macht – erfordern nach wie vor menschliche Expertise.

## Technische Notizen

Suno bietet zwei Modelle:
- **v4.5**: Kostenlos, 50 Credits/Tag, "previously unimaginable production capabilities"
- **v5**: $10/Monat, noch höhere Qualität, v5-Samples werden parallel angeboten

Ich habe v4.5 genutzt. Die v5-Samples, die zum Vergleich angezeigt werden, klingen tatsächlich besser – aber ohne Musikexpertise kann ich nicht genau sagen, *warum*. Es klingt "voller"? "Sauberer"? Die Unterschiede sind subtil.

---

## Reflexion

*Dieser Abschnitt folgt der autoethnografischen Methodik nach Ellis et al. (2011) und Schöns "Reflection-in-Action" (1983).*

### Kontext

- **Tool/Workflow:** Suno AI v4.5 (Web-Interface), direkte Prompt-Eingabe
- **Intention:** Ambient-Musik für prozedural generierte Spielwelt, loopbar, sowjetisch-dystopisch

### Prozess

- **Input:** Zwei Text-Prompts mit Genre-, Stimmungs- und Stilangaben
- **Iterationen:** 2 Prompts × 2 generierte Tracks = 4 Ergebnisse
- **Output:** Vier Tracks zwischen 10 Sekunden und mehreren Minuten, professionell produziert, aber generisch

### Erkenntnisse

- **Überraschungen:** Die generierten Beschreibungen sind oft evocativer als die Musik selbst. Suno "versteht" den gewünschten Vibe auf textueller Ebene, setzt ihn aber in einen kommerziellen Sound um.
- **Fehler als Feature:** Die "zu kommerzielle" Qualität zeigt, worauf das Modell trainiert wurde. Das ist kein Bug, sondern die logische Konsequenz aus Training auf erfolgreicher Musik.
- **Meine Rolle vs. KI:** Ich habe die kreative Vision (sowjetisch-minimalistisch), die KI liefert handwerklich solide, aber austauschbare Umsetzungen. Der *spezifische* Sound, der diese Spielwelt einzigartig machen würde, entsteht nicht automatisch.

### Weiterentwicklung

- **Workflow-Änderung:** Detailliertere Prompts mit spezifischen musikalischen Referenzen testen. "Klingt wie [Komponist X]" statt abstrakter Genre-Beschreibungen.
- **Offene Fragen:** Kann ein Fine-Tune auf 8-bit/Chiptune-Musik das Ergebnis verbessern? Lohnt sich die manuelle Nachbearbeitung (EQ, Bitcrushing) für Authentizität?
- **Nächste Schritte:** Tracks als Ausgangsmaterial nutzen und in einer DAW bearbeiten. Der "Rohstoff" ist da – die Veredelung bleibt menschliche Arbeit.

---

*Referenzen: Ellis, Adams & Bochner (2011) - Autoethnography: An Overview; Schön (1983) - The Reflective Practitioner*
