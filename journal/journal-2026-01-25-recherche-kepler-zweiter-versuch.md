# Recherche — Kepler und die KI, ein zweiter Versuch

**25. Januar 2026**

Im November hatte ich mit ComfyUI versucht, konsistente Bilder von Kepler zu generieren. Es war frustrierend. Die KI interpretierte hartnäckig Gesichter in seine Voxel-Maske hinein, egal, was ich promptete. Face Detailer, PuLID, InstantID: alle auf menschliche Gesichter trainiert, alle unfähig, einen Charakter ohne Gesicht zu respektieren.

![Kepler in seiner Voxel-Form — kein Gesicht, das ist Absicht.](assets/images/kepler-voxel.png)

![Generiertes Bild aus dem ComfyUI-Experiment: Die KI hat ein Gesicht in die Maske interpretiert.](assets/journal/2025-11-16-comfyui-consistent-character/generated-kepler-003.png)

![Noch ein Versuch — wieder ein Gesicht, wo keines sein sollte.](assets/journal/2025-11-16-comfyui-consistent-character/generated-kepler-007.png)

Seitdem habe ich das Thema nicht losgelassen. In den Wochen dazwischen habe ich andere Dinge gemacht: Suno ausprobiert, mit Claude über KI-Grundlagen geredet, die Thesis-Struktur weitergedacht. Aber im Hinterkopf blieb dieses Bild: Kepler mit einem fremden Gesicht. Es fühlte sich an, als hätte das System meinen Charakter nicht nur falsch dargestellt, sondern ihn *korrigiert*. Als wäre ein gesichtsloses Wesen ein Fehler, den die KI beheben muss.

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

Beeindruckend: Gemini behält die geometrische Voxel-Form bei und fügt keine Gesichter hinzu. Aber jeder neue Prompt baut auf dem vorherigen Bild auf, statt es zu ersetzen. Für einen neuen Stil müsste ich jeweils einen neuen Chat starten.

### Chat 2: Treppe im Nachthimmel

> **"Show this character walking up a set of endless glowing stairs in the night sky. Make it a Portrait image."** → **"You did not end up making it a portrait, and I want him to be walking up, not down, and the staircase is a spiral staircase."**

![Beeindruckende Atmosphäre, aber kein Hochformat trotz explizitem Wunsch.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-stairs-nightsky.png)

![Die Spiraltreppe wurde umgesetzt, aber immer noch kein Portrait-Format. Und die Sterne liegen vor dem Planeten — physikalisch unmöglich.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-stairs-spiral.png)

Die Voxel-Ästhetik bleibt konsistent, kein Gesicht hinzugefügt. Aber Gemini ignoriert die Portrait-Anweisung zweimal, und die Sterne vor dem Planeten zeigen, dass das Modell kein räumliches Verständnis der Szene hat. Es komponiert visuell, nicht physikalisch.

### Chat 3: Brücke bei Nacht

> **"Das hier sind ein paar Beispielbilder von Kepler. Behalte seine Voxel-Ästhetik bei und generiere mir ein hochkant ästhetisches Cover. Wie er über eine Brücke in der Nacht fährt in einem Retro-Auto."** → **"Sorge dafür, dass der Brückenzaun nicht leuchtet. Wähle eine andere Perspektive und entferne den Text."** → **"Die Barrikaden der Brücke leuchten immer noch."**

Ich hatte nur "Cover" geschrieben, nicht "Album-Cover". Gemini hat den Kontext selbst erschlossen und "NIGHT DRIVE / KEPLER" als Titel gesetzt.

![Gemini generiert ungefragt ein Album-Cover mit Titel "NIGHT DRIVE / KEPLER" — es interpretiert "Cover" als Musikcover und fügt selbstständig Text hinzu.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-bridge-cover.png)

![Text entfernt, andere Perspektive — aber der Brückenzaun leuchtet weiterhin, und die Sterne-vor-Planeten-Problematik bleibt.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-bridge-notext.png)

![Dritter Versuch — die leuchtenden Barrikaden lassen sich nicht abschalten.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-bridge-stillglowing.png)

### Chat 4: Typografie auf bestehendem Cover

> **"Kannst du mir auf dieses Bild einen Album title geben: 'es tut mir leid' in liquid metal cyber tribal aesthetic geben."** → **"Jetzt soll er nur metallisch grau sein und etwas weiter oben eine andere Schriftart, die noch etwas mehr slanted ist. In den Farben des Covers selbst."** → **"Ok, bitte ändert es noch mal komplett um und verschiebt den Text nach oben."**

![Gemini setzt den Text in einer generischen Blackletter-Schrift mit leichtem Metallic-Effekt — weit entfernt von "liquid metal cyber tribal".](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-typo-liquidmetal.png)

![Kaum Veränderung — die Schrift ist minimal anders positioniert, aber weder slanted noch in den Cover-Farben.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-typo-slanted.png)

![Dritte Iteration — wieder fast identisch. "Komplett um" wurde ignoriert.](assets/journal/2026-01-25-recherche-kepler-zweiter-versuch/gemini-nanobanana-typo-moved.png)

