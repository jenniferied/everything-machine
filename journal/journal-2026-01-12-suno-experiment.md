# KI-Musik für prozedurale Spielwelten: Ein Suno-Experiment

**12. Januar 2026**

Heute ein kleines Experiment außerhalb des Kepler-Kontexts. Ich arbeite an einem anderen Projekt – einer prozedural generierten Spielwelt mit sowjetischer Ästhetik – und wollte testen, wie gut KI-Musikgenerierung für spezifische Game-Audio-Anforderungen funktioniert.

![Houdini-Workflow mit den drei prozeduralen Generatoren: terrain_generator, building_generator und street_generator für die sowjetisch inspirierte Spielwelt.](assets/journal/2026-01-12-suno-experiment/houdini-generators.png)

## Prozeduralismus und Pattern-basiertes Design

Das Projekt "ПАНЕЛЬКИ" (Panelki) entsteht im Rahmen des Masterkurses über prozedurale Weltgenerierung – Virtuelle Welten. Der Kern: Anstatt jedes Gebäude und jeden Straßenzug manuell zu platzieren, definiere ich *Regeln* und *Muster*, aus denen die Welt emergent entsteht. In Houdini habe ich drei HDAs (Houdini Digital Assets) entwickelt:

- **terrain_generator**: Echte Höhendaten aus Neryungi, Russland (ALOS PALSAR DEM)
- **building_generator**: Modulare Soviet-Architektur aus OpenStreetMap-Footprints
- **street_generator**: Straßennetzwerke, die die Gebäude verbinden

Das Ergebnis ist eine dystopische Winterstadt, bevölkert von anthropomorphen Tierfiguren im Stil sowjetischer Zeichentrickfilme.

![Konzeptkunst: Wolf unter einer Straßenlaterne im ewigen Winter. Konzeptbild erstellt mit Google Gemini (Nano Banana Pro).](assets/journal/2026-01-12-suno-experiment/concept-wolf-streetlamp.png)

## KI-Musik

Was mich zu diesem Experiment gebracht hat: Ich sah ein Video eines Musikproduzenten in meinem YouTube Feed: viele kommerzielle Musik wird inzwischen KI-generiert – ohne dass es auffällt. Bei Bildern und Videos sehe ich noch deutliche Artefakte und Inkonsistenzen, KI-Werbespots werden regelmäßig "außeinandergenommen" und kritisiert. Bei Audio liegt es anscheinend für einen Laien nah am professionellen Standard. Suno ist wohl aktuell der Marktführer.


## Das Experiment: Zwei Prompts

Das Video hatte mich inspiriert: ich brauchte Hintergrundmusik für meine Welt, die einen Pixel-look haben sollte: loopbar, atmosphärisch, sowjetisch-dystopisch. Keine Vocals. Also habe ich mich angemeldet und zwei Ansätze auf Suno getestet.

### Versuch 1: "Lo-fi"

<div data-audio-viewer
     data-prompt="Soviet-inspired dystopian winter lo fi game music loop, no vocals"
     data-artist="Suno AI"
     data-tracks='[
       {"src": "assets/journal/2026-01-12-suno-experiment/frozen-terminals.mp3", "title": "Frozen Terminals", "cover": "assets/journal/2026-01-12-suno-experiment/cover-frozen-terminals.jpeg", "artist": "Suno v5 (beta)", "description": "Dusty lo-fi loop built on detuned analog pads, soft tape hiss, and distant mechanical clanks. Low, pulsing bass stays static and hypnotic while a brittle music-box motif and minor-key piano fragments drift in and out. Subtle vinyl wobble and filtered wind FX create a bleak Soviet-dystopia winter mood; arrangement evolves slowly for seamless looping, with occasional radio-interference swells to reset the ear."},
       {"src": "assets/journal/2026-01-12-suno-experiment/red-snow-protocol.mp3", "title": "Red Snow Protocol", "cover": "assets/journal/2026-01-12-suno-experiment/cover-red-snow-protocol.jpeg", "artist": "Suno v4.5", "description": "Cold-war lo-fi loop with dusty vinyl crackle, tape-warbled strings, and a low, pulsing bass. Minimal piano figures trade with distant metallic hits, like factory echoes under falling snow. Muffled snare and soft rim knocks keep a slow, hypnotic groove; saturated synth pads swell in and out to suggest looming surveillance. Arrangement cycles subtly so it can loop seamlessly in-game, building a quiet, relentless tension."}
     ]'>
