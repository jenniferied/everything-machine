# Video-Generierung — Kepler in Bewegung

**15. Februar 2026**

Nach dem Bildgenerierungs-Experiment war die Frage unvermeidlich: Können die Bilder in Bewegung kommen? Kepler im Studio sitzend, beeindruckend als Standbild. Aber was, wenn er nickt? Wenn das Wasser im Pool kräuselt? Wenn das Auto tatsächlich fährt?

Die fal.ai-Pipeline war bereits aufgesetzt, also lag der nächste Schritt nahe: Image-to-Video. Sieben Modelle, vier Szenen, 28 generierte Videos. Ein systematischer Vergleich nach demselben Prinzip wie beim Bildexperiment. Dieselbe Frage, eine Dimension weiter: Respektieren die Modelle Keplers gesichtslose Voxel-Ästhetik, wenn die Bilder sich bewegen?

Das Setup: Ein Python-Skript, das vier Szenen-Bilder aus Experiment 05 nimmt und sie über fal.ai an sieben Image-to-Video-Modelle schickt. Jedes Modell bekommt dasselbe Bild und denselben Prompt. Die einzige Variable ist das Modell selbst. Die Ergebnisse: ein CSV mit 28 Bewertungen und 28 MP4-Dateien.

## Die Input-Bilder

Vier Szenen aus dem Bildexperiment, alle generiert mit NanoBanana Pro (Gemini 2.5 Flash), bewusst gewählt für unterschiedliche Herausforderungen:

![Studio (Querformat) — Kepler am Mischpult. Die einfachste Szene: klare Geometrie, kontrollierte Beleuchtung.](assets/images/experiment-05/14_nanobanana_scenes_landscape/studio.jpg)

![Pool (Hochformat) — Kepler auf einem Pool-Floaty, Draufsicht. Schwieriger: Wasser, Gesicht sichtbar, Hochformat.](assets/images/experiment-05/24_nanobanana_apose_portrait/pool_floaty.jpg)

![Night Drive (Hochformat) — Kepler im Retro-Auto bei Nacht. Die technisch anspruchsvollste Szene.](assets/images/experiment-05/20_nanobanana_final_portrait/night_drive.jpg)

![Spiral Staircase (Hochformat) — Kepler auf einer leuchtenden Wendeltreppe. Komplexe Geometrie und Glow.](assets/images/experiment-05/18_nanobanana_v2_portrait/spiral_staircase.jpg)

Eine Querformat-Szene, drei Hochformat-Szenen. Das war Absicht: Das Bildexperiment hatte gezeigt, dass Hochformat für die Modelle schwieriger ist. Beim Video wollte ich wissen, ob sich das bestätigt.

## Die Modelle

| Modell | Kosten/Video | Studio | Pool | Night Drive | Staircase | Gesamt |
|--------|:------------:|:------:|:----:|:-----------:|:---------:|:------:|
| **Kling O3** | $0,84 | Gut | Gut | Schlecht | Gut | **Bestes Modell** |
| **Kling 3.0 V3** | $0,84 | Gut | Gut | Okay | Schlecht | **Zweiter Platz** |
| Veo 3.1 | $0,80 | Schlecht | Gut | Okay | Okay | Durchwachsen |
| Seedance Pro | $0,62 | Okay | Schlecht | Gut | Okay | Überraschungen |
| Wan 2.6 | $0,50 | Gut | Schlecht | Schlecht | Okay | Inkonsistent |
| PixVerse v5.5 | $0,20 | Okay | Schlecht | Schlecht | Okay | Zu billig |
| LTX-2 | $0,36 | Gut | Schlecht | Schlecht | Schlecht | **Verlierer** |

Die Preise reichen von $0,20 (PixVerse) bis $0,84 (Kling) pro Video, und die Kosten-Qualitäts-Korrelation ist stärker als bei Bildern: Günstige Modelle scheitern fast durchgehend.

## Highlights

**Kling O3 — Studio:** Kepler bewegt sich subtil zum Beat, die Finger liegen auf dem Mischpult, die Monitore glühen stabil. Natürlichste Bewegung aller Modelle.

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/kling_o3_studio.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">Kling O3 — Studio. Subtile Bewegung, stabile Voxel-Ästhetik.</figcaption></figure>

**Kling 3.0 V3 — Pool:** Das beste Video des gesamten Tests. Keine Gesichtshalluzination, natürliche Wasserbewegung, der Floaty dreht sich langsam. Bewertungskommentar: *"Das beste!"*

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/kling_v3_pool.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">Kling 3.0 V3 — Pool. Keine Halluzination, natürliche Wasserbewegung.</figcaption></figure>