Drei Iterationen, kaum Unterschied. Keine der Anweisungen — liquid metal, cyber tribal, slanted, Cover-Farben, komplett anders — wurde umgesetzt. Typografie ist offensichtlich eine Schwachstelle: Gemini kann Text auf Bilder setzen, aber die ästhetische Kontrolle über Schriftart, Stil und Platzierung fehlt fast vollständig.

### Zwischenfazit Gemini

Die vier Chats zeigen ein klares Bild: Gemini ist beeindruckend darin, die Voxel-Ästhetik beizubehalten und Szenen zu generieren. Als Inspirationsquelle funktioniert es. Aber für Art Direction ist das Chat-Fenster unbrauchbar. Manche Anweisungen werden präzise befolgt (Szenen-Änderungen, Text entfernen), andere hartnäckig ignoriert (Hochformat, Leuchteffekte, Typografie-Stil, Sterne-vor-Planeten-Physik). Für jeden neuen Anlauf muss man einen frischen Chat öffnen, und selbst dann ist die Kontrolle zu grob. Für feinere Steuerung bräuchte man die API oder spezialisierte Tools wie NanoBanano in ComfyUI. Das Potenzial ist da — aber Spaß macht es nicht.

## 2D-Workaround: ControlNet Depth + Inpainting

Ein vielversprechender Ansatz: Statt Face-Tools zu nutzen, kann ich über Depth Maps arbeiten. [Flux.1-dev-Controlnet-Depth](https://huggingface.co/jasperai/Flux.1-dev-Controlnet-Depth) extrahiert die räumliche Struktur eines Bildes und nutzt sie als Kontrollsignal, ohne das Gesicht interpretieren zu müssen. Kombiniert mit Inpainting könnte ich Kepler-Referenzen mit Tiefenkarte einspeisen und die KI nur den Stil und die Umgebung generieren lassen, während die Silhouette erhalten bleibt.

Das umgeht das Face-Problem elegant: Die Depth Map sieht nur Geometrie, keine Gesichtszüge.

## Von der Frustration zum System

Die Gemini-Chats haben gezeigt: Das Potenzial ist da, aber die Steuerung über ein Chat-Fenster ist zu grob. Manche Anweisungen werden befolgt, andere ignoriert. Bei jedem neuen Versuch muss ich einen frischen Chat öffnen. Das skaliert nicht.

Parallel hatte ich [fal.ai](https://fal.ai) entdeckt, eine Plattform, die gehostete Inferenz für dutzende Bildmodelle anbietet. Kein lokales Setup, keine GPU, alles über API. Die Idee: Statt manuell in Chat-Fenstern zu experimentieren, ein Python-Skript schreiben, das systematisch verschiedene Modelle mit denselben Prompts und Referenzbildern aufruft. Cursor und Claude Code als Entwicklungsumgebung, fal.ai als Inferenz-Backend.

Der Workflow-Shift war fundamental: Nicht mehr "wie überrede ich ein einzelnes Modell?" — sondern "wie vergleiche ich neun Modelle systematisch miteinander?". Ein Automatisierungs-Problem statt eines Überredungs-Problems. Das erste Mal, dass Claude Code nicht nur bei der Recherche half, sondern den gesamten Experiment-Workflow ermöglichte: Skript schreiben, API-Calls strukturieren, Ergebnisse sortieren.

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

## Reflexion

- **Tools:** Gemini/NanoBanano Pro, fal.ai API, Claude Code, VS Code, Blender (Referenzrender)
- **Workflow:** fundamental verändert — vom manuellen Überreden eines Modells zum automatisierten Vergleich von neun Modellen über API, mit strukturierter Bewertung per Interview
- **Autorschaft:** technische Problemlöserin und Kuratorin — Claude Code gab Instruktionen, ich setzte auf, bezahlte, bewertete; Autorschaft war schon vor KI-Einsatz verteilt (Keplers 3D-Modell stammt von Gavin und anderen Artists)
- **Iteration:** reproduzierbarer Workflow für zukünftige Modellvergleiche entstanden; schnelle Ergebnisse ermöglichten breites Screening, aber ungenaue Instruktionen führten zu verschwendeten Runs (z.B. Bild gestretcht statt erweitert)
- **Scheitern:** Gemini ignoriert Anweisungen selektiv (Hochformat, Leuchteffekte, Typografie-Stil) — Chat-basierte Art Direction skaliert nicht; Claude Code stretchte Bild statt es zu erweitern, weil Instruktion zu vage war
- **Erkenntnis:** "Ich fühle mich nicht wie eine Künstlerin — macht mir aber nichts aus." Autorschaft ist in diesem Projekt von Anfang an verteilt, nicht erst durch KI

**Keywords:** #fal.ai #Automatisierung #Kuratorin #FaceBias #Autorschaft

<div class="interview-transcript">
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Welche Tools hast du in dieser Session verwendet?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Ich habe erstmal meine Referenz, die ich in Blender gerendert habe, in Gemini gepackt. Die hat sich dann NanoBanano Pro bedient. Das war mir dann aber zu tricky, deswegen habe ich fal.ai benutzt. Ich benutze mittlerweile gar nicht mehr Cursor, sondern VS Code, weil das kostenlos ist, und ich bin komplett auf Claude Code umgestiegen.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Was wolltest du erreichen?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Ich wollte endlich erfolgreiche Generationen machen und visuell cool aussehende Bilder erstellen, die nahe an finaler Qualität sind. Und ich wollte die neuen Modelle ausprobieren, ohne extremen Aufwand zu betreiben — es sind ständig neue da und es ist schwer zu wissen, was das Beste ist. Ich wollte auch mit Automatisierung und agentischen Workflows in Claude Code spielen.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Hat sich dein Arbeitsablauf verändert?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Der gesamte Workflow hat sich fundamental verändert. Anstatt dieses schwierigen Arbeitens mit ComfyUI hatte ich plötzlich dieses total automatisierte Setup mit Claude, wo ich zu den einzelnen Bildern interviewt wurde. Ich konnte mir durch die verschiedenen Ergebnisse ein besseres Bild machen. Durch die objektive Bewertung per Interview und die Erstellung der Tabelle konnte ich am Ende wirklich sagen: das funktioniert oft gut und das nicht. Dadurch habe ich mit Hilfe der KI recherchiert, was Best Practices sind. Die Ergebnisse wurden dadurch teilweise besser — zum Beispiel das quadratische Aspect Ratio, welches ich dann ins Portrait- oder Landschaftsformat bringen konnte.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Wie hast du deine Rolle in diesem Prozess erlebt?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Ich war technische Problemlöserin. Instruktionsbefolgerin. Claude Code hat mir wirklich detaillierte Instruktionen gegeben, wie ich das Ganze aufsetzen soll. Aber ich bin selber auf die Idee gekommen, habe mich auf der Seite registriert, den API Key geholt, das Ganze bezahlt. Es war eigentlich genau Kuratorin: Ich habe etwas Technisches ausprobiert und dann bewertet. Davor habe ich die technischen Komponenten nach Anleitung von Claude Code zusammengestellt. Ich fühle mich nicht wirklich wie eine Künstlerin gerade. Macht mir aber auch nicht unbedingt was aus. Ich fand es einfach erleichternd und cool, mal interessante Ergebnisse zu kriegen.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Wie hat die schnelle KI-Ausgabe deinen Prozess beeinflusst?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Ich habe viel mehr Modelle ausprobiert, als es ohne KI jemals möglich gewesen wäre. Es ist ein reproduzierbarer Workflow — das werde ich in der Zukunft wieder benutzen. Da es immer wieder neue Modelle geben wird, und ich jetzt weiß, dass ich in dieser Domäne zu Ergebnissen kommen kann, werde ich es weiterhin so automatisiert mit Claude Code über einen API Key machen.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Was ist schiefgelaufen und was hast du daraus gelernt?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Da ich das Bild nicht selber breiter oder höher gemacht habe, sondern die KI gesagt hat, sie soll es machen, hat sie mich missverstanden und hat das Bild gestretcht. Dadurch habe ich Geld und Zeit verloren mit verzerrten Ergebnissen. Genauso schnell wurde es behoben, aber manchmal ist es frustrierend, die KI zu korrigieren. Da hilft es natürlich, sich präzise auszudrücken. Ich tendiere dazu, schnell die Instruktion zu geben und schnell das Ergebnis haben zu wollen — dann gebe ich mir nicht so viel Mühe, genau zu beschreiben, was ich will.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Hat sich eine eigene visuelle Sprache entwickelt?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Nicht unbedingt eine eigene Sprache, denn die Ästhetik wurde durch Kepler selbst — das 3D-Modell, welches wir erstellt haben, und das, was die KI dazu gedacht hat — erstellt. Ich habe da noch nicht viel mit dem Prompting rumgespielt, ob man etwas Stil reinbringen kann.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Du beschreibst den Shift vom „Überredungs-Problem" zum „Automatisierungs-Problem". Gleichzeitig sagst du, du fühlst dich nicht wie eine Künstlerin, sondern wie eine Kuratorin. Hat dieser Wechsel etwas an deiner Beziehung zu den Ergebnissen verändert?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Die Bilder fühlen sich von Anfang an nicht nach etwas an, das ich selber gemacht habe. Klar, ich habe das Modell gerendert und ein bisschen daran gearbeitet, aber das Grund-3D-Modell wurde von jemand anderem erzeugt — von Gavin. Er hat mit anderen 3D Artists den Voxel-Kepler entworfen, und ich habe ihn nur modifiziert. Also sehe ich die 3D-Figur nicht als meine Kreation. Hätte ich das Charakterdesign, den Charakter selber und die komplette 3D-Modellierung von Anfang an erstellt, dann hätte ich wahrscheinlich ein viel höheres Gefühl der Autorschaft. So hält es sich in Grenzen. Aber allgemein ist es in diesem Projekt so, dass ich nicht die einzige Autorin bin. Das fällt mir übrigens gerade erst ein, wie du mir diese Frage stellst.</p></div>
</div>
</div>

