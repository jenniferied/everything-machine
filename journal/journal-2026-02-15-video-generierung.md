# Video-Generierung — Kepler in Bewegung

**15. Februar 2026**

Nach dem Bildgenerierungs-Experiment war die Frage unvermeidlich: Können die Bilder in Bewegung kommen? Kepler im Studio sitzend — beeindruckend als Standbild. Aber was, wenn er nickt? Wenn das Wasser im Pool kräuselt? Wenn das Auto tatsächlich fährt?

Die fal.ai-Pipeline war bereits aufgesetzt, also lag der nächste Schritt nahe: Image-to-Video. Sieben Modelle, vier Szenen, 28 generierte Videos — ein systematischer Vergleich nach demselben Prinzip wie beim Bildexperiment. Dieselbe Frage, eine Dimension weiter: Respektieren die Modelle Keplers gesichtslose Voxel-Ästhetik auch, wenn die Bilder anfangen, sich zu bewegen?

Das Setup: Ein Python-Skript, das vier Szenen-Bilder aus Experiment 05 nimmt und sie über fal.ai an sieben Image-to-Video-Modelle schickt. Jedes Modell bekommt dasselbe Bild und denselben Prompt — die einzige Variable ist das Modell selbst. Die Ergebnisse: ein CSV mit 28 Bewertungen und 28 MP4-Dateien.

## Die Input-Bilder

Vier Szenen aus dem Bildexperiment — alle generiert mit NanoBanana Pro (Gemini 2.5 Flash) — bewusst gewählt für unterschiedliche Herausforderungen:

![Studio (Querformat) — Kepler am Mischpult. Die einfachste Szene: klare Geometrie, kontrollierte Beleuchtung.](assets/images/experiment-05/14_nanobanana_scenes_landscape/studio.jpg)

![Pool (Hochformat) — Kepler auf einem Pool-Floaty, Draufsicht. Schwieriger: Wasser, Gesicht sichtbar, Hochformat.](assets/images/experiment-05/24_nanobanana_apose_portrait/pool_floaty.jpg)

![Night Drive (Hochformat) — Kepler im Retro-Auto bei Nacht. Die technisch anspruchsvollste Szene.](assets/images/experiment-05/20_nanobanana_final_portrait/night_drive.jpg)

![Spiral Staircase (Hochformat) — Kepler auf einer leuchtenden Wendeltreppe. Komplexe Geometrie und Glow.](assets/images/experiment-05/18_nanobanana_v2_portrait/spiral_staircase.jpg)

Eine Querformat-Szene, drei Hochformat-Szenen. Das war Absicht: Das Bildexperiment hatte gezeigt, dass Hochformat für die Modelle schwieriger ist — und beim Video wollte ich wissen, ob sich das bestätigt.

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

Die Preise reichen von $0,20 (PixVerse) bis $0,84 (Kling) pro Video — und die Kosten-Qualitäts-Korrelation ist stärker als bei Bildern: Günstige Modelle scheitern fast durchgehend.

## Highlights

**Kling O3 — Studio:** Kepler bewegt sich subtil zum Beat, die Finger liegen auf dem Mischpult, die Monitore glühen stabil. Natürlichste Bewegung aller Modelle.

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/kling_o3_studio.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">Kling O3 — Studio. Subtile Bewegung, stabile Voxel-Ästhetik.</figcaption></figure>

**Kling 3.0 V3 — Pool:** Das beste Video des gesamten Tests. Keine Gesichtshalluzination, natürliche Wasserbewegung, der Floaty dreht sich langsam. Bewertungskommentar: *"Das beste!"*

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/kling_v3_pool.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">Kling 3.0 V3 — Pool. Keine Halluzination, natürliche Wasserbewegung.</figcaption></figure>

