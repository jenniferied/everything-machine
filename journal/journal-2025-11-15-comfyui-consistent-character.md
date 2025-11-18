# Referenzen sammeln und ComfyUI Consistent Character Workflow ausprobieren

**15. November 2025**

Heute habe ich mich zum ersten Mal richtig mit dem ComfyUI Consistent Character Workflow beschäftigt. Das Ziel war klar: Ich wollte herausfinden, ob ich damit konsistente Darstellungen von Kepler über verschiedene Bilder hinweg erzeugen kann, ohne jedes Mal von vorne anfangen zu müssen.

Zuerst habe ich versucht, bestehende Bilder als Referenzen zu verwenden. Das hat teilweise funktioniert, aber es gab einige Probleme, die schnell klar wurden. Wenn ich zum Beispiel ein Bild hochgeladen habe, auf dem Kepler einen Basketball hält, und dann in den Prompts eine Maske hinzugefügt habe, wurde die Maske zwar generiert, aber der Basketball blieb einfach drin. Das Modell hat offenbar nicht verstanden, dass bestimmte Elemente entfernt werden sollten, wenn neue hinzukommen. Ähnlich war es mit Gesichtern – wenn ich ein Bild mit einem bestimmten Gesichtsausdruck als Referenz genommen habe, wurden bei der Generierung manchmal zusätzliche Gesichter eingefügt, als Platzhalter für Ergebnisse, die das System noch nicht richtig interpretieren konnte.

Nach ein paar frustrierenden Versuchen habe ich beschlossen, eine eigene Referenz zu erstellen. Ich habe Kepler auf einem neutralen grauen Hintergrund fotografiert, ohne störende Elemente, ohne Basketball, ohne komplexe Hintergründe. Nur er, klar und deutlich. Dann habe ich die Prompts leicht angepasst, um zu sehen, wie sich das auf die Ergebnisse auswirkt.

![Referenzbild von Kepler auf neutralem Hintergrund](assets/journal/comfyui-consistent-character/reference-kepler.png)

Die Ergebnisse waren gemischt. Einige Bilder sahen wirklich gut aus – der Charakter war konsistent, die Details stimmten, und die Maske wurde korrekt dargestellt. Andere waren weniger überzeugend. Manchmal verlor der Workflow die Konsistenz komplett, besonders bei unterschiedlichen Posen oder wenn ich versucht habe, komplexere Szenen zu generieren. Es scheint, als ob das System am besten funktioniert, wenn die Referenzbilder möglichst klar und unkompliziert sind.

![Generiertes Kepler-Bild 1](assets/journal/comfyui-consistent-character/generated-kepler-001.png)

![Generiertes Kepler-Bild 2](assets/journal/comfyui-consistent-character/generated-kepler-002.png)

![Generiertes Kepler-Bild 3](assets/journal/comfyui-consistent-character/generated-kepler-003.png)

![Generiertes Kepler-Bild 4](assets/journal/comfyui-consistent-character/generated-kepler-004.png)

![Generiertes Kepler-Bild 5](assets/journal/comfyui-consistent-character/generated-kepler-005.png)

![Generiertes Kepler-Bild 6](assets/journal/comfyui-consistent-character/generated-kepler-006.png)

## Die Technologie dahinter

Der ComfyUI Consistent Character Workflow basiert auf mehreren Technologien, die zusammenarbeiten, um konsistente Charakterdarstellungen zu ermöglichen. ComfyUI selbst ist eine grafische Benutzeroberfläche für Stable Diffusion, die es ermöglicht, komplexe Bildgenerierungsprozesse durch modulare Workflows zu steuern. Statt Code zu schreiben, verbindet man Nodes miteinander, die verschiedene Funktionen repräsentieren – von der Bildladung über die Prompt-Verarbeitung bis hin zur finalen Ausgabe.

![ComfyUI Workflow Screenshot 1](assets/journal/comfyui-consistent-character/workflow-screenshot-001.png)

![ComfyUI Workflow Screenshot 2](assets/journal/comfyui-consistent-character/workflow-screenshot-002.png)

