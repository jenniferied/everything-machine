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

## NanoBanano — nicht was ich dachte

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

## Von der Frustration zum System

Die Gemini-Chats haben gezeigt: Das Potenzial ist da, aber die Steuerung über ein Chat-Fenster ist zu grob. Manche Anweisungen werden befolgt, andere ignoriert — und bei jedem neuen Versuch muss ich einen frischen Chat öffnen. Das skaliert nicht.

Parallel hatte ich [fal.ai](https://fal.ai) entdeckt — eine Plattform, die gehostete Inferenz für dutzende Bildmodelle anbietet. Kein lokales Setup, keine GPU, alles über API. Die Idee: Statt manuell in Chat-Fenstern zu experimentieren, ein Python-Skript schreiben, das systematisch verschiedene Modelle mit denselben Prompts und Referenzbildern aufruft. Cursor und Claude Code als Entwicklungsumgebung, fal.ai als Inferenz-Backend.

Der Workflow-Shift war fundamental: Nicht mehr "wie überrede ich ein einzelnes Modell?" — sondern "wie vergleiche ich neun Modelle systematisch miteinander?". Ein Automatisierungs-Problem statt eines Überredungs-Problems. Und das erste Mal, dass Claude Code nicht nur bei der Recherche half, sondern den gesamten Experiment-Workflow ermöglichte: Skript schreiben, API-Calls strukturieren, Ergebnisse sortieren.

## 9 Modelle, 7 Phasen

Das Experiment (Experiment 05) wuchs über mehrere Wochen in sieben Phasen:

**Phase 1 — Screening:** Neun Modelle mit demselben Kepler-A-Pose-Referenzbild testen. Erste Sortierung: Welche respektieren die Voxel-Ästhetik, welche halluzinieren Gesichter?

**Phase 2 — Szenen:** Die besten Modelle in vier Signature Scenes testen (Studio, Pool, Night Drive, Spiral Staircase) — jeweils in Quer- und Hochformat.

**Phase 2b — Der Durchbruch:** Wechsel vom A-Pose- zum Posed-Referenzbild. Sofort bessere Ergebnisse — die dynamischere Pose gibt den Modellen mehr Kontext über Keplers Körpersprache.

**Phase 3 — Signature Scenes:** Verfeinerte Prompts, optimierte Parameter. Die finalen Bilder sind die, die auf der Bild-Generationen-Seite zu sehen sind.

**Ergebnis:** Zwei klare Gewinner — *GPT Image 1.5* (OpenAI, über fal.ai) und *NanoBanana Pro* (Gemini 2.5 Flash). Beide respektieren Keplers gesichtslose Voxel-Ästhetik konsistent, beide produzieren in verschiedenen Szenen und Formaten brauchbare Ergebnisse. Die günstigeren Modelle (MiniMax, Z-Image) scheiterten am Face-Bias — genau das Problem, das schon ComfyUI hatte.

## Highlights

Ein paar der stärksten Ergebnisse aus 134 generierten Bildern:

![GPT Image 1.5 — Kepler im Studio, posed. Mein Lieblingsbild aus dem gesamten Experiment.](assets/images/experiment-05/11_gpt15_posed/11_gpt15_posed_010.jpg)

![NanoBanana — Studio-Szene, Querformat. Atmosphärisch stark.](assets/images/experiment-05/18_nanobanana_v2_landscape/studio.jpg)

![NanoBanana — Night Drive, Querformat.](assets/images/experiment-05/20_nanobanana_final_landscape/night_drive.jpg)

![GPT Image 1.5 — Pool-Szene, Querformat.](assets/images/experiment-05/19_gpt15_final_landscape/pool_floaty.jpg)

![NanoBanana — Spiral Staircase, Querformat.](assets/images/experiment-05/20_nanobanana_final_landscape/spiral_staircase.jpg)

![GPT Image 1.5 — Night Drive, Querformat.](assets/images/experiment-05/19_gpt15_final_landscape/night_drive.jpg)

Alle 134 Ergebnisse sind auf der Bild-Generationen-Seite zu sehen.

