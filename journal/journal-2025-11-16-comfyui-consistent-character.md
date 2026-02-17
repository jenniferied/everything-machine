# ComfyUI Consistent Character Workflow ausprobieren

**16. November 2025**

Heute habe ich mich zum ersten Mal richtig mit dem ComfyUI Consistent Character Workflow beschäftigt. Das Ziel war klar: Ich wollte herausfinden, ob ich damit konsistente Darstellungen von Kepler über verschiedene Bilder hinweg erzeugen kann, ohne jedes Mal von vorne anfangen zu müssen.

Zuerst habe ich versucht, bestehende Bilder als Referenzen zu verwenden. Das hat teilweise funktioniert, aber es gab einige Probleme, die schnell klar wurden. Wenn ich zum Beispiel ein Bild hochgeladen habe, auf dem Kepler einen Basketball hält, und dann in den Prompts eine Maske hinzugefügt habe, wurde die Maske zwar generiert, aber der Basketball blieb einfach drin. Das Modell hat offenbar nicht verstanden, dass bestimmte Elemente entfernt werden sollten, wenn neue hinzukommen. Ähnlich war es mit Gesichtern – wenn ich ein Bild mit einem bestimmten Gesichtsausdruck als Referenz genommen habe, wurden bei der Generierung manchmal zusätzliche Gesichter eingefügt, als Platzhalter für Ergebnisse, die das System noch nicht richtig interpretieren konnte.

Nach ein paar frustrierenden Versuchen habe ich beschlossen, eine eigene Referenz zu erstellen. Ich habe Kepler auf einem neutralen grauen Hintergrund fotografiert, ohne störende Elemente, ohne Basketball, ohne komplexe Hintergründe. Nur er, klar und deutlich. Dann habe ich die Prompts leicht angepasst, um zu sehen, wie sich das auf die Ergebnisse auswirkt.

![Referenzbild von Kepler auf neutralem Hintergrund](assets/journal/2025-11-16-comfyui-consistent-character/reference-kepler.png)

Die Ergebnisse waren gemischt. Einige Bilder sahen wirklich gut aus – der Charakter war konsistent, die Details stimmten, und die Maske wurde korrekt dargestellt. Andere waren weniger überzeugend. Manchmal verlor der Workflow die Konsistenz komplett, besonders bei unterschiedlichen Posen oder wenn ich versucht habe, komplexere Szenen zu generieren. Es scheint, als ob das System am besten funktioniert, wenn die Referenzbilder möglichst klar und unkompliziert sind.

![Generiertes Kepler-Bild 1](assets/journal/2025-11-16-comfyui-consistent-character/generated-kepler-001.png)

![Generiertes Kepler-Bild 2](assets/journal/2025-11-16-comfyui-consistent-character/generated-kepler-002.png)

![Generiertes Kepler-Bild 3](assets/journal/2025-11-16-comfyui-consistent-character/generated-kepler-003.png)

![Generiertes Kepler-Bild 4](assets/journal/2025-11-16-comfyui-consistent-character/generated-kepler-004.png)

![Generiertes Kepler-Bild 5](assets/journal/2025-11-16-comfyui-consistent-character/generated-kepler-005.png)

![Generiertes Kepler-Bild 6](assets/journal/2025-11-16-comfyui-consistent-character/generated-kepler-006.png)

## ComfyUI und Flux

Der ComfyUI Consistent Character Workflow basiert auf mehreren Technologien, die zusammenarbeiten, um konsistente Charakterdarstellungen zu ermöglichen. ComfyUI selbst ist eine grafische Benutzeroberfläche für Stable Diffusion, die es ermöglicht, komplexe Bildgenerierungsprozesse durch modulare Workflows zu steuern. Statt Code zu schreiben, verbindet man Nodes miteinander, die verschiedene Funktionen repräsentieren – von der Bildladung über die Prompt-Verarbeitung bis hin zur finalen Ausgabe.

![ComfyUI Workflow Screenshot 1](assets/journal/2025-11-16-comfyui-consistent-character/workflow-screenshot-001.png)

![ComfyUI Workflow Screenshot 2](assets/journal/2025-11-16-comfyui-consistent-character/workflow-screenshot-002.png)

Der Consistent Character Workflow nutzt dabei hauptsächlich das Flux-Modell, ein von Black Forest Labs entwickeltes Bildgenerierungsmodell, das besonders gut darin ist, konsistente Darstellungen zu erzeugen. Flux funktioniert ähnlich wie Stable Diffusion, verwendet aber eine andere Architektur, die es ermöglicht, feinere Details und bessere Konsistenz über mehrere Bilder hinweg zu erreichen.

## IP-Adapter und ControlNet

Ein wichtiger Teil des Workflows ist die Verwendung von IP-Adapter oder ähnlichen Technologien, die es ermöglichen, Referenzbilder in den Generierungsprozess einzubinden. Diese Adapter analysieren das Referenzbild und extrahieren bestimmte Merkmale – Gesichtszüge, Kleidung, Stil – und versuchen dann, diese Merkmale in neuen Generierungen beizubehalten. Das funktioniert durch sogenannte Attention-Mechanismen, bei denen das Modell lernt, welche Teile des Referenzbilds wichtig sind und welche ignoriert werden können.