**Seedance Pro — Night Drive:** Die größte Überraschung. Das Modell, das beim Pool und Studio enttäuschte, lieferte das beste Night-Drive-Ergebnis aller sieben Modelle. Keine Gesichtshalluzination, flüssige Fahrbewegung.

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/seedance_pro_night_drive.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">Seedance Pro — Night Drive. Überraschend gut, keine Halluzination.</figcaption></figure>

## Lowlights

**PixVerse v5.5 — Night Drive:** Das Gesicht verändert sich zu einer Art Lego-Figur. Der Face-Bias wird hier am deutlichsten sichtbar — das Modell "korrigiert" Keplers gesichtslose Maske Frame für Frame.

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/pixverse_v55_night_drive.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">PixVerse v5.5 — Night Drive. Gesichtshalluzination: Kepler wird zur Lego-Figur.</figcaption></figure>

**LTX-2 — Night Drive:** Das Auto fährt rückwärts, das Seitenverhältnis hat sich geändert, der Blickwinkel stimmt nicht. Drei Fehler in einem Video.

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/ltx2_night_drive.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">LTX-2 — Night Drive. Auto fährt rückwärts, Seitenverhältnis geändert.</figcaption></figure>

**Kling 3.0 V3 — Spiral Staircase:** Ausgerechnet das zweitbeste Modell scheitert hier komplett. Die Stufen funktionieren nicht, das Leuchten wirkt unnatürlich, und die Kamera bewegt sich in eine völlig unerwartete Richtung. Pool-Gewinner, Treppen-Verlierer.

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/kling_v3_spiral_staircase.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">Kling 3.0 V3 — Spiral Staircase. Stufen, Leuchten und Kamera — alles geht schief.</figcaption></figure>

## Portrait vs. Landscape

Die überraschendste Erkenntnis: Hochformat-Bilder sind für Video-Modelle *deutlich* schwieriger als Querformat.

Im Studio (Querformat) lieferten fast alle Modelle brauchbare Ergebnisse. Sobald es ins Hochformat ging — Pool, Night Drive, Spiral Staircase — brach die Qualität bei den günstigeren Modellen ein. Das Hauptproblem: **Gesichtshalluzination**. Keplers gesichtslose Voxel-Maske wird im Video nach und nach mit Augen, Nase, Mund gefüllt — als ob das Modell "korrigieren" will, was es für einen Fehler hält.

Die Gesichtshalluzination im Video ist schlimmer als im Standbild: Sie passiert *progressiv*. Das erste Frame sieht noch richtig aus, aber über die Sekunden hinweg "wächst" ein Gesicht in die Maske hinein. Das Face-Bias-Problem aus dem Bildexperiment multipliziert sich über die Zeit.

<figure class="image-figure my-4"><video src="assets/videos/experiment-06/wan_v26_pool.mp4" controls muted loop playsinline class="img-100 rounded-sm"></video><figcaption class="image-caption">Wan 2.6 — Pool. Das Gesicht wächst über die Videodauer in die Maske hinein.</figcaption></figure>

## Überraschungen und Gotchas

**Wan 2.6 generiert Audio** — auch wenn man es nicht anfordert. Es gibt keinen zuverlässigen Parameter, um die Audio-Generierung zu deaktivieren. Ein Gotcha, das in der API-Dokumentation nicht erwähnt wird.

**LTX-2 ändert das Seitenverhältnis** bei Portrait-Input. Aus 9:16 wird etwas, das weder 9:16 noch 16:9 ist. Für eine Pipeline, die mit gemischten Orientierungen arbeitet, ein Ausschlusskriterium.

**"Camera holds still"** im Prompt verhindert Kamerabewegung nicht zuverlässig. Manche Modelle interpretieren es als Vorschlag, nicht als Anweisung. Kling O3 und Veo 3.1 halten sich am ehesten daran.

**Zwei Modelle ließen das Auto rückwärts fahren** — LTX-2 und Veo 3.1 interpretierten die Fahrtrichtung falsch in der Night-Drive-Szene.

Alle 28 Videos sind auf der Video-Generationen-Seite zu sehen.