**Seedance Pro — Night Drive:** Die größte Überraschung. Das Modell, das beim Pool und Studio enttäuschte, lieferte das beste Night-Drive-Ergebnis aller sieben Modelle. Keine Gesichtshalluzination, flüssige Fahrbewegung.

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/seedance_pro_night_drive.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">Seedance Pro — Night Drive. Überraschend gut, keine Halluzination.</figcaption></figure>

## Lowlights

**PixVerse v5.5 — Night Drive:** Das Gesicht verändert sich zu einer Art Lego-Figur. Der Face-Bias wird hier am deutlichsten sichtbar. Das Modell "korrigiert" Keplers gesichtslose Maske Frame für Frame.

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/pixverse_v55_night_drive.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">PixVerse v5.5 — Night Drive. Gesichtshalluzination: Kepler wird zur Lego-Figur.</figcaption></figure>

**LTX-2 — Night Drive:** Das Auto fährt rückwärts, das Seitenverhältnis hat sich geändert, der Blickwinkel stimmt nicht. Drei Fehler in einem Video.

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/ltx2_night_drive.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">LTX-2 — Night Drive. Auto fährt rückwärts, Seitenverhältnis geändert.</figcaption></figure>

**Kling 3.0 V3 — Spiral Staircase:** Ausgerechnet das zweitbeste Modell scheitert hier komplett. Die Stufen funktionieren nicht, das Leuchten wirkt unnatürlich, und die Kamera bewegt sich in eine völlig unerwartete Richtung. Pool-Gewinner, Treppen-Verlierer.

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/kling_v3_spiral_staircase.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">Kling 3.0 V3 — Spiral Staircase. Stufen, Leuchten und Kamera — alles geht schief.</figcaption></figure>

## Portrait vs. Landscape

Die überraschendste Erkenntnis: Hochformat-Bilder sind für Video-Modelle schwieriger als Querformat.

Im Studio (Querformat) lieferten fast alle Modelle brauchbare Ergebnisse. Sobald es ins Hochformat ging (Pool, Night Drive, Spiral Staircase), brach die Qualität bei den günstigeren Modellen ein. Das Hauptproblem: **Gesichtshalluzination**. Keplers gesichtslose Voxel-Maske wird im Video nach und nach mit Augen, Nase, Mund gefüllt, als wolle das Modell "korrigieren", was es für einen Fehler hält.

Die Gesichtshalluzination im Video ist schlimmer als im Standbild: Sie passiert *progressiv*. Das erste Frame sieht noch richtig aus, aber über die Sekunden hinweg "wächst" ein Gesicht in die Maske hinein. Das Face-Bias-Problem aus dem Bildexperiment multipliziert sich über die Zeit.

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/wan_v26_pool.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">Wan 2.6 — Pool. Das Gesicht wächst über die Videodauer in die Maske hinein.</figcaption></figure>

## Überraschungen und Gotchas

**Wan 2.6 generiert Audio**, auch wenn man es nicht anfordert. Es gibt keinen zuverlässigen Parameter, um die Audio-Generierung zu deaktivieren. Ein Gotcha, das in der API-Dokumentation nicht erwähnt wird.

**LTX-2 ändert das Seitenverhältnis** bei Portrait-Input. Aus 9:16 wird etwas, das weder 9:16 noch 16:9 ist. Für eine Pipeline, die mit gemischten Orientierungen arbeitet, ein Ausschlusskriterium.

**"Camera holds still"** im Prompt verhindert Kamerabewegung nicht zuverlässig. Manche Modelle interpretieren es als Vorschlag, nicht als Anweisung. Kling O3 und Veo 3.1 halten sich am ehesten daran.

**Zwei Modelle ließen das Auto rückwärts fahren**: LTX-2 und Veo 3.1 interpretierten die Fahrtrichtung falsch in der Night-Drive-Szene.

Alle 28 Videos sind auf der Video-Generationen-Seite zu sehen.

## Reflexion

