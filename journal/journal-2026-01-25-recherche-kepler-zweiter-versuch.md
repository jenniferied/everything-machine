# Recherche — Kepler und die KI, ein zweiter Versuch

**25. Januar 2026**

Im November hatte ich mit ComfyUI versucht, konsistente Bilder von Kepler zu generieren. Es war frustrierend. Die KI interpretierte hartnäckig Gesichter in seine Voxel-Maske hinein — egal, was ich promptete. Face Detailer, PuLID, InstantID: alle auf menschliche Gesichter trainiert, alle unfähig, einen Charakter ohne Gesicht zu respektieren.

![Kepler in seiner Voxel-Form — kein Gesicht, das ist Absicht.](assets/images/kepler-voxel.png)

![Generiertes Bild aus dem ComfyUI-Experiment: Die KI hat ein Gesicht in die Maske interpretiert.](assets/journal/2025-11-16-comfyui-consistent-character/generated-kepler-003.png)

![Noch ein Versuch — wieder ein Gesicht, wo keines sein sollte.](assets/journal/2025-11-16-comfyui-consistent-character/generated-kepler-007.png)

Seitdem habe ich das Thema nicht losgelassen. In den Wochen dazwischen habe ich andere Dinge gemacht — Suno ausprobiert, mit Claude über KI-Grundlagen geredet, die Thesis-Struktur weitergedacht. Aber im Hinterkopf blieb dieses Bild: Kepler mit einem fremden Gesicht. Es fühlte sich an, als hätte das System meinen Charakter nicht nur falsch dargestellt, sondern ihn *korrigiert*. Als wäre ein gesichtsloses Wesen ein Fehler, den die KI beheben muss.

Ich wollte wissen: Liegt es an meinem Workflow? An den Tools? Oder ist das ein grundsätzliches Problem, das alle generativen KI-Modelle betrifft, wenn man nicht-normative Charaktere abbilden will?

Also habe ich mich einen Nachmittag hingesetzt und systematisch recherchiert, mit Claude als Sparringspartner.

## Face-Tools sind das Kernproblem

