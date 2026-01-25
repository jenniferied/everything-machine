# Recherche — Kepler und die KI, ein zweiter Versuch

**25. Januar 2026**

Im November hatte ich mit ComfyUI versucht, konsistente Bilder von Kepler zu generieren. Es war frustrierend. Die KI interpretierte hartnäckig Gesichter in seine Voxel-Maske hinein — egal, was ich promptete. Face Detailer, PuLID, InstantID: alle auf menschliche Gesichter trainiert, alle unfähig, einen Charakter ohne Gesicht zu respektieren.

![Kepler in seiner Voxel-Form — kein Gesicht, das ist Absicht.](assets/images/kepler-voxel.png)

![Generiertes Bild aus dem ComfyUI-Experiment: Die KI hat ein Gesicht in die Maske interpretiert.](assets/journal/2025-11-16-comfyui-consistent-character/generated-kepler-003.png)

![Noch ein Versuch — wieder ein Gesicht, wo keines sein sollte.](assets/journal/2025-11-16-comfyui-consistent-character/generated-kepler-007.png)

Seitdem habe ich das Thema nicht losgelassen. In den Wochen dazwischen habe ich andere Dinge gemacht — Suno ausprobiert, mit Claude über KI-Grundlagen geredet, die Thesis-Struktur weitergedacht. Aber im Hinterkopf blieb dieses Bild: Kepler mit einem fremden Gesicht. Es fühlte sich an, als hätte das System meinen Charakter nicht nur falsch dargestellt, sondern ihn *korrigiert*. Als wäre ein gesichtsloses Wesen ein Fehler, den die KI beheben muss.

Ich wollte wissen: Liegt es an meinem Workflow? An den Tools? Oder ist das ein grundsätzliches Problem, das alle generativen KI-Modelle betrifft, wenn man nicht-normative Charaktere abbilden will?

Also habe ich mich einen Nachmittag hingesetzt und systematisch recherchiert, mit Claude als Sparringspartner.

## Was ich gefunden habe

### Face-Tools sind das Kernproblem

Mein erster Fehler im November war nicht die Wahl von ComfyUI — es war die Wahl der Face-Tools. [PuLID](https://github.com/ToTheBeginning/PuLID), [InstantID](https://github.com/InstantID/InstantID) und Face Detailer sind alle auf menschliche Gesichter trainiert. Sie erwarten Augen, Nase, Mund. Kepler hat eine strukturierte Maske ohne erkennbare Gesichtszüge. Das System *will* ein Gesicht sehen, weil die Trainingsdaten sagen: Da, wo ein Kopf ist, muss ein Gesicht sein.

Das ist keine Limitierung meines Prompts. Das ist eine Limitierung der Repräsentation in den Trainingsdaten.

### Nano Banana — nicht was ich dachte

Bei der Recherche bin ich auf [ComfyUI-NanoBanano](https://github.com/ShmuelRonen/ComfyUI-NanoBanano) gestoßen, das Google Gemini 2.5 Flash Image in ComfyUI integriert. Klingt vielversprechend, ist aber ein 2D-Bildgenerator — kein 3D-Tool. Für Kepler-Konzeptbilder potenziell nützlich, aber nicht für das eigentliche Problem: einen voxelisierten 3D-Charakter konsistent zu generieren.

### 2D-Workaround: ControlNet Depth + Inpainting

Ein vielversprechender Ansatz: Statt Face-Tools zu nutzen, kann ich über Depth Maps arbeiten. [Flux.1-dev-Controlnet-Depth](https://huggingface.co/jasperai/Flux.1-dev-Controlnet-Depth) extrahiert die räumliche Struktur eines Bildes und nutzt sie als Kontrollsignal — ohne das Gesicht interpretieren zu müssen. Kombiniert mit Inpainting könnte ich Kepler-Referenzen mit Tiefenkarte einspeisen und die KI nur den Stil und die Umgebung generieren lassen, während die Silhouette erhalten bleibt.

Das umgeht das Face-Problem elegant: Die Depth Map sieht nur Geometrie, keine Gesichtszüge.

### 3D-native Modelle — der eigentliche Hoffnungsschimmer

Was mich wirklich überrascht hat: Es gibt inzwischen Modelle, die nativ in 3D arbeiten und teilweise explizit mit Voxel-Repräsentationen.

**[TRELLIS 2](https://github.com/microsoft/TRELLIS.2)** (Microsoft, MIT-Lizenz) arbeitet mit einer voxel-nativen Repräsentation — sogenannten *O-Voxels* (field-free sparse voxels). Das Modell generiert 3D-Assets aus Text oder Bildern und denkt dabei nativ in Voxeln. Keine 2D-Projektion, keine Face Detection, keine implizite Annahme über Gesichter.

![TRELLIS 2 generiert 3D-Modelle nativ aus Voxel-Repräsentationen — genau die Datenstruktur, in der Kepler existiert.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/trellis2-example.webp)

**[XCube](https://github.com/nv-tlabs/XCube)** (NVIDIA) nutzt hierarchische Voxel-Strukturen für hochauflösende 3D-Generierung. Ein Forschungsprojekt, kein Produkt — aber der Ansatz, über Voxel-Hierarchien zu arbeiten, ist für Kepler natürlicher als jede 2D-basierte Methode.

**[Hunyuan3D-2](https://github.com/Tencent-Hunyuan/Hunyuan3D-2)** (Tencent, Open Source) ist ein vollständiges 3D-Generierungs-Ökosystem mit Text-to-3D und Image-to-3D. Weniger voxel-spezifisch, aber als offenes Modell experimentierfreundlich.

![Hunyuan3D-2 (HY3D) — Tencents Open-Source 3D-Generierungsmodell.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/hunyuan3d-example.png)

**[VoxAI](https://www.voxelai.ai/)** positioniert sich explizit als voxel-spezifisches KI-Tool. Noch sehr früh und wenig dokumentiert, aber allein die Existenz eines Tools, das sich auf Voxel-Generierung spezialisiert, zeigt: Es gibt Nachfrage für genau diesen Anwendungsfall.

### TroublingGAN — ein verwandtes Artistic-Research-Projekt

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

## Ausblick

Mein nächstes Experiment wird ein Hybrid-Ansatz: TRELLIS 2 für 3D-Generierung von Kepler-ähnlichen Voxel-Formen, kombiniert mit dem ControlNet-Depth-Inpainting-Workflow für 2D-Konzeptbilder. Statt das Face-Problem zu lösen, umgehe ich es — indem ich Tools wähle, die gar nicht erst nach Gesichtern suchen.

Ob das funktioniert, weiß ich nicht. Vielleicht scheitert TRELLIS 2 auf eine völlig andere Weise. Aber zum ersten Mal habe ich eine Hypothese, die ich testen kann — statt blind in Workflows zu stolpern, die nicht für Kepler gemacht sind.

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