- **Tools:** fal.ai API, Claude Code, Python-Skript (von Claude Code geschrieben), 7 Image-to-Video-Modelle
- **Workflow:** durch bestehende Bild-Pipeline einfacher als beim ersten Mal — selbes Prinzip, eine Dimension weiter; reproduzierbarer agentischer Workflow reduziert Aufwand für zukünftige Modellvergleiche drastisch
- **Autorschaft:** neugierige Kuratorin — systematisches Bewerten hat Spaß gemacht; Spannung zwischen quantitativen und qualitativen Ergebnissen; die eigentliche kreative Arbeit mit Gavin steht noch bevor
- **Iteration:** agentischer Workflow gibt Confidence — "Recherchiere die neuesten Modelle und generiere mir fünf Beispielbilder" reicht als Instruktion; viel schneller als manuelles Chat-Fenster-Ping-Pong
- **Ästhetik:** kein eigener Stil entwickelt — Prompting wurde noch nicht für Stil-Experimente genutzt; nächster Schritt: Pinterest-Referenzen und Gavins ästhetische Vision einbringen
- **Erkenntnis:** brauchbare Ergebnisse sind erst der Startpunkt, nicht das Ziel — jetzt, wo die Technik funktioniert, beginnt die eigentliche kreative Iteration mit dem Künstler

**Keywords:** #ImageToVideo #FaceHalluzination #AgentischerWorkflow #Kuratorin #PromptAdherence

<div class="interview-transcript">
<div class="chat-message claude">
  <div class="chat-avatar"><img src="assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Welche Tools hast du in dieser Session verwendet?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Ich habe wieder fal.ai API und Claude Code verwendet. Claude Code hat für mich ein Python-Skript geschrieben, in dem ich sieben verschiedene Video-Modelle ansprechen konnte.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Was wolltest du erreichen?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Ich wollte diesen Workflow noch mal an Videos testen. Ich war endlich zufrieden mit den Bildergebnissen und dachte, ich könnte diese als Ausgangsbilder für Image-to-Video-Modelle benutzen. Das bringt mich näher an mein Endziel: Cover-Grafiken und Spotify-Reels für Kepler. Ich wollte schauen, wie nah ich an ein brauchbares Ergebnis kommen kann.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Hat sich dein Arbeitsablauf verändert im Vergleich zum Bild-Experiment?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Es war einfacher durch die bestehende Pipeline als zuvor. Ansonsten war es sehr ähnlich und auch sehr interessant. Die Halluzinationen waren besonders interessant — es sind einfach viel mehr Elemente, die schiefgehen können oder interessant sein könnten.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Wie hast du deine Rolle in diesem Prozess erlebt?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Wieder Kuratorin — Anweisungen geben und dann kuratieren. Vielleicht war ich hier auch ein bisschen mehr Erforscherin. Ich habe mich neugierig gefühlt, was die Ergebnisse angeht. Ich hatte mich in dieses systematische Bewerten eingegroovt und war gespannt auf die quantitativen und qualitativen Ergebnisse.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Wie hat die schnelle KI-Ausgabe deinen Prozess beeinflusst?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Ich konnte mehr Experimente machen, genauso wie bei den Bildern. Ich habe jetzt einen reproduzierbaren Workflow und kann jedes neue Modell einfach ausprobieren, ohne Burnout. Ich sage der KI einfach: „Recherchiere die neuesten Modelle und generiere mir fünf Beispielbilder" — und dann habe ich ein Resultat. Es hat mir Confidence gegeben, dass KI auch coole, schnelle Ergebnisse liefern kann, bei denen man schnell iterieren kann. Es ist viel aufwändiger, alles in einen Chatbot zu schreiben und rein- und rauszukopieren — durch den agentischen Workflow mit Claude Code wird das automatisiert.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Was ist schiefgelaufen und was hast du daraus gelernt?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>[Keine spezifischen Probleme über die im Journal dokumentierten hinaus.]</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Hat sich eine eigene visuelle Sprache entwickelt?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Es ist gar nicht meine eigene visuelle Sprache! Ich habe in den Prompts gar nicht mit dem Stil experimentiert — das ist eine Frage für weitere Experimente. An sich finde ich den Style cool, aber er ist nicht meiner. Oder der von Kepler. Auch wenn Kepler dort teilweise gut drin aussieht.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Die Gesichtshalluzination passiert im Video progressiv — Frame für Frame wächst ein Gesicht in die Maske. Siehst du darin etwas über Keplers Identität, oder ist das eher ein technisches Problem?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Ich bin gar nicht die Schöpferin von Kepler — ich setze seine Vision um. Seine ästhetischen Qualitäten sind in unserem Pinterest Board zu finden. Ich bin noch gar nicht an dem Punkt, wo ich unsere Inputs verwende oder ihn mit reinbringe. Jetzt, wo die Modelle funktionieren — und das ist relativ neu, diese Prompt Adherence, wahrscheinlich durch die Kombination von Large Language Models mit bildgenerierenden Modellen — ist der Moment, wo ich zum Künstler gehe und mit ihm zusammen iteriere. Oder erstmal in unsere Referenzen gehe und versuche, genau diesen Stil nachzubilden.</p></div>
</div>
</div>