</div>

**Ergebnis:** Klingt zu kommerziell. "Lo-fi" war der falsche Begriff – ich wollte etwas Minimalistischeres, Roheres. Die generierte Beschreibung klingt besser als der tatsächliche Output.

### Versuch 2: "Minimal"

<div data-audio-viewer
     data-prompt="pixel game soundtrack, soviet inspired, winter and snow, dystopian and lonely, slow, minimal, no vocals"
     data-artist="Suno AI"
     data-tracks='[
       {"src": "assets/journal/2026-01-12-suno-experiment/frozen-relay.mp3", "title": "Frozen Relay", "cover": "assets/journal/2026-01-12-suno-experiment/cover-frozen-relay.jpeg", "artist": "Suno v5 (beta)", "description": "Bitcrushed chiptune pads over a sparse, detuned synth choir; slow, mechanical pulse with occasional metallic hits and distant wind FX. Melody is minimal and repetitive, using cold-square leads and low, droning bass. Reverb-drenched bells hint at Soviet-era clock towers in a buried city, with the energy staying restrained and lonely throughout; mix is narrow and mono-leaning, like an aging arcade cabinet in an abandoned bunker."},
       {"src": "assets/journal/2026-01-12-suno-experiment/iron-frost-protocol.mp3", "title": "Iron Frost Protocol", "cover": "assets/journal/2026-01-12-suno-experiment/cover-iron-frost-protocol.jpeg", "artist": "Suno v4.5", "description": "Minimal chiptune score with cold, glassy square waves and a slow, mechanical pulse. Sparse low-register synths suggest distant engines; high, bell-like arps trace falling snow. Reverb is long and metallic, as if heard in an empty hangar. Occasional detuned tones and filtered white-noise gusts create a bleak, dystopian hush."}
     ]'>
</div>

**Ergebnis:** Nicht wirklich minimal. Der Fokus auf "pixel game soundtrack" hat dazu geführt, dass es teilweise wie ein Hero-Soundtrack aus einem Indie-Game klingt – nicht wie atmosphärische Hintergrundmusik für ein Spiel, in dem man explorativ durch eine verlassene Stadt läuft. Die Beschreibungen sind interessant ("aging arcade cabinet in an abandoned bunker"), ich finde der tatsächliche Sound geht in eine andere Richtung.

## Die Beschreibungs-Output-Diskrepanz

![Pixel-Art-Ästhetik: Das Schaf auf sowjetischer Straße – genau dieser Stil bräuchte passende Musik. Konzeptbild erstellt mit Midjourney v7.](assets/journal/2026-01-12-suno-experiment/concept-sheep-pixel.png)

Was auffällt: Suno generiert wunderbar detaillierte Beschreibungen. "Bitcrushed chiptune pads over a sparse, detuned synth choir" klingt exakt nach dem, was ich will. Der tatsächliche Output? Klingt halt etwas zu "polished", wie Stock-Music.

Das ist dasselbe Muster wie bei meinen ComfyUI-Experimenten mit Kepler: Ich wollte einen voxelisierten, pixeligen Charakter ohne erkennbares Gesicht. Die KI lieferte typisch KI-generiert aussehende Ergebnisse mit Uncanny-Valley-Gesichtern, obwohl der Prompt explizit "voxel", "blocky", "no face" enthielt.

**Die Erkenntnis:** Generalistische KI-Tools sind wahrscheinlich einfach auf kommerzielle Mehrheitsästhetik trainiert. Spezialisierte Nischen – Pixel-Game-Soundtracks, voxelisierte Charaktere – erfordern entweder sehr viele Iterationen, sezialisierte Fine-Tunes oder manuelle Nachbearbeitung

In diesem Fall hat das Tool die Anforderungen nicht erfüllt – der Output schien für mich "handwerklich solide", aber stilistisch daneben, "too much". Für kommerzielle Mainstream-Musik mag das funktionieren, für spezialisierte Nischen braucht es nach wie vor menschliche Expertise oder zumindest erhebliche Nachbearbeitung.

