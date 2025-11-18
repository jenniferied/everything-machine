# Marble von Worldlabs ausprobieren

**18. November 2025**

Heute habe ich Marble von Worldlabs getestet, ein neues Tool, das unter marble.worldlabs.ai verfügbar ist. Ich hatte davon gehört, dass es sich um ein Tool zur Erstellung von 3D-Welten handelt, und war neugierig, wie es sich von anderen Tools unterscheidet, die ich bisher verwendet habe.

Marble ist im Grunde eine browserbasierte Plattform, die es ermöglicht, interaktive 3D-Welten zu erstellen und zu erkunden. Das Besondere daran ist, dass man keine komplexe Software installieren muss – alles läuft im Browser, was den Einstieg deutlich erleichtert. Die Oberfläche ist relativ intuitiv gestaltet, auch wenn es am Anfang etwas dauert, bis man sich zurechtfindet.

Ich habe drei verschiedene Welten erstellt, um zu sehen, wie flexibel das Tool ist und welche Möglichkeiten es bietet.

Die erste Welt war eine futuristische Stadt. Ich wollte etwas schaffen, das an die Ästhetik von Kepler erinnert – urban, digital, etwas melancholisch. Die Erstellung war überraschend einfach. Marble bietet verschiedene vorgefertigte Assets, die man einfach in die Szene ziehen kann, und man kann sie dann anpassen – Größe, Position, Rotation. Die Beleuchtung lässt sich ebenfalls relativ einfach steuern, was wichtig ist, um die richtige Stimmung zu erzeugen. Was mich überrascht hat, war die Qualität der Echtzeit-Vorschau. Man sieht sofort, wie die Welt aussehen wird, ohne lange Rendering-Zeiten warten zu müssen.

Die zweite Welt war ein Märchenwald – komplett anders, um zu testen, ob das Tool auch für verschiedene Stile geeignet ist. Hier habe ich gemerkt, dass Marble ziemlich flexibel ist. Die Assets sind vielfältig, und man kann verschiedene Texturen und Materialien anwenden. Die Herausforderung war, eine kohärente Atmosphäre zu schaffen, die nicht zu chaotisch wirkt. Ich habe verschiedene Bäume, Pflanzen und Lichtquellen platziert, und das System hat die Beleuchtung automatisch angepasst, was sehr hilfreich war.

Die dritte Welt war eine Unterwasserwelt. Das war interessant, weil ich sehen wollte, wie Marble mit Partikelsystemen und speziellen Effekten umgeht. Wasser ist immer eine Herausforderung in 3D-Programmen, und Marble bietet einige vorgefertigte Wasser-Effekte, die ganz gut funktionieren. Die Partikelsysteme für Blasen und andere Unterwasser-Effekte waren ebenfalls vorhanden, auch wenn sie nicht so detailliert anpassbar sind wie in professionellen 3D-Programmen.

Meine Gedanken dazu: Marble ist definitiv ein interessantes Tool, besonders für schnelle Prototypen und Experimente. Die Browser-Basis macht es zugänglich, und die Echtzeit-Vorschau ist ein großer Vorteil. Allerdings merkt man auch die Grenzen – die Assets sind begrenzt, und die Anpassungsmöglichkeiten sind nicht so tiefgreifend wie bei professionellen Tools wie Blender oder Unreal Engine. Für das, was ich mit Kepler mache, könnte es nützlich sein, um schnell Ideen zu visualisieren oder um Hintergründe zu erstellen, die dann in anderen Programmen weiterverarbeitet werden können.

## Die Technologie dahinter

Marble basiert auf einer Kombination verschiedener Web-Technologien, die es ermöglichen, komplexe 3D-Grafiken direkt im Browser zu rendern. Der Kern der Technologie ist WebGL, eine JavaScript-API, die es ermöglicht, Hardware-beschleunigte 3D-Grafiken zu rendern, ohne dass Plugins wie Flash benötigt werden. WebGL ist im Grunde eine Browser-Version von OpenGL, der weit verbreiteten Grafik-API, die auch in vielen Desktop-Anwendungen verwendet wird.