ControlNet ist ein weiteres wichtiges Werkzeug in diesem Workflow. Es ermöglicht es, bestimmte Aspekte der Generierung zu kontrollieren – zum Beispiel die Pose eines Charakters oder die Tiefenstruktur einer Szene. ControlNet funktioniert, indem es zusätzliche Informationen aus einem Kontrollbild extrahiert und diese Informationen dann in den Generierungsprozess einfließen lässt. Wenn ich zum Beispiel ein Bild mit einer bestimmten Pose habe, kann ControlNet diese Pose erkennen und sicherstellen, dass der generierte Charakter in derselben Pose erscheint.

Das Problem, das ich mit dem Basketball hatte, liegt wahrscheinlich daran, dass das System nicht wirklich "versteht", was es generiert. Es erkennt Muster und Merkmale, aber es hat kein semantisches Verständnis davon, dass ein Basketball und eine Maske möglicherweise nicht gleichzeitig vorhanden sein sollten. Das Modell sieht einfach verschiedene visuelle Elemente und versucht, sie zu kombinieren, ohne die logischen Zusammenhänge zu berücksichtigen.

## Face Detailer — und das Problem

Face Detailer ist ein zusätzliches Tool, das speziell darauf ausgelegt ist, Gesichter zu verbessern. Es funktioniert, indem es das generierte Bild analysiert, Gesichter erkennt und dann diese Bereiche mit einem speziell trainierten Modell nachbearbeitet. Das kann helfen, Details zu schärfen und realistischere Gesichtszüge zu erzeugen, aber es kann auch zu Problemen führen, wenn das System Gesichter erkennt, wo keine sein sollten, oder wenn es versucht, Gesichter zu "reparieren", die eigentlich korrekt waren.

Der gesamte Workflow ist im Grunde eine Kette von Transformationen. Zuerst wird das Referenzbild analysiert und seine Merkmale werden extrahiert. Dann wird ein Text-Prompt verarbeitet, der beschreibt, was generiert werden soll. Diese Informationen werden kombiniert und durch das Flux-Modell geleitet, das Schritt für Schritt ein neues Bild generiert. ControlNet kann dabei zusätzliche Kontrolle bieten, und Face Detailer kann am Ende noch einmal über die Gesichter gehen, um sie zu verbessern.

Das Problem ist, dass jeder dieser Schritte Fehler einführen kann. Wenn die Referenz nicht klar genug ist, werden die extrahierten Merkmale ungenau. Wenn der Prompt zu komplex ist, kann das Modell verschiedene Interpretationen haben. Und wenn ControlNet oder Face Detailer falsch interpretieren, was sie sehen sollen, entstehen Artefakte wie zusätzliche Gesichter oder nicht entfernte Objekte.

Die Lösung, die ich gefunden habe – eine klare Referenz auf neutralem Hintergrund – funktioniert, weil sie dem System weniger Raum für Fehlinterpretationen lässt. Wenn nur der Charakter zu sehen ist, ohne störende Elemente, kann das Modell sich auf die wichtigen Merkmale konzentrieren. Aber selbst dann ist die Konsistenz nicht garantiert, besonders wenn man versucht, den Charakter in verschiedenen Posen oder Kontexten zu zeigen.

---

## Reflexion

- **Tools:** ComfyUI lokal, M1 MacBook — aufwendige Installation
- **Scheitern:** Gesichter in Keplers Maske halluziniert, negative Prompts helfen nicht
- **Erkenntnis:** keine magischen Tools — Art Directability fehlt noch
- **Ästhetik:** generisch KI-mäßig, nicht weit gekommen
- **Offene Frage:** eigenes Modell trainieren oder anderen Workflow?

### Kontext

- **Tools:** ComfyUI mit einem Network von Mickmumpitz (lokal auf M1 MacBook Pro Max 64 GB)
- **Intention:** Album-Cover und Konzeptbilder für Kepler erstellen, Konsistenz erreichen, ComfyUI als Plattform lernen

### Die 5 Forschungsfragen

- **Workflow:** Komplett neuer Workflow mit ComfyUI. Muss wiederkommen, um es besser zu verstehen – vielleicht nicht mit Kepler als Charakter. Er ist besonders schwierig: kein Mensch per se, Maske statt Gesicht, voxelisiert.
- **Autorschaft:** Lernende und Experimentierende – ich habe mich an dem Netzwerk einer anderen Person orientiert.
- **Iteration:** Gar nicht so schnell – lokale Installation auf M1 MacBook, langer Installationsprozess, viele Gigabyte. Frustrierend.
- **Scheitern:** Sehr inkonsistente Ergebnisse. Der Basketball wurde nicht entfernt. Besonders frustrierend: Gesichter wurden in Keplers Maske interpretiert, auch mit negativen Prompts.
- **Ästhetik:** Nicht so weit gekommen – die Ergebnisse sahen generisch KI-mäßig aus.

### Synthese