## Technische Notizen

Suno bietet zwei Modelle:
- **v4.5**: Kostenlos, 50 Credits/Tag, "previously unimaginable production capabilities"
- **v5**: $30/Monat (Pro), noch höhere Qualität, v5-Samples werden parallel angeboten

Ich habe beide Modelle getestet: Die "Frozen"-Tracks (Frozen Terminals, Frozen Relay) sind mit v5 (beta) generiert – im Free Trial allerdings auf eine Minute begrenzt. Red Snow Protocol und Iron Frost Protocol stammen aus v4.5 und sind länger, gefallen mir aber weniger – **warum genau, kann ich nicht sagen**.

---

## Reflexion

Das war frustrierend. Ich wollte Musik für meine sowjetisch-dystopische Spielwelt: minimal, loopbar, atmosphärisch. Suno lieferte Stock-Music-Qualität – handwerklich solide, aber austauschbar.

Das Interessante: Die generierten *Beschreibungen* waren besser als die Musik. "Bitcrushed chiptune pads over a sparse, detuned synth choir" – genau das wollte ich. Der Output? Zu poliert, zu kommerziell.

### Kontext

- **Tools:** Suno AI (Web-Interface)
- **Intention:** Game-Soundtrack für das Panelki-Projekt erstellen

### Die 5 Forschungsfragen

- **Workflow:** Schneller Prototyp – Ideen testen ohne Musikwissen.
- **Autorschaft:** Enttäuscht, Kurator:in – ich habe nur ausgewählt, nicht gestaltet.
- **Iteration:** Verworfen – vermute, mit diesem Modell nicht weit zu kommen.
- **Scheitern:** Zu kommerziell. Die Beschreibungen waren besser als der Output.
- **Ästhetik:** Verfehlt – KI lieferte generischen Sound statt minimal-dystopisch.

### Synthese

- **Zentrale Erkenntnis:** Die generierten Beschreibungen zeigen mir: Für meine Vision gibt es Begriffe. Ich könnte damit existierende Musik suchen, ein anderes Tool probieren, oder einem echten Musiker ein Briefing geben.
- **Offene Frage:** Sind generalistische KI-Tools für spezialisierte Nischen überhaupt geeignet – oder braucht es immer Fine-Tunes oder menschliche Expertise?

**Keywords:** #Suno #Musik #GameAudio #Frustration #Beschreibung≠Output

<div class="interview-transcript">
<h4>Kontext</h4>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Welche Tools hast du verwendet?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Suno AI.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Was wolltest du erreichen?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Game-Soundtrack.</p></div>
</div>
<h4>Die 5 Forschungsfragen</h4>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Hat sich dein Arbeitsablauf verändert? <em>(Workflow)</em></p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Schneller Prototyp.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Wie hast du deine Rolle erlebt? <em>(Autorschaft)</em></p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Enttäuscht, Kurator:in.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Wie hat die schnelle KI-Ausgabe deinen Prozess beeinflusst? <em>(Iteration)</em></p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>In dem Fall habe ich das Ganze ja verworfen, weil ich vermute, dass ich mit dem Modell nicht sonderlich weit komme.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Was ist schiefgelaufen? <em>(Scheitern)</em></p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Zu kommerziell, Beschreibung ≠ Output.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Hat sich eine eigene musikalische/ästhetische Sprache entwickelt? <em>(Ästhetik)</em></p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Nein, verfehlt.</p></div>
</div>
<h4>Synthese</h4>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Im Eintrag schreibst du, dass Sunos generierte Beschreibungen ('Bitcrushed chiptune pads over a sparse, detuned synth choir') besser klingen als die Musik selbst. Ist das frustrierend – oder zeigt es, dass du die KI vielleicht als Text-Generator für Briefings an echte Musiker nutzen könntest?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Also zeigt mir, dass für die Vision, die ich hatte, gibt es Begriffe, und es gibt mir Hoffnung, dass ich entweder bereits existierende Musik mit diesen Begriffen finden kann, ein anderes Tool verwenden könnte, um so etwas zu generieren, oder es einem echten Musiker geben könnte. Es ist sehr frustrierend.</p></div>
</div>
</div>