Über WebGL hinaus nutzt Marble wahrscheinlich auch WebGPU, eine neuere Technologie, die noch bessere Performance bietet. WebGPU ist der Nachfolger von WebGL und ermöglicht es, die volle Leistung der Grafikkarte zu nutzen, ähnlich wie DirectX oder Vulkan auf Desktop-Systemen. Das ist wichtig, weil 3D-Rendering sehr rechenintensiv ist, und ohne Hardware-Beschleunigung wäre es praktisch unmöglich, komplexe Szenen in Echtzeit zu rendern.

Die 3D-Engine, die Marble verwendet, ist wahrscheinlich eine angepasste Version einer bestehenden Engine wie Three.js oder Babylon.js, oder eine proprietäre Entwicklung. Diese Engines abstrahieren die Komplexität von WebGL und bieten höhere Funktionen – zum Beispiel für das Laden von 3D-Modellen, das Anwenden von Texturen, das Berechnen von Beleuchtung und Schatten, und das Rendern von Partikelsystemen.

Physikbasiertes Rendering, oder PBR, ist ein wichtiger Teil der Technologie. PBR ist ein Rendering-Ansatz, der versucht, die Art und Weise zu simulieren, wie Licht mit Materialien interagiert, basierend auf physikalischen Gesetzen. Statt einfach Farben und Texturen anzuwenden, berücksichtigt PBR verschiedene Materialeigenschaften – wie rau oder glatt eine Oberfläche ist, wie metallisch sie ist, wie sie Licht reflektiert oder absorbiert. Das führt zu realistischeren Ergebnissen, besonders bei verschiedenen Beleuchtungssituationen.

Prozedurale Generierung ist ein weiterer wichtiger Aspekt. Statt jedes Detail manuell zu platzieren, kann das System bestimmte Elemente automatisch generieren – zum Beispiel Bäume in einem Wald, die alle leicht unterschiedlich aussehen, oder Steine auf einem Boden, die zufällig verteilt sind. Das funktioniert durch Algorithmen, die basierend auf Parametern und Zufallszahlen verschiedene Variationen erzeugen. Das macht es möglich, große, detaillierte Welten zu erstellen, ohne jedes einzelne Element manuell platzieren zu müssen.

Die Echtzeit-Vorschau, die Marble bietet, ist möglich durch optimiertes Rendering. Das System rendert nicht jedes Detail in voller Qualität, sondern verwendet verschiedene Techniken, um die Performance zu optimieren – zum Beispiel Level-of-Detail-Systeme, bei denen Objekte, die weiter weg sind, mit weniger Details gerendert werden, oder Frustum Culling, bei dem Objekte, die außerhalb des Sichtfelds sind, gar nicht erst gerendert werden.

Die Interaktivität – also die Möglichkeit, durch die Welten zu navigieren und sie zu erkunden – wird durch Eingabe-Handler ermöglicht, die Maus- und Tastatur-Eingaben in Bewegungen und Aktionen umwandeln. Die Kamera wird in Echtzeit aktualisiert, basierend auf den Eingaben des Benutzers, und die Szene wird entsprechend neu gerendert.

Ein interessanter Aspekt ist, dass Marble wahrscheinlich auch KI-gestützte Funktionen verwendet, zum Beispiel für das automatische Platzieren von Objekten oder für Design-Vorschläge. Das könnte durch Machine-Learning-Modelle funktionieren, die auf dem Server laufen und dann die Ergebnisse an den Browser senden, oder durch kleinere Modelle, die direkt im Browser ausgeführt werden, was durch WebAssembly möglich ist.

Die Browser-Basis von Marble bringt sowohl Vorteile als auch Herausforderungen mit sich. Der Vorteil ist die Zugänglichkeit – man braucht keine Installation, und es funktioniert auf verschiedenen Plattformen. Die Herausforderung ist, dass Browser-Umgebungen weniger Ressourcen haben als native Anwendungen, und dass die Kompatibilität zwischen verschiedenen Browsern manchmal problematisch sein kann. Aber moderne Browser und Web-Technologien haben diese Lücke in den letzten Jahren deutlich verkleinert.

