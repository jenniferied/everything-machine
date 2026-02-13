# Website für Artistic Research mit Cursor aufsetzen

**19. November 2025**

Für mein Artistic Research-Projekt "Everything Machine (Kepler)" brauchte ich eine Website, die sowohl den wissenschaftlichen Anspruch erfüllt als auch die künstlerische Identität von Kepler widerspiegelt. Statt mit einem fertigen CMS zu arbeiten, habe ich mich entschieden, die Seite von Grund auf mit [Cursor](https://cursor.sh) zu bauen – einem AI-gestützten Code-Editor, der mir dabei hilft, schneller zu entwickeln und gleichzeitig den Code sauber zu halten.

## Technical Setup: Cursor und GitHub

Cursor ist im Grunde ein Fork von VS Code, der mit KI-Features erweitert wurde. Man kann direkt im Editor mit der KI chatten, Code generieren lassen oder bestehenden Code refactoren. Für mich war das perfekt, weil ich so nicht ständig zwischen Browser und Dokumentation wechseln musste – die KI kennt den Kontext meines Projekts und kann direkt helfen.

![Cursor Oberfläche. Links die Liste der Dateien im GitHub Repository, in der Mitte eine Datei mit Changes, die die KI gemacht hat (die accepted werden können – in diesem Fall ein Prompt um das Layout zu fixen), rechts der Agent View, der ein Modell (in diesem Fall GPT 5.1 Codex) nutzt, um Prompts umzusetzen.](assets/journal/2025-11-19-cursor-build/cursor-interface-screenshot.png)

Das Projekt ist komplett in Git versioniert. Jede größere Änderung wurde als Commit festgehalten, was es mir ermöglicht, den Entwicklungsprozess nachzuvollziehen. Die Struktur ist simpel: `index.html` für die Hauptseite, `scripts.js` für die Logik, `style.css` für das Styling, und ein `journal/` Ordner für alle Markdown-Einträge. Keine komplexen Build-Tools, keine Dependencies außer Tailwind CSS über CDN – alles läuft direkt im Browser.

## Design: Research Catalogue inspiriert, aber dunkel

Als Inspiration diente mir die [Research Catalogue](https://www.researchcatalogue.net/) – eine Plattform für Artistic Research, die ich während meines Studiums kennengelernt habe. Die hat diesen cleanen, wissenschaftlichen Look mit klarer Navigation und guter Lesbarkeit. Ich habe mir das Konzept geliehen, aber es für Kepler angepasst.

![Research Catalogue Layout-Beispiel. Ein cooler Artikel auf researchcatalogue.net, der das Layout demonstriert – cleanes Design mit klarer Navigation und guter Lesbarkeit.](assets/journal/2025-11-19-cursor-build/research-catalogue-layout-screenshot.png)

Ein besonders gutes Beispiel für das Research Catalogue Design ist dieser [Design Phenomenographies for Industrial Wastelands](https://www.researchcatalogue.net/view/2829981/3316740), der zeigt, wie multimediale Inhalte in einem wissenschaftlichen Kontext präsentiert werden können.

Statt hellem Hintergrund gibt es einen dunklen Theme (#111), der besser zu Keplers digitaler Identität passt. Die Navigation funktioniert ähnlich wie bei Research Catalogue – ein Dropdown-Menü oben links mit den Hauptsektionen. Links werden als "Pills" dargestellt (abgerundete Buttons), was moderner wirkt als normale Textlinks.

Das Besondere sind die Pixel-Headings. Kepler hat diese Voxel-Ästhetik, und um das visuell zu transportieren, verwende ich die "Press Start 2P" Font von Google Fonts für alle Überschriften. Das gibt der Seite sofort diesen retro-digitalen Vibe, ohne dass es zu verspielt wirkt. Die Hauptüberschriften im Journal haben sogar einen animierten Gradient-Effekt, der von grün zu weiß übergeht – eine Referenz an die Matrix-Ästhetik, die zu Keplers digitaler Existenz passt.

## Musikplayer: Medien-Enhancement im Header

Ein wichtiger Teil des Projekts ist die Musik von Kepler. Statt die Songs nur als statische Links einzubinden, habe ich einen Mini-Player in die Navigation integriert. Der bleibt immer sichtbar, auch wenn man durch die Seiten navigiert, und spielt die Songs aus einer Playlist ab.

Technisch funktioniert das so: In `scripts.js` gibt es ein `playlist` Array, in dem alle Songs mit Metadaten (Titel, Album, Cover, Spotify-Link) gespeichert sind. Der Player nutzt das native HTML5 `<audio>` Element und zeigt den aktuellen Track in einem Marquee-Text an. Über einen Playlist-Button kann man alle verfügbaren Songs sehen und direkt wechseln.

Die Implementierung war relativ simpel – keine externe Library nötig. Der Player lädt die Metadaten (Dauer) asynchron, damit die Seite schnell bleibt. Die Playlist wird dynamisch generiert, sodass ich einfach neue Songs zum Array hinzufügen kann, ohne HTML ändern zu müssen.

## Titelseite: Abstract als Basis

Die erste Seite ("Projektübersicht") basiert direkt auf meinem Abstract. Der Text steht prominent oben in einem abgesetzten Container, gefolgt von Einleitung, Forschungsfragen und Methodologie. Das Layout ist zentriert und auf Lesbarkeit optimiert – max-width von 4xl, damit die Zeilenlänge nicht zu lang wird.

Die Struktur ist bewusst einfach gehalten: keine komplexen Animationen, keine überladenen Effekte. Der Fokus liegt auf dem Inhalt, was für eine wissenschaftliche Arbeit wichtig ist. Die Bilder sind in einem Grid angeordnet, mit Fallback-Placeholders falls Dateien fehlen.

## Logbuch: Pixel-Effekt und horizontale Timeline

Das Herzstück der Website ist das Prozess-Logbuch. Hier werden alle Journal-Einträge aus dem `journal/` Ordner automatisch geladen und angezeigt. Jeder Eintrag ist eine Markdown-Datei, die beim Laden geparst und in ein Grid-Layout umgewandelt wird.

Die Timeline oben ist horizontal scrollbar und zeigt alle verfügbaren Einträge mit Datum und Titel. Klickt man auf einen Eintrag, wird er im Hauptbereich angezeigt. Die Einträge selbst werden in "Bubbles" dargestellt – jeder Abschnitt (überschrieben mit ## oder ###) wird zu einer eigenen Karte im Grid.

Der Pixel-Effekt kommt beim Titel zum Tragen: Wenn ein Eintrag geladen wird, erscheint der Titel mit einem Typing-Effekt, Buchstabe für Buchstabe, als würde jemand tippen. Dazu gibt es einen blinkenden Cursor. Die Font ist "Press Start 2P", und der Titel hat einen animierten Gradient, der von grün zu weiß übergeht.

Technisch wird das so umgesetzt: Der Markdown-Parser (`parseMarkdown` Funktion) teilt jeden Eintrag in Abschnitte auf. Überschriften werden zu Bubble-Titeln, der Rest wird als HTML formatiert. Bilder, Links und spezielle Komponenten (wie die WORLD_INFO Dropdowns für Marble-Welten) werden dabei berücksichtigt. Das Grid passt sich automatisch an die Bildschirmgröße an – 3 Spalten auf Desktop, 2 auf Tablet, 1 auf Mobile.

## Git-Versionierung und Projektstruktur

Jeder größere Entwicklungsschritt wurde in Git committet. Die Commits zeigen den Prozess: Zuerst die Grundstruktur, dann der Player, dann das Journal-System, dann die Timeline, dann die Bubble-Layouts. Das macht es einfach, zu sehen, wie sich die Website entwickelt hat.

Die Projektstruktur ist bewusst flach gehalten:
- `index.html` – Haupt-HTML
- `scripts.js` – Alle JavaScript-Logik (Player, Journal-Loader, Navigation)
- `style.css` – Alle Styles (Dark Theme, Grid-Layouts, Animationen)
- `journal/*.md` – Markdown-Einträge, die automatisch geladen werden
- `assets/` – Bilder, Audio, Journal-Assets

Keine Node-Modules, keine Build-Steps – alles läuft direkt im Browser. Das macht die Entwicklung schnell und das Deployment einfach. Für lokales Testen reicht ein einfacher HTTP-Server (z.B. `python -m http.server 8001`).

## Fazit

Die Website ist jetzt in Version 1.0 – Player funktioniert, Journal lädt automatisch, Design ist konsistent. Cursor hat den Prozess deutlich beschleunigt, besonders bei repetitiven Aufgaben wie dem Markdown-Parsing oder dem Grid-Layout. Die Git-Versionierung gibt mir Sicherheit, dass ich jederzeit zurückkehren kann, wenn etwas schiefgeht.

Was mir besonders geholfen hat: Ich habe bereits Erfahrung mit Web-Entwicklung, und das macht einen großen Unterschied, wenn man mit KI programmiert. Man kann die Vorschläge der KI besser einschätzen, weiß, was funktioniert und was nicht, und kann gezielt nachfragen oder anpassen. Cursor ist ein mächtiges Tool, aber es ersetzt nicht das Verständnis für die Grundlagen – es beschleunigt den Workflow enorm, wenn man weiß, was man will. Die Basis steht, und das war das Ziel.

---

## Reflexion

Das war einfach krass. Das Aufsetzen dieser Website ging tausendfach schneller als ohne KI. Ich konnte mein bestehendes Wissen einbringen, musste aber bei Kleinigkeiten nicht selbst googeln und bugfixen – Cursor und Claude haben das erledigt. Ich konnte quasi meine kreative Vision umsetzen.

Ich fühlte mich wie ein Manager mit Gesamtvision, der einen Junior Developer anleitet. Manchmal war es Kollaboration, wenn wir zusammen nicht weiterkamen. Ich habe viel reviewed – und dabei auch gelernt, weil ich in den Thinking-Prozess reinschauen konnte. Die Debugging-Schleifen waren nervig, aber ich habe gelernt, wie man die KI besser anleitet: den Chat öfter erneuern, weil zu viel Kontext die KI verschlechtert, und falsche Ansätze ablehnen statt weiterzumachen.

### Kontext

- **Tools:** Cursor, Version Control via Github, und größtenteils die Modelle von Anthropic
- **Intention:** Ich wollte sowohl die Website erstellen als auch Cursor ausprobieren, da es sich interessant für mich anhörte und ich bereits Webentwicklungserfahrung habe, aber nur sehr limitiert und es würde sehr lange dauern, wenn ich es ganz alleine mache.

### Die 5 Forschungsfragen

- **Workflow:** Oh mein Gott, das war einfach sehr krass! Das hat das Aufsetzen der Website einfach tausendfach schneller gemacht. Also, hier war der größte Unterschied zu merken, wo ich konnte mein bestehendes Wissen einbringen. Aber musste bei Kleinigkeiten nicht selber googeln und bug fixen, sondern Cursor. Die KI-Modelle haben das für mich erledigt. Ich konnte schnell experimentieren und ich hatte zwar Probleme beim Debugging, aber ich wäre gar nicht so weit gekommen ohne Cursor und Claude. Ich konnte quasi meine kreative Vision umsetzen.
- **Autorschaft:** Ich fühlte mich wie ein Manager mit Gesamtvision, der einen Junior Developer anleitet. Irgendwann wurde es eher Kollaboration, wenn wir zusammen nicht weiterkamen. Ich habe viel reviewed – und dabei auch gelernt, weil ich in den Thinking-Prozess reinschauen konnte.
- **Iteration:** Die KI-Ausgabe war sofort da – Code, Layouts, Fixes. Das hat meinen Workflow massiv beschleunigt, aber manchmal habe ich zu schnell akzeptiert, ohne den Code richtig zu verstehen. Das Tempo verleitet zur Oberflächlichkeit.
- **Scheitern:** Also, wir kamen ab und zu in Debugging-Schleifen. Das war schon sehr nervig, aber ich habe dann besser gelernt, wie man die KI anleiten kann. Zum Beispiel, dass man öfter den Chat erneuern sollte, damit umso mehr Informationen im Kontext sind, desto schlechter die KI funktioniert. Es wurden auch falsche Ansätze gewählt, welche ich dann ablehnen musste bzw. zurückrudern musste.
- **Ästhetik:** Ja, ein bisschen Kepler-DNA und der Matrix-Look. Ich mag dunkle Websites, und ich hatte mich ja vom Research Catalogue inspirieren lassen. Da waren die Artikel, die mich inspiriert haben, aber weiß, und ich wollte einen dunklen Look für dieses Projekt.

### Synthese

- **Zentrale Erkenntnis:** Garbage in, garbage out. Vorwissen macht einen großen Unterschied – einfache Sachen funktionieren schnell, aber je spezifischer die Anforderungen und je größer die Codebase, desto schwieriger wird es für Laien zu managen.
- **Offene Frage:** Glaubst du, jemand ohne deine Web-Erfahrung hätte ein ähnliches Ergebnis erreichen können?

**Keywords:** #Cursor #KI-Programmierung #WebDevelopment #Workflow #Lernen

<div class="interview-transcript">

<h4>Kontext</h4>

<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Welche Tools hast du verwendet?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Cursor, Version Control via Github, und größtenteils die Modelle von Anthropic.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Was wolltest du erreichen?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Ich wollte sowohl die Website erstellen als auch Cursor ausprobieren, da es sich interessant für mich anhörte und ich bereits Webentwicklungserfahrung habe, aber nur sehr limitiert und es würde sehr lange dauern, wenn ich es ganz alleine mache.</p></div>
</div>

<h4>Die 5 Forschungsfragen</h4>

<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Hat sich dein Arbeitsablauf verändert? <em>(Workflow)</em></p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Oh mein Gott, das war einfach sehr krass! Das hat das Aufsetzen der Website einfach tausendfach schneller gemacht.

Also, hier war der größte Unterschied zu merken, wo ich konnte mein bestehendes Wissen einbringen. Aber musste bei Kleinigkeiten nicht selber googeln und bug fixen, sondern Cursor. Die KI-Modelle haben das für mich erledigt. Ich konnte schnell experimentieren und ich hatte zwar Probleme beim Debugging, aber ich wäre gar nicht so weit gekommen ohne Cursor und Claude. Ich konnte quasi meine kreative Vision umsetzen.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Wie hast du deine Rolle erlebt? <em>(Autorschaft)</em></p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>I felt like a manager with the overall vision asking a junior developer to code for me. At some point, I felt like I was collaborating a bit when it couldn't figure out where it was going wrong. And I was reviewing a lot what I was doing. At the same time, I was learning because when I was doing things I couldn't have done myself, I asked it, or I could see its thinking process too. So I also learned a lot.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Wie hat die schnelle KI-Ausgabe deinen Prozess beeinflusst? <em>(Iteration)</em></p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Die KI-Ausgabe war sofort da. Code, Layouts, Fixes. Das hat meinen Workflow massiv beschleunigt, weil ich nicht mehr googeln und Stack Overflow durchforsten musste. Aber es hat auch dazu geführt, dass ich manchmal zu schnell akzeptiert habe, ohne den Code richtig zu verstehen. Das Tempo verleitet zur Oberflächlichkeit.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Was ist schiefgelaufen? <em>(Scheitern)</em></p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Also, wir kamen ab und zu in Debugging-Schleifen. Das war schon sehr nervig, aber ich habe dann besser gelernt, wie man die KI anleiten kann. Zum Beispiel, dass man öfter den Chat erneuern sollte, damit umso mehr Informationen im Kontext sind, desto schlechter die KI funktioniert. Es wurden auch falsche Ansätze gewählt, welche ich dann ablehnen musste bzw. zurückrudern musste.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Hat sich eine eigene visuelle Sprache entwickelt? <em>(Ästhetik)</em></p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Ja, ein bisschen Kepler-DNA und der Matrix-Look. Ich mag dunkle Websites, und ich hatte mich ja vom Research Catalogue inspirieren lassen. Da waren die Artikel, die mich inspiriert haben, aber weiß, und ich wollte einen dunklen Look für dieses Projekt.</p></div>
</div>

<h4>Synthese</h4>

<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Du hast geschrieben, dass deine bestehende Web-Erfahrung entscheidend war, um KI-Vorschläge einzuschätzen. Glaubst du, jemand ohne diese Erfahrung hätte ein ähnliches Ergebnis erreichen können?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Also ich glaube, es hängt sehr stark von der Person ab. Ich glaube, Leute, die gar keinen Hintergrund haben und auch nicht so viel Geduld, würden schnell an ihre Grenzen kommen. Also, es ist nicht so, dass man einfach alles an die KI geben kann. Garbage in, garbage out. Man muss schon ein bisschen mitlernen, obwohl es schon Ergebnisse gibt, die mit relativ viel wenig Arbeit gut sein können. Ich denke, wenn jemand einfach nur sagt: "Hey, kannst du mir einen Taschenrechner programmieren? Vielleicht in einer bestimmten Farbe, die mir gefällt?" – dann würde das schnell funktionieren, einfach nur weil es so viel vorhandener Code für das Programmieren von Taschenrechnern gibt.

Aber umso spezifischer die Anforderungen werden, umso länger der Chat und umso größer die codebase, desto schwieriger wird es das ganze für einen Laien zu managen.</p></div>
</div>
</div>