- **Zentrale Erkenntnis:** Es ist frustrierend, aber am Ende ein technisches Problem. Die Art Directability ist noch nicht da. Es sind keine magischen Tools – für viele fühlt es sich beim ersten Mal mit ChatGPT so an, aber es sind einfach Werkzeuge, die mehr oder weniger gut für den Anwendungsfall funktionieren. Mit einer realistischen, Anime- oder Cartoon-Figur hätte es besser funktioniert. Aber Kepler hat kein sichtbares Gesicht, und die Trainingsdaten enthalten Gesichter – deswegen bleiben sie hartnäckig dort.
- **Offene Frage:** Muss ich ein eigenes Modell trainieren? Oder gibt es einen Workflow, der mit maskierten Charakteren besser umgeht?

**Keywords:** #ComfyUI #Flux #Konsistenz #Frustration #Kepler #ArtDirectability

<div class="interview-transcript">

<h4>Kontext</h4>

<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Welche Tools hast du in dieser Session verwendet?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>ComfyUI mit einem Network von Mickmumpitz (Füge einen Link zu seinem YT Channel hinzu).</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Was wolltest du erreichen?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Ich wollte schauen, ob ich Album-Cover- oder Konzeptbilder erstellen konnte von Kepler. Mir war aber wichtig, dass eine Konsistenz besteht und es ästhetisch aussieht. Ich war auch etwas von dem ComfyUI Workflow und dem Konzept überfordert, deswegen wollte ich das als Plattform nutzen, um das Ganze zu lernen.</p></div>
</div>

<h4>Die 5 Forschungsfragen</h4>

<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Hat sich dein Arbeitsablauf verändert? (Workflow)</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Es ist ein komplett neuer Workflow mit ComfyUI zu arbeiten. Ich glaube, ich muss wiederkehren, um das Ganze besser zu verstehen, und vielleicht nicht mit Kepler als Charakter. Denn ich habe gleich gesehen, dass er besonders schwierig ist. Er ist jetzt kein Mensch per se, und sein Stil könnte schwierig zu replizieren sein, da er kein Gesicht hat, eine Maske trägt und in der Version, in der ich sie ihnen zeigen möchte, auch noch voxelized ist.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Wie hast du deine Rolle erlebt? (Autorschaft)</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Ich war Lernende und experimentierte eher als ich das Tool wirklich verwendete. Ich hatte mich ja an dem Netzwerk einer anderen Person orientiert.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Wie hat die schnelle KI-Ausgabe deinen Prozess beeinflusst? (Iteration)</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Es war gar nicht so schnell, da ich es tatsächlich lokal auf meinem M1-MacBook Pro Max 64 GB ausprobiert habe. Auch der Prozess, das Ganze zu installieren, hat länger gedauert und hat viele Gigabyte benötigt. Also war es etwas frustrierend.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Was ist schiefgelaufen? (Scheitern)</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Es war sehr inkonsistent. Die Prompts haben nicht das erfüllt, was sie erfüllen sollten. Der Basketball wurde nicht entfernt, als ich ein Bild mit Basketball eingefügt habe. Besonders frustrierend war, dass Gesichter in Keplers Maske rein interpretiert worden sind. Auch als ich negative Prompts dafür eingefügt habe. Ich glaube, das wird ein größeres Problem.</p></div>
</div>
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Hat sich eine eigene visuelle Sprache entwickelt? (Ästhetik)</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Nein, denn so weit bin ich gar nicht erst gekommen in diesem Anlauf. Denn es haben Sachen ja auch nicht funktioniert, und das, was herauskam, sah schon sehr generisch KI-mäßig aus.</p></div>
</div>

<h4>Synthese</h4>

<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Du hast erwähnt, dass das System Gesichter in Keplers Maske interpretiert hat – obwohl er bewusst kein Gesicht haben soll. Wie fühlt es sich an, wenn die KI deine künstlerische Intention so grundlegend 'missversteht'?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>Es ist einfach frustrierend. Am Ende des Tages ist es ein technisches Problem.</p>
<p>Ich wollte ja genau durch die Verwendung von KI neue Möglichkeiten schaffen, die intuitiv sind und Spaß machen und auch Zeit einsparen, um Dinge zu kreieren, ohne jetzt mir ganz die Arbeit abzunehmen.</p>
<p>Aber es zeigt halt, dass wir noch nicht ganz da sind und die Art Directability noch nicht da ist. Und das würde ich mir eben wünschen. Aber es sind halt keine magischen Tools, so wie es sich anfühlt.</p>
<p>Für viele, wenn sie das erste Mal ChatGPT benutzen, sind es einfach nur Werkzeuge, die mehr oder weniger gut für den Anwendungsfall funktionieren. Es hätte zufällig gut funktionieren können. Es würde viel besser funktionieren, wenn es sich um eine realistische, oder Anime-style, oder Cartoon-style Figur handeln würde. Aber dem ist nicht so. Kepler hat eben kein sichtbares Gesicht, aber viele der Trainingsdaten enthalten Gesichter und deswegen bleiben sie hartnäckig dort.</p></div>
</div>
</div>