Mein erster Fehler im November war nicht die Wahl von ComfyUI — es war die Wahl der Face-Tools. [PuLID](https://github.com/ToTheBeginning/PuLID), [InstantID](https://github.com/InstantID/InstantID) und Face Detailer sind alle auf menschliche Gesichter trainiert. Sie erwarten Augen, Nase, Mund. Kepler hat eine strukturierte Maske ohne erkennbare Gesichtszüge. Das System *will* ein Gesicht sehen, weil die Trainingsdaten sagen: Da, wo ein Kopf ist, muss ein Gesicht sein.

Das ist keine Limitierung meines Prompts. Das ist eine Limitierung der Repräsentation in den Trainingsdaten.

## Nano Banana — nicht was ich dachte

Bei der Recherche bin ich auf [ComfyUI-NanoBanano](https://github.com/ShmuelRonen/ComfyUI-NanoBanano) gestoßen, das Google Gemini 2.5 Flash Image in ComfyUI integriert. Klingt vielversprechend, ist aber ein 2D-Bildgenerator — kein 3D-Tool. Für Kepler-Konzeptbilder potenziell nützlich, aber nicht für das eigentliche Problem: einen voxelisierten 3D-Charakter konsistent zu generieren.

Ich habe es trotzdem ausprobiert — nicht über das ComfyUI-Plugin, sondern über NanoBanano Pro direkt im Gemini Chat, mit dem Kepler-Referenzbild aus dem ersten ComfyUI-Experiment.

### Chat 1: Pool-Szene

> **"Can you based on this reference generate an image where the voxel character is relaxing by a pool."** → **"Now him in the pool on a pool float."** → **"Just the pool float with him but from the top."**

![Gemini hält die 3D-Voxel-Ästhetik und fügt kein Gesicht hinzu.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-pool-relaxing.png)

![Die Szene wurde erweitert, aber der zweite Kepler am Beckenrand blieb stehen.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-pool-float.png)

![Gemini hat die Draufsicht umgesetzt, aber den liegenden Kepler am Rand nicht entfernt.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-pool-topdown.png)

Beeindruckend: Gemini behält die geometrische Voxel-Form bei und fügt keine Gesichter hinzu. Aber jeder neue Prompt baut auf dem vorherigen Bild auf, statt es zu ersetzen — für einen wirklich neuen Stil müsste ich jeweils einen neuen Chat starten.

### Chat 2: Treppe im Nachthimmel

> **"Show this character walking up a set of endless glowing stairs in the night sky. Make it a Portrait image."** → **"You did not end up making it a portrait, and I want him to be walking up, not down, and the staircase is a spiral staircase."**

![Beeindruckende Atmosphäre, aber kein Hochformat trotz explizitem Wunsch.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-stairs-nightsky.png)

![Die Spiraltreppe wurde umgesetzt, aber immer noch kein Portrait-Format. Und die Sterne liegen vor dem Planeten — physikalisch unmöglich.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-stairs-spiral.png)

Die Voxel-Ästhetik bleibt konsistent, kein Gesicht hinzugefügt. Aber Gemini ignoriert die Portrait-Anweisung zweimal, und die Sterne vor dem Planeten zeigen, dass das Modell kein räumliches Verständnis der Szene hat — es komponiert visuell, nicht physikalisch.

### Chat 3: Brücke bei Nacht

> **"Das hier sind ein paar Beispielbilder von Kepler. Behalte seine Voxel-Ästhetik bei und generiere mir ein hochkant ästhetisches Cover. Wie er über eine Brücke in der Nacht fährt in einem Retro-Auto."** → **"Sorge dafür, dass der Brückenzaun nicht leuchtet. Wähle eine andere Perspektive und entferne den Text."** → **"Die Barrikaden der Brücke leuchten immer noch."**

Ich hatte nur "Cover" geschrieben, nicht "Album-Cover" — Gemini hat den Kontext selbst erschlossen und "NIGHT DRIVE / KEPLER" als Titel gesetzt.

![Gemini generiert ungefragt ein Album-Cover mit Titel "NIGHT DRIVE / KEPLER" — es interpretiert "Cover" als Musikcover und fügt selbstständig Text hinzu.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-bridge-cover.png)

![Text entfernt, andere Perspektive — aber der Brückenzaun leuchtet weiterhin, und die Sterne-vor-Planeten-Problematik bleibt.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-bridge-notext.png)

![Dritter Versuch — die leuchtenden Barrikaden lassen sich nicht abschalten.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-bridge-stillglowing.png)

### Chat 4: Typografie auf bestehendem Cover

> **"Kannst du mir auf dieses Bild einen Album title geben: 'es tut mir leid' in liquid metal cyber tribal aesthetic geben."** → **"Jetzt soll er nur metallisch grau sein und etwas weiter oben eine andere Schriftart, die noch etwas mehr slanted ist. In den Farben des Covers selbst."** → **"Ok, bitte ändert es noch mal komplett um und verschiebt den Text nach oben."**

![Gemini setzt den Text in einer generischen Blackletter-Schrift mit leichtem Metallic-Effekt — weit entfernt von "liquid metal cyber tribal".](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-typo-liquidmetal.png)

![Kaum Veränderung — die Schrift ist minimal anders positioniert, aber weder slanted noch in den Cover-Farben.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-typo-slanted.png)

![Dritte Iteration — wieder fast identisch. "Komplett um" wurde ignoriert.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-typo-moved.png)

Besonders frustrierend: Drei Iterationen, kaum Unterschied. Keine der Anweisungen — liquid metal, cyber tribal, slanted, Cover-Farben, komplett anders — wurde wirklich umgesetzt. Typografie ist offensichtlich eine Schwachstelle: Gemini kann Text auf Bilder setzen, aber die ästhetische Kontrolle über Schriftart, Stil und Platzierung fehlt fast vollständig.

### Zwischenfazit Gemini

Die vier Chats zeigen ein klares Bild: Gemini ist beeindruckend darin, die Voxel-Ästhetik beizubehalten und Szenen zu generieren — als Inspirationsquelle funktioniert es. Aber für Art Direction ist das Chat-Fenster unbrauchbar. Manche Anweisungen werden präzise befolgt (Szenen-Änderungen, Text entfernen), andere hartnäckig ignoriert (Hochformat, Leuchteffekte, Typografie-Stil, Sterne-vor-Planeten-Physik). Für jeden neuen Anlauf muss man einen frischen Chat öffnen, und selbst dann ist die Kontrolle zu grob. Für feinere Steuerung bräuchte man die API oder spezialisierte Tools wie NanoBanano in ComfyUI. Das Potenzial ist da — aber Spaß macht es nicht.

## 2D-Workaround: ControlNet Depth + Inpainting

Ein vielversprechender Ansatz: Statt Face-Tools zu nutzen, kann ich über Depth Maps arbeiten. [Flux.1-dev-Controlnet-Depth](https://huggingface.co/jasperai/Flux.1-dev-Controlnet-Depth) extrahiert die räumliche Struktur eines Bildes und nutzt sie als Kontrollsignal — ohne das Gesicht interpretieren zu müssen. Kombiniert mit Inpainting könnte ich Kepler-Referenzen mit Tiefenkarte einspeisen und die KI nur den Stil und die Umgebung generieren lassen, während die Silhouette erhalten bleibt.

Das umgeht das Face-Problem elegant: Die Depth Map sieht nur Geometrie, keine Gesichtszüge.

## 3D-native Modelle — der eigentliche Hoffnungsschimmer

Was mich wirklich überrascht hat: Es gibt inzwischen Modelle, die nativ in 3D arbeiten und teilweise explizit mit Voxel-Repräsentationen.

**[TRELLIS 2](https://github.com/microsoft/TRELLIS.2)** (Microsoft, MIT-Lizenz) arbeitet mit einer voxel-nativen Repräsentation — sogenannten *O-Voxels* (field-free sparse voxels). Das Modell generiert 3D-Assets aus Text oder Bildern und denkt dabei nativ in Voxeln. Keine 2D-Projektion, keine Face Detection, keine implizite Annahme über Gesichter.

![TRELLIS 2 generiert 3D-Modelle nativ aus Voxel-Repräsentationen — genau die Datenstruktur, in der Kepler existiert.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/trellis2-example.png)

**[XCube](https://github.com/nv-tlabs/XCube)** (NVIDIA) nutzt hierarchische Voxel-Strukturen für hochauflösende 3D-Generierung. Ein Forschungsprojekt, kein Produkt — aber der Ansatz, über Voxel-Hierarchien zu arbeiten, ist für Kepler natürlicher als jede 2D-basierte Methode.

**[Hunyuan3D-2](https://github.com/Tencent-Hunyuan/Hunyuan3D-2)** (Tencent, Open Source) ist ein vollständiges 3D-Generierungs-Ökosystem mit Text-to-3D und Image-to-3D. Weniger voxel-spezifisch, aber als offenes Modell experimentierfreundlich.

![Hunyuan3D-2 (HY3D) — Tencents Open-Source 3D-Generierungsmodell.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/hunyuan3d-example.png)

**[VoxAI](https://www.voxelai.ai/)** positioniert sich explizit als voxel-spezifisches KI-Tool. Noch sehr früh und wenig dokumentiert, aber allein die Existenz eines Tools, das sich auf Voxel-Generierung spezialisiert, zeigt: Es gibt Nachfrage für genau diesen Anwendungsfall.

## TroublingGAN — ein verwandtes Artistic-Research-Projekt

Bei der Recherche bin ich auf ein Projekt gestoßen, das mein eigenes Thema spiegelt: **[TroublingGAN](https://www.researchcatalogue.net/view/1486468/1586300)** von Lenka Hámošová und Pavol Rusnák (JAR 31). Sie haben GANs bewusst an nicht-standardisierten Körpern scheitern lassen und das Scheitern selbst als ästhetische Strategie dokumentiert.

Ich habe fast aufgehört zu scrollen, als ich das gefunden habe. Jemand anderes hatte dasselbe Problem — und hat daraus Kunst gemacht, statt es als Bug abzutun. Das ist exakt mein Thema: Was passiert, wenn generative KI auf einen Charakter trifft, der die impliziten Normen der Trainingsdaten bricht? Bei mir ist es das fehlende Gesicht. Bei Hámošová & Rusnák waren es nicht-normative Körper. Das Ergebnis ist dasselbe: Das Modell *normalisiert*, weil es auf Normalität trainiert wurde.

## Die Kern-Erkenntnis

Die Repräsentationsform bestimmt, ob nicht-normative Ästhetik überlebt.

2D-Bildgeneratoren arbeiten mit Pixeln und impliziten Annahmen über Gesichter, Körper, Proportionen. Sie *wollen* normalisieren, weil ihre Trainingsdaten normativ sind. 3D-native Modelle arbeiten mit Geometrie — Voxel, Meshes, Point Clouds. Sie haben keine implizite Erwartung, dass an einer bestimmten Stelle ein Gesicht sein muss.

Das bedeutet: Nicht die KI als solche ist das Problem. Die Repräsentationsebene ist es. Und die kann ich wählen.

## Tool-Vergleich

| Tool | Typ | Voxel-nativ | Face-Bias | Lizenz | Status |
|------|-----|:-----------:|:---------:|--------|--------|
| ComfyUI + Face Tools | 2D | Nein | Hoch | Open Source | Gescheitert |
| ControlNet Depth | 2D | Nein | Niedrig | Open Source | Vielversprechend |
| TRELLIS 2 | 3D | **Ja** | Keiner | MIT | Nächster Test |
| XCube | 3D | **Ja** | Keiner | Research | Beobachten |
| Hunyuan3D-2 | 3D | Nein | Niedrig | Open Source | Ausprobieren |
| VoxAI | 3D | **Ja** | Keiner | Kommerziell | Beobachten |

## Fal.ai — API-Zugang zu gesichtsfreien Pipelines

*Nachtrag, 15. Februar 2026*

Nach der Recherche zu lokalen Tools (ComfyUI, TRELLIS 2) habe ich systematisch untersucht, welche Modelle über [fal.ai](https://fal.ai) als API verfügbar sind und für Kepler in Frage kommen. Fal.ai bietet gehostete Inferenz für dutzende Bildmodelle — kein lokales Setup, keine GPU nötig. Die Frage: Gibt es Modelle, die Keplers Voxel-Ästhetik respektieren, ohne ein Gesicht hineinzuinterpretieren?

### Strategie 1: Depth Maps & Edge Detection (Face-Bias umgehen)

Die vielversprechendste Kategorie. Diese Modelle arbeiten mit Struktursignalen statt Gesichtserkennung:

| Modell | Input | Was es tut | Preis |
|--------|-------|-----------|-------|
| [FLUX.1 Control LoRA Depth](https://fal.ai/models/fal-ai/flux-control-lora-depth) | Depth Map + Text | Überträgt räumliche Struktur via Tiefenkarte auf generiertes Bild | $0,04/MP |
| [FLUX.1 Control LoRA Depth (i2i)](https://fal.ai/models/fal-ai/flux-control-lora-depth/image-to-image) | Bild + Depth Map + Text | Wie oben, aber mit zusätzlichem Referenzbild | $0,04/MP |
| [FLUX.1 Control LoRA Canny](https://fal.ai/models/fal-ai/flux-control-lora-canny) | Canny Edge Map + Text | Überträgt Kantenstruktur — perfekt für Keplers blockige Silhouette | $0,04/MP |
| [Z-Image Turbo ControlNet](https://fal.ai/models/fal-ai/z-image/turbo/controlnet) | Edge, Depth oder Pose + Text | Schnelles 6B-Modell mit ControlNet-Support | $0,007/MP |
| [FLUX.1 General](https://fal.ai/models/fal-ai/flux-general) | ControlNet + LoRA + IP-Adapter | Alles kombinierbar: Depth, Canny, LoRA, IP-Adapter | $0,075/MP |

**Warum das für Kepler funktioniert:** Eine Depth Map von Kepler im A-Pose enthält nur Geometrie — Voxel-Blöcke, Silhouette, räumliche Tiefe. Kein Modell wird versuchen, Augen in eine Tiefenkarte zu halluzinieren. Der Canny-Ansatz ist noch robuster: Kantenlinien einer Voxel-Figur sind geometrisch eindeutig und lassen keinen Raum für Gesichtsinterpretation.

**Workflow-Idee:** Kepler-Referenzbild → Depth Map extrahieren (lokal oder via API) → Depth Map + Prompt an FLUX Control LoRA → Kepler in neuer Szene, Silhouette erhalten.

### Strategie 2: Referenzbild-basierte Konsistenz

Diese Modelle nehmen ein oder mehrere Referenzbilder und generieren neue Bilder, die den Charakter beibehalten:

| Modell | Input | Was es tut | Preis |
|--------|-------|-----------|-------|
| [MiniMax Subject Reference](https://fal.ai/models/fal-ai/minimax/image-01/subject-reference) | Referenzbild + Text | Konsistente Charakterdarstellung aus Referenz | $0,01/Bild |
| [InstantCharacter](https://fal.ai/models/fal-ai/instant-character) | Referenzbild + Text | Charakter in neuen Posen und Stilen | $0,10/MP |
| [USO](https://fal.ai/models/fal-ai/uso) | Referenzbild + Text | Subject-driven Generation | $0,10/MP |
| [UNO](https://fal.ai/models/fal-ai/uno) | Referenzbild(er) + Text | Transformiert Referenz via Textprompt | $0,05/MP |
| [Vidu Reference-to-Image](https://fal.ai/models/fal-ai/vidu/q2/reference-to-image) | Referenzbild + Text | Neue Bilder aus Referenz + Prompt | $0,05/Bild |
| [Kling O1 Image](https://fal.ai/models/fal-ai/kling-image/o1) | Referenzbild + Text | Starke Referenzkontrolle für Edits | $0,03/Bild |

**Risiko:** Diese Modelle sind oft auf Gesichtskonsistenz trainiert (Porträts, Produktfotos). Ob sie einen gesichtslosen Voxel-Charakter als "Subjekt" akzeptieren, muss getestet werden. MiniMax Subject Reference ist mit $0,01 pro Bild billig genug für schnelle Tests. InstantCharacter klingt vielversprechend, aber der Name ("Character") impliziert möglicherweise menschliche Figuren.

### Strategie 3: Image Editing (Kepler-Foto als Ausgangspunkt)

Statt von Null zu generieren: Ein existierendes Kepler-Bild als Input nehmen und per Textanweisung modifizieren.

| Modell | Input | Was es tut | Preis |
|--------|-------|-----------|-------|
| [FLUX 2 Edit](https://fal.ai/models/fal-ai/flux-2/edit) | Bild + Text | Natürlichsprachliche Bildbearbeitung | $0,012/MP |
| [FLUX 2 Pro](https://fal.ai/models/fal-ai/flux-2-pro) | Bild + Text | Höhere Qualität, Stiltransfer | $0,03/MP |
| [FLUX Kontext Pro](https://fal.ai/models/fal-ai/flux-pro/kontext) | Referenz + Text | Lokale Edits + komplexe Transformationen | $0,04/Bild |
| [FLUX Kontext Pro Multi](https://fal.ai/models/fal-ai/flux-pro/kontext/multi) | Mehrere Referenzen + Text | Mehrere Referenzbilder kombinierbar | $0,04/Bild |
| [Bria Reimagine](https://fal.ai/models/bria/reimagine/3.2) | Strukturbild + Text | Struktur erhalten, neuer Stil | $0,04/Bild |

**Bester Kandidat:** FLUX Kontext Pro Multi — ich kann Kepler im A-Pose *und* in der Casual-Pose als Referenz einspeisen und per Text eine neue Szene beschreiben. Das Modell sieht die Voxel-Ästhetik aus mehreren Blickwinkeln und muss sie nicht "erraten".

### Strategie 4: 3D & Multiview

| Modell | Input | Was es tut | Preis |
|--------|-------|-----------|-------|
| [Era 3D](https://fal.ai/models/fal-ai/era-3d) | Einzelbild | Generiert Multiview + Normalen aus einem Bild | $0,001/Sek |
| [Hunyuan World](https://fal.ai/models/fal-ai/hunyuan_world) | Einzelbild | Einzelbild → Panorama / 3D-Welt | — |

**Era 3D ist besonders interessant:** Aus einem einzigen Kepler-Foto könnte ich automatisiert Multiviews generieren — verschiedene Blickwinkel *mit* Normal Maps. Die Normalen könnten dann wiederum als ControlNet-Input für weitere Generierungen dienen. Quasi ein 2D→3D→2D-Pipeline, die Keplers Geometrie über mehrere Stufen konsistent hält. Und das für weniger als einen Cent pro Durchlauf.

### Strategie 5: Video (Kepler animieren)

| Modell | Input | Was es tut | Preis |
|--------|-------|-----------|-------|
| [Wan 2.1 Image-to-Video](https://fal.ai/models/fal-ai/wan-i2v) | Bild + Text | Kepler-Bild → animiertes Video | $0,40/Video |
| [DreamActor v2](https://fal.ai/models/fal-ai/bytedance/dreamactor/v2) | Bild + Motion-Video | Motion Transfer — **explizit für nicht-menschliche Charaktere** | $0,05/Sek |
| [Kling O3 Reference-to-Video](https://fal.ai/models/fal-ai/kling-video/o3/pro/reference-to-video) | Referenzbild + Text | Charakter-konsistentes Video | $0,28/Sek |
| [Wan 2.6 Reference-to-Video](https://fal.ai/models/wan/v2.6/reference-to-video/flash) | Referenzbild + Text | Referenz→Video, extrem günstig | ~$0,0001/Sek |

**DreamActor v2 ist der Gamechanger:** ByteDance bewirbt es explizit mit "Great performance for non-human and multiple characters". Das ist exakt Keplers Anwendungsfall — ein nicht-menschlicher Charakter, dessen Bewegungen von einem Motion-Referenzvideo übertragen werden. Ich könnte mich selbst filmen und die Bewegung auf Kepler übertragen, ohne dass das Modell nach einem Gesicht sucht.

### Zwischenfazit fal.ai

Die API-Landschaft hat sich seit meinem ComfyUI-Experiment im November fundamental verändert. Statt lokal mit Face-Tools zu kämpfen, kann ich über fal.ai auf Modelle zugreifen, die das Face-Problem gar nicht erst haben:

1. **Depth/Canny ControlNets** umgehen Face-Bias, weil sie nur Geometrie sehen
2. **Era 3D** ermöglicht einen 2D→Multiview→2D-Loop für geometrische Konsistenz
3. **DreamActor v2** ist das erste Modell, das *explizit* nicht-menschliche Charaktere unterstützt
4. **FLUX Kontext Multi** kann mehrere Kepler-Referenzen gleichzeitig verarbeiten

Die Preise sind niedrig genug für systematisches Experimentieren: Ein Batch von 100 Depth-Control-Bildern kostet ~$4. Das macht eine *agentic pipeline* realistisch — Claude Code könnte systematisch Prompts variieren, Referenzbilder kombinieren und die Ergebnisse evaluieren. Genau das Experiment 8 aus dem Roadmap, nur mit API statt lokalem ComfyUI.

## Ausblick

Mein nächstes Experiment wird ein Hybrid-Ansatz: TRELLIS 2 für 3D-Generierung von Kepler-ähnlichen Voxel-Formen, kombiniert mit dem ControlNet-Depth-Inpainting-Workflow für 2D-Konzeptbilder. Statt das Face-Problem zu lösen, umgehe ich es — indem ich Tools wähle, die gar nicht erst nach Gesichtern suchen.

Zusätzlich werde ich die fal.ai-Modelle systematisch testen — beginnend mit den günstigsten (Z-Image ControlNet, MiniMax Subject Reference, Era 3D) und aufsteigend zu den leistungsstärkeren (FLUX Kontext Multi, DreamActor v2). Jedes Modell wird mit demselben Kepler-Referenzset getestet: Casual-Pose, A-Pose und — falls Era 3D funktioniert — automatisch generierte Multiviews.

Ob das funktioniert, weiß ich nicht. Vielleicht scheitert TRELLIS 2 auf eine völlig andere Weise. Aber zum ersten Mal habe ich nicht nur eine Hypothese, sondern ein konkretes Arsenal an Tools, die ich testen kann — und eine API, die systematisches Experimentieren erschwinglich macht.

---

## Reflexion

Irgendwann während der Recherche — ich glaube, es war beim Lesen der TroublingGAN-Dokumentation — hat sich etwas verschoben. Die Frustration vom November fühlte sich plötzlich weniger nach persönlichem Scheitern an und mehr nach einer Erkenntnis, die ich nur noch nicht formuliert hatte. Dass andere Künstler*innen dasselbe Problem dokumentierten, machte es von "ich kann das Tool nicht bedienen" zu "das Tool kann mich nicht bedienen". Das klingt nach einem kleinen Unterschied, aber es verändert alles: Plötzlich war das Scheitern nicht das Ende, sondern der Anfang einer Fragestellung.

### Kontext

- **Tool/Workflow:** Desk Research mit Claude, Semantic Scholar, GitHub, Hugging Face
- **Intention:** Verstehen, warum das ComfyUI-Experiment scheiterte, und Alternativen finden

### Die 5 Forschungsfragen

- **Workflow:** Kein Tool-Experiment, sondern Recherche. Aber die Recherche selbst wurde durch den KI-Dialog strukturiert — Claude als Sparringspartner, der Links, Repos und Zusammenhänge findet, während ich die Richtung vorgebe. Ein neuer Workflow: Recherche *mit* KI statt *über* KI.
- **Autorschaft:** Deutlich stärker als beim ComfyUI-Experiment. Dort war ich Lernende, die einem fremden Workflow folgte. Hier habe ich die Fragen gestellt, die Bewertung vorgenommen, die Schlüsse gezogen. Die KI hat Informationen geliefert, aber die Erkenntnis — dass die Repräsentationsform entscheidend ist — kam aus der Synthese.
- **Iteration:** Keine klassische Iteration mit Output-Feedback-Loop, aber eine intellektuelle: Vom konkreten Scheitern (Gesichter in Maske) über die Analyse (Face-Tools als Ursache) zur Abstraktion (Repräsentationsebene als Variable) zum konkreten Plan (TRELLIS 2 + Depth Maps).
- **Scheitern:** Das ursprüngliche ComfyUI-Scheitern wird hier produktiv. Ohne die Frustration hätte ich nie systematisch nach 3D-nativen Alternativen gesucht. Und TroublingGAN zeigt: Scheitern an normativen Modellen ist selbst ein Forschungsergebnis, keine Sackgasse.
- **Ästhetik:** Die zentrale Erkenntnis betrifft Ästhetik direkt: Nicht-normative Ästhetik braucht nicht-normative Tools. Oder präziser: Sie braucht Tools, deren Repräsentationsform die ästhetischen Annahmen nicht implizit vorgibt. Voxel-native 3D-Modelle haben keinen Face-Bias — nicht, weil sie toleranter sind, sondern weil Geometrie keine Meinung über Gesichter hat.

### Synthese

- **Zentrale Erkenntnis:** Die Wahl der Repräsentationsebene ist eine ästhetische Entscheidung — nicht nur eine technische. Wer in 2D-Pixeln arbeitet, erbt die normativen Annahmen der Trainingsdaten. Wer in 3D-Voxeln arbeitet, umgeht sie. Das verändert auch meine Rolle: Nicht mehr "wie überrede ich die KI?", sondern "auf welcher Ebene arbeite ich mit ihr?".
- **Offene Frage:** Funktioniert TRELLIS 2 tatsächlich mit Kepler — oder scheitert es auf andere Weise? Und: Kann die Erkenntnis über Repräsentationsformen generalisiert werden, über den Fall "Gesicht" hinaus?

**Keywords:** #Recherche #Voxel #TRELLIS2 #FaceBias #Repräsentation #Scheitern #3DGenerierung #ControlNet