Der Consistent Character Workflow nutzt dabei hauptsächlich das Flux-Modell, ein von Black Forest Labs entwickeltes Bildgenerierungsmodell, das besonders gut darin ist, konsistente Darstellungen zu erzeugen. Flux funktioniert ähnlich wie Stable Diffusion, verwendet aber eine andere Architektur, die es ermöglicht, feinere Details und bessere Konsistenz über mehrere Bilder hinweg zu erreichen.

Ein wichtiger Teil des Workflows ist die Verwendung von IP-Adapter oder ähnlichen Technologien, die es ermöglichen, Referenzbilder in den Generierungsprozess einzubinden. Diese Adapter analysieren das Referenzbild und extrahieren bestimmte Merkmale – Gesichtszüge, Kleidung, Stil – und versuchen dann, diese Merkmale in neuen Generierungen beizubehalten. Das funktioniert durch sogenannte Attention-Mechanismen, bei denen das Modell lernt, welche Teile des Referenzbilds wichtig sind und welche ignoriert werden können.

ControlNet ist ein weiteres wichtiges Werkzeug in diesem Workflow. Es ermöglicht es, bestimmte Aspekte der Generierung zu kontrollieren – zum Beispiel die Pose eines Charakters oder die Tiefenstruktur einer Szene. ControlNet funktioniert, indem es zusätzliche Informationen aus einem Kontrollbild extrahiert und diese Informationen dann in den Generierungsprozess einfließen lässt. Wenn ich zum Beispiel ein Bild mit einer bestimmten Pose habe, kann ControlNet diese Pose erkennen und sicherstellen, dass der generierte Charakter in derselben Pose erscheint.

Das Problem, das ich mit dem Basketball hatte, liegt wahrscheinlich daran, dass das System nicht wirklich "versteht", was es generiert. Es erkennt Muster und Merkmale, aber es hat kein semantisches Verständnis davon, dass ein Basketball und eine Maske möglicherweise nicht gleichzeitig vorhanden sein sollten. Das Modell sieht einfach verschiedene visuelle Elemente und versucht, sie zu kombinieren, ohne die logischen Zusammenhänge zu berücksichtigen.

Face Detailer ist ein zusätzliches Tool, das speziell darauf ausgelegt ist, Gesichter zu verbessern. Es funktioniert, indem es das generierte Bild analysiert, Gesichter erkennt und dann diese Bereiche mit einem speziell trainierten Modell nachbearbeitet. Das kann helfen, Details zu schärfen und realistischere Gesichtszüge zu erzeugen, aber es kann auch zu Problemen führen, wenn das System Gesichter erkennt, wo keine sein sollten, oder wenn es versucht, Gesichter zu "reparieren", die eigentlich korrekt waren.

Der gesamte Workflow ist im Grunde eine Kette von Transformationen. Zuerst wird das Referenzbild analysiert und seine Merkmale werden extrahiert. Dann wird ein Text-Prompt verarbeitet, der beschreibt, was generiert werden soll. Diese Informationen werden kombiniert und durch das Flux-Modell geleitet, das Schritt für Schritt ein neues Bild generiert. ControlNet kann dabei zusätzliche Kontrolle bieten, und Face Detailer kann am Ende noch einmal über die Gesichter gehen, um sie zu verbessern.

Das Problem ist, dass jeder dieser Schritte Fehler einführen kann. Wenn die Referenz nicht klar genug ist, werden die extrahierten Merkmale ungenau. Wenn der Prompt zu komplex ist, kann das Modell verschiedene Interpretationen haben. Und wenn ControlNet oder Face Detailer falsch interpretieren, was sie sehen sollen, entstehen Artefakte wie zusätzliche Gesichter oder nicht entfernte Objekte.

Die Lösung, die ich gefunden habe – eine klare Referenz auf neutralem Hintergrund – funktioniert, weil sie dem System weniger Raum für Fehlinterpretationen lässt. Wenn nur der Charakter zu sehen ist, ohne störende Elemente, kann das Modell sich auf die wichtigen Merkmale konzentrieren. Aber selbst dann ist die Konsistenz nicht garantiert, besonders wenn man versucht, den Charakter in verschiedenen Posen oder Kontexten zu zeigen.

