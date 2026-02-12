---
title: "EVERYTHING MACHINE"
subtitle: "Ein explorativer Artistic Research-Prozess zur Erweiterung des digitalen Alter Egos 'Kepler' mittels multimodaler KI-Inputs"
author: "Jennifer Meier"
date: "Februar 2026"
institute: "Technische Hochschule Ostwestfalen-Lippe"
department: "Fachbereich Medienproduktion, Master Medienproduktion"
course: "Artistic Research"
instructor: "Prof. Dr. Aristotelis Hadjakos"
lang: de-DE
bibliography: references/bibliography.bib
toc: true
abstract: |
  Die vorliegende Arbeit untersucht im Rahmen einer Practice-Based Research mit
  autoethnografischem Ansatz, wie der Einsatz multimodaler KI-Systeme den kreativen
  Prozess bei der Entwicklung einer digitalen Künstleridentität verändert. Am Beispiel
  von Kepler -- einer maskierten, voxelisierten Musiker-Persona -- dokumentiert die
  Autorin [N] Experimente mit KI-Tools aus den Bereichen Bildgenerierung,
  Musikproduktion, Webentwicklung und Texterstellung. Die Analyse identifiziert vier
  zentrale Prozessveränderungen: (1) Flow entsteht unvorhersehbar -- der Website-Build
  mit KI gelang produktiv, während die Bildgenerierung für Kepler an der
  Nischen-Ästhetik scheiterte; (2) KI beschleunigt und begrenzt gleichzeitig --
  Exploration und Prototyping werden schneller, aber die Kontrolle über ästhetische
  Details geht verloren; (3) die Autorschaft verschiebt sich fundamental -- von der
  Ausführenden zur Kuratorin, Dirigentin, Lernenden; (4) der emotionale Zyklus
  zwischen KI-Enthusiasmus und KI-Burnout erweist sich als reale Belastung im
  kreativen Prozess -- der ständige Zwang, neue Tools zu evaluieren und mit
  Limitierungen zu kämpfen, kostet kreative Energie. Die Arbeit zeigt, dass die
  Veränderungen des kreativen Prozesses durch KI nicht linear und nicht planbar sind,
  sondern im iterativen Arbeiten emergent entstehen. Damit leistet sie einen Beitrag
  zur Artistic-Research-Diskussion um Kreativität, Autorschaft und implizites Wissen
  im Kontext generativer KI-Systeme.

  **Keywords:** Artistic Research, generative KI, Mensch-KI-Kollaboration, digitale Identität, Autoethnografie, kreativer Prozess, Practice-Based Research
---

# Einleitung

## Hintergrund und Motivation

### Artistic Research

Die vorliegende Arbeit versteht Artistic Research primär im Sinne von Henk Borgdorffs [-@borgdorff2012conflict, S. 179--181] Definition als künstlerische Praxis, die sich als Forschung qualifiziert, wenn ihr Zweck darin besteht, Wissen und Verständnis durch originäre Untersuchungen in und durch Kunstobjekte und kreative Prozesse zu erweitern. Dabei adressiert Artistic Research Fragen, die sowohl für den Forschungskontext als auch für die Kunstwelt relevant sind, und verwendet experimentelle sowie hermeneutische Methoden, um implizites Wissen in Kunstwerken und künstlerischen Prozessen offenzulegen. Wesentliche Komponenten umfassen die Intention zur Wissenserweiterung über die persönliche künstlerische Entwicklung hinaus, Originalität sowie verschiedene Wissensformen einschließlich propositionalem Wissen, Fertigkeitswissen und implizitem Wissen [@borgdorff2012conflict].

Diese Arbeit positioniert sich im Bereich der praxisbasierten Forschung (practice-based research), bei der das Machen, Kreieren und Performen sowie die resultierenden Kunstwerke eine konstitutive methodologische Rolle spielen [@borgdorff2012conflict; @candy2006practice]. Konkret werden kleine KI-Experimente anhand eines realen Projekts durchgeführt: der Entwicklung visueller Inhalte wie Albumcover und kurzer Reels für ein musikalisches Alter Ego namens Kepler. Die Forschungsergebnisse werden auf einer Website mit Journaleinträgen dokumentiert und der Forschungsgemeinschaft sowie der Öffentlichkeit zugänglich gemacht.

### Der Moment der generativen KI

Wir erleben einen historischen Umbruch in der kreativen Produktion. Zwischen 2022 und 2025 hat sich eine Expansion generativer KI-Tools ereignet, die nahezu alle kreativen Domänen erfasst: DALL-E, Midjourney und Stable Diffusion für Bilder; ChatGPT und Claude für Text; Suno und Udio für Musik; Runway und Sora für Video. Was vor wenigen Jahren noch Gegenstand von Science-Fiction-Spekulationen war, ist heute alltägliches Werkzeug.

Diese Entwicklung demokratisiert kreative Produktion auf beispiellose Weise. Eine einzelne Person kann nun Visuals, Texte, Musik und Videos in einer Qualität erstellen, die früher ganze Teams erforderte. Gleichzeitig wirft diese Demokratisierung fundamentale Fragen auf: Was bedeutet Autorschaft, wenn Maschinen mitschreiben? Was ist Kreativität, wenn Algorithmen Bilder generieren? Was ist ästhetischer Wert, wenn "alles" auf Knopfdruck möglich scheint?

Diese Fragen sind nicht abstrakt-philosophisch, sondern berühren die konkrete Praxis von Medienproduzent\*innen, Künstler\*innen und Kreativen weltweit.

### Kepler: Ein digitales Alter Ego

Im Kontext meiner eigenen künstlerischen Praxis manifestiert sich diese Transformation in der Entwicklung von "Kepler" -- einem digitalen Alter Ego, das als Musiker und visueller Künstler existiert. Kepler ist keine rein fiktive Figur, die ich erfunden habe, sondern ein emergentes Ergebnis meiner Zusammenarbeit mit KI-Systemen: Seine visuelle Erscheinung entsteht durch Diffusion Models, seine Texte durch Kollaboration mit LLMs, seine Musik durch KI-gestützte Produktion.

Das Projekt begann mit einer einfachen Frage: Was passiert, wenn ich nicht mehr nur Werkzeuge benutze, sondern mit ihnen zusammenarbeite? Die Antwort hat mich überrascht: Kepler entwickelte eine Eigenlogik, die ich nicht vollständig geplant hatte. Er wurde mehr als eine Figur -- er wurde ein Spiegel meiner Auseinandersetzung mit dieser neuen kreativen Landschaft.

### "Everything Machine": Der Projektname

Das Projekt "Everything Machine" dokumentiert diesen Entwicklungsprozess transparent auf einer öffentlichen Website. Der Name verweist auf die Idee einer Maschine, die "alles" produzieren kann -- Text, Bild, Audio, Video, Code. Gleichzeitig fragt er kritisch, was dieses "alles" wert ist. Wenn eine Maschine alles kann, was bedeutet das für die Dinge, die wir wertschätzen?

Der Name enthält auch eine Ironie: Je mehr ich mit generativer KI arbeite, desto deutlicher wird, dass sie eben nicht "alles" kann. Sie kann keine echten Erfahrungen machen, keine authentischen Emotionen empfinden, keine wirklichen Beziehungen aufbauen. Die "Everything Machine" ist zugleich mächtig und begrenzt -- und genau diese Spannung macht sie zum Gegenstand künstlerischer Forschung.

## Forschungsfrage und Überblick

Die zentrale Forschungsfrage lautet:

> **Wie verändert der Einsatz multimodaler KI-Systeme (Text, Bild, Audio) den kreativen Prozess bei der Entwicklung einer digitalen Künstleridentität?**

Im Laufe der Praxis verschob sich der Fokus zeitweise in Richtung einer Ästhetik-Frage -- selbst ein Ergebnis des iterativen Forschungsprozesses. Die vorliegende Arbeit kehrt zur Prozessfrage zurück, weil die Praxis zeigte, dass die Veränderung des kreativen Prozesses die eigentliche Erkenntnis ist.

Zur Beantwortung dieser Frage verbindet die Arbeit:

1. **Praktische Experimente:** Iterative Entwicklung von Kepler durch verschiedene KI-Tools, beobachtet auf Prozessveränderungen
2. **Theoretische Reflexion:** Einordnung in Diskurse zu Kreativität, Autorschaft und Human-AI Interaction
3. **Methodische Transparenz:** Öffentliche Dokumentation des gesamten Prozesses

Die Arbeit gliedert sich in fünf Abschnitte: Nach der Einleitung folgt eine Darstellung des Forschungsstands (Abschnitt 2), dann die methodische Beschreibung (Abschnitt 3), die Darstellung meiner Forschung (Abschnitt 4) und schließlich die Diskussion (Abschnitt 5).

# Stand der Forschung

## Artistic Research als Erkenntnisform

Die theoretische Grundlage für dieses Projekt bildet das Feld des Artistic Research, wie es von Autor\*innen wie Borgdorff [-@borgdorff2012conflict] und Candy [-@candy2006practice] konzeptualisiert wird. Artistic Research positioniert künstlerische Praxis nicht als Illustration wissenschaftlicher Erkenntnisse, sondern als eigenständige Erkenntnisform.

Candy unterscheidet zwischen "practice-based" und "practice-led" Research. Im vorliegenden Projekt ist die Praxis nicht nur Forschungsinstrument, sondern konstituiert den Forschungsgegenstand selbst: Die Entwicklung von Kepler *ist* die Forschung.

## Kreativität und künstliche Intelligenz

Margaret Bodens [-@boden2004creative] Unterscheidung zwischen explorativer, kombinatorischer und transformativer Kreativität bietet einen Rahmen für die Analyse von KI-generierter Kunst. Generative KI-Systeme operieren primär im Modus der explorativen und kombinatorischen Kreativität: Sie erkunden einen "conceptual space" und kombinieren erlernte Muster auf neue Weise.

Die Frage, ob diese Systeme zu "echter" Kreativität fähig sind, bleibt umstritten. Für das vorliegende Projekt ist diese Frage jedoch weniger relevant als die praktische Beobachtung: In der Kollaboration entstehen Ergebnisse, die weder ich allein noch das KI-System allein hervorgebracht hätte.

## Herausforderungen KI-generierter Medien

Zwei bekannte Phänomene treten beim praktischen Arbeiten mit generativer KI wiederholt auf:

**Uncanny Valley** [@mori2012uncanny]: KI-generierte Darstellungen von Menschen lösen häufig Unbehagen aus, weil sie menschenähnlich, aber nicht perfekt realistisch sind. In der Praxis zeigt sich das als konkretes Hindernis -- etwa wenn Bildmodelle Gesichtszüge in Keplers Maske halluzinieren, weil das Modell die Abwesenheit eines Gesichts nicht akzeptiert.

**Suspension of Disbelief** [@coleridge1817biographia]: Die Bereitschaft des Publikums, sich auf eine fiktionale Welt einzulassen, wird durch solche Artefakte immer wieder gestört. Für Kepler als virtuelle Persona stellt sich die Frage, ob Rezipient\*innen ihn als "authentischen" Künstler akzeptieren -- eine Frage, die im kreativen Prozess ständig mitverhandelt wird.

## Forschungslücke

Während es zunehmend Literatur zu generativer KI in der Kunst gibt, fehlen autoethnografische Tiefenstudien, die den iterativen Entstehungsprozess hybrider Kunstwerke aus der Perspektive der beteiligten Künstler\*innen dokumentieren. Diese Arbeit adressiert diese Lücke.

# Methodologie

## Methodischer Rahmen: Practice-Based Research

Das Projekt folgt dem Paradigma des Practice-Based Research, bei dem die künstlerische Praxis selbst die primäre Forschungsmethode darstellt. Die Entwicklung von Kepler ist nicht Gegenstand einer externen Untersuchung, sondern der Ort, an dem Forschung stattfindet.

## Konkrete Methoden

### Autoethnografisches Journaling

Regelmäßige Journal-Einträge dokumentieren den kreativen Prozess nach einer strukturierten Vorlage:

- **Intention:** Zielsetzung der Session
- **Prozess:** Konkrete Aktionen, Prompts, Iterationen
- **Ergebnis:** Output und erste Bewertung
- **Reflexion:** Erkenntnisse, Überraschungen, Anpassungen
- **Nächste Schritte:** Konsequenzen für den weiteren Prozess

### Iterative Experimentierung

Systematische Experimente mit verschiedenen KI-Tools (Stable Diffusion, DALL-E, ChatGPT, Claude, Suno, Udio) folgen einem Zyklus von Hypothese, Experiment, Dokumentation und Anpassung.

### Öffentliche Website als Forschungsartefakt

Die Website "Everything Machine" macht den gesamten Prozess transparent zugänglich. Sie ist selbst Teil des künstlerischen Outputs und dient gleichzeitig als Forschungsdokumentation. Die Website wurde bewusst ohne externes Content-Management-System entwickelt -- stattdessen als maßgeschneiderte Webanwendung mit modernem JavaScript (ES6 Module, EventBus-Pattern für lose Kopplung der Komponenten).

Die technische Architektur der Website reflektiert die methodischen Prinzipien des Projekts: Transparenz durch Versionierung (Git), Iterativität durch modularen Aufbau und Selbstreflexion durch ein integriertes Journal-System.

### KI-gestützter Reflexionsprozess

Ein zentrales Element der Methodik ist der strukturierte Reflexionsprozess, der selbst die Kollaboration mit KI einbezieht. Jeder Journal-Eintrag wird nach dem Schreiben einer KI-gestützten Reflexion unterzogen:

1. **Dokumentieren:** Ich schreibe den Journal-Eintrag während oder direkt nach der kreativen Arbeit.
2. **Reflektieren mit KI:** Nach dem Schreiben führe ich eine Konversation mit der KI (Claude). Sie liest den Eintrag, stellt Rückfragen und hilft mir, strukturierte Reflexionsfragen zu beantworten.
3. **Verdichten:** Die KI fasst die Konversation in einem standardisierten Format zusammen -- mit immer gleichen Fragen, um Vergleichbarkeit über alle Einträge hinweg zu gewährleisten.

Die festen Reflexionsfragen folgen einer Struktur, die auf autoethnografischer Praxis [@ellis2011autoethnography] und Donald Schöns Konzept des "Reflection-in-Action" [@schoen1983practitioner] basiert:

- **Kontext:** Tool/Workflow, Intention
- **Prozess:** Input, Iterationen, Output
- **Erkenntnisse:** Überraschungen, Fehler als Feature, meine Rolle vs. KI
- **Weiterentwicklung:** Workflow-Änderung, offene Fragen, nächste Schritte

Dieser Prozess selbst ist Teil der Artistic Research: Die KI wird zum Sparringspartner für die Selbstreflexion, nicht zum Autor. Die Antworten entstehen im Dialog -- die KI strukturiert und verdichtet, aber die Erkenntnisse kommen aus meiner Erfahrung.

Die Website stellt diese Reflexionen als spezielle Widgets dar, die visuell vom Haupttext abgesetzt sind und Keywords für die spätere Cross-Entry-Analyse extrahierbar machen.

## Ethische Überlegungen

Da es sich um ein autoethnografisches Projekt handelt, werden keine personenbezogenen Daten Dritter erhoben -- Gegenstand der Untersuchung ist ausschließlich der eigene kreative Prozess.

Der Einsatz generativer KI wirft dennoch ethische Fragen auf, die dieses Projekt bewusst adressiert. Die verwendeten Modelle -- Stable Diffusion, DALL-E, ChatGPT, Claude, Suno, Udio -- wurden auf umfangreichen Datensätzen trainiert, deren Zusammensetzung nicht vollständig transparent ist und deren urheberrechtlicher Status Gegenstand laufender Debatten bleibt. Dieses Spannungsfeld wird nicht verschwiegen, sondern als Teil der Forschung reflektiert.

Transparenz bildet einen Kernwert des Projekts: Der gesamte Entwicklungsprozess ist auf der Website öffentlich dokumentiert, einschließlich verwendeter Tools, Prompts und Iterationsschritte. Alle KI-generierten Inhalte werden als solche kenntlich gemacht.

Auch im analytischen und reflexiven Prozess wird KI eingesetzt. Claude dient als Sparringspartner für die autoethnografische Reflexion und unterstützt die Strukturierung der wissenschaftlichen Dokumentation. Diese Verwendung wird offengelegt, weil die bewusste Entscheidung für Transparenz statt Verschleierung dem methodischen Selbstverständnis dieses Artistic Research-Projekts entspricht: Wenn die Kollaboration mit KI der Forschungsgegenstand ist, muss sie auf allen Ebenen sichtbar sein.

# Meine Forschung: Der Weg zu Kepler

## Ausgangspunkt und erste Schritte

Am Anfang dieser Forschung stand kein theoretisches Konzept, sondern ein ganz praktisches Problem: Kepler brauchte Bilder. Videos. Eine Welt. Kepler existierte bereits als musikalische Identität -- als Name, als Idee, als Figur mit Maske und voxelisiertem Stil. Aber visuell war er fragmentarisch: ein paar Fotos, ein paar Renders aus Unreal Engine, zusammengehalten von einer ästhetischen Intuition, die ich teilte mit Gavin, meinem musikalischen Kollaborateur. Was fehlte, war Konsistenz. Und die Frage, ob generative KI diese Konsistenz liefern konnte, wurde zum Ausgangspunkt meiner Forschung.

Der erste Schritt war analog. Gavin und ich sammelten Referenzen: Pinterest-Boards für Cover-Inspiration, Kleidung, Song-spezifische Vibes. Ein Google-Drive-Ordner für geteilte Ressourcen -- Fotos, existierende Artworks, Konzeptideen. Kein KI-Tool kam zum Einsatz. Was mir dabei bewusst wurde: Der Prozess des Sammelns, Sortierens und Kuratierens ist ein zutiefst menschlicher. Selbst wenn einige der gesammelten Bilder selbst KI-generiert gewesen sein mögen -- die Auswahl, die Kombination, das Gespür für das Richtige, das bleibt bei uns. Diese Beobachtung wurde zum stillen Leitmotiv der gesamten Forschung: Wo genau verläuft die Grenze zwischen menschlicher Kuration und maschineller Generierung?

## Entscheidungen und Abzweigungen

### Die Wahl des visuellen Stils

Kepler trägt eine Maske. Er hat kein sichtbares Gesicht. Sein Stil ist voxelisiert, blockhaft, bewusst abstrahiert. Das ist keine kosmetische Entscheidung, sondern eine identitätsstiftende: Die Maske ist das, was Kepler von einem gewöhnlichen Avatar unterscheidet. Sie schafft Distanz und Projektionsfläche zugleich.

Genau diese Designentscheidung erwies sich als fundamentale Herausforderung für die Arbeit mit generativer KI. Bildgenerierungsmodelle wie Flux oder Stable Diffusion sind auf Trainingsdaten aufgebaut, die überwiegend menschliche Gesichter enthalten. Das Modell "will" ein Gesicht sehen, wo keines sein soll -- es projiziert hartnäckig Gesichtszüge in Keplers Maske, selbst wenn der Prompt explizit dagegen formuliert ist. Keplers Ästhetik liegt in einer Nische, die das Modell nicht versteht, weil sie in den Trainingsdaten nicht oder kaum repräsentiert ist. Was bei einer realistischen, Anime- oder Cartoon-Figur funktioniert hätte, scheiterte an Keplers bewusster Andersartigkeit.

### Die Website als Forschungsartefakt

Eine zentrale Entscheidung war, die Dokumentationswebsite nicht mit einem fertigen CMS zu erstellen, sondern von Grund auf mit Cursor zu bauen -- einem KI-gestützten Code-Editor. Das war keine rein pragmatische Wahl. Die Website ist selbst Teil des künstlerischen Outputs: Ihr dunkles Theme, die Pixel-Headings in "Press Start 2P"-Font, der animierte Matrix-Gradient, der integrierte Musikplayer -- all das transportiert Keplers digitale Identität. Die Website ist nicht Rahmen für die Forschung, sie ist Forschung.

Der Bauprozess mit Cursor offenbarte eine weitere Facette der Mensch-KI-Kollaboration. Ich fühlte mich, wie ich in meinem Journal notierte, "wie eine Managerin mit Gesamtvision, die einen Junior Developer dirigiert". Die KI war schnell bei repetitiven Aufgaben, aber bei komplexen ästhetischen Entscheidungen -- dem richtigen Abstand, dem richtigen Farbton, der richtigen Interaktion -- war ich diejenige, die führte. Mein Vorwissen in Webentwicklung war dabei entscheidend: "Garbage in, garbage out", notierte ich. Je spezifischer die Anforderungen und je größer die Codebase, desto schwieriger wird es für jemanden ohne Vorwissen, die Qualität zu steuern.

### Von der Intention zum Experiment

Die Forschungsfrage [@borgdorff2012conflict; @candy2006practice] lenkte die Experimentwahl nicht wie ein Skript, sondern wie ein Kompass. Ich wollte verschiedene Modalitäten testen: Bild, 3D, Code, Audio. Nicht um Vollständigkeit zu demonstrieren, sondern weil Kepler multimodal existiert und weil ich verstehen wollte, ob die Muster der Kollaboration über Domänen hinweg stabil bleiben. Die Methodik des Practice-Based Research [@candy2006practice] legitimierte dabei einen explorativen Ansatz: Die Praxis selbst generiert die Erkenntnisse, nicht ein vorab definiertes Versuchsdesign.

## Experimente und Ergebnisse

### Experiment 1: Visuelle Konsistenz (ComfyUI + Flux)

Mein erster ernsthafter Versuch, Kepler visuell konsistent mit KI zu generieren, nutzte ComfyUI mit dem Flux-Modell, ergänzt durch IP-Adapter, ControlNet und Face Detailer. Die Installation auf meinem M1 MacBook Pro dauerte Stunden und verschlang viele Gigabyte -- schon das ein Hinweis darauf, dass es sich nicht um die "Zaubertools" handelt, als die generative KI oft dargestellt wird.

Die Ergebnisse waren gemischt. Wenn ich ein Foto als Referenz nutzte, auf dem Kepler einen Basketball hielt, wurde der Basketball im generierten Bild beibehalten, obwohl er dort nicht hingehörte. Das Modell hat kein semantisches Verständnis davon, welche Elemente zusammengehören. Gravierender war das Gesichtsproblem: Face Detailer, eigentlich zur Verbesserung von Gesichtsdetails entwickelt, interpretierte Gesichter in Keplers Maske hinein -- eine Art Face Hallucination, die selbst durch negative Prompts nicht vollständig unterdrückt werden konnte. Es handelt sich um das, was Mori [-@mori2012uncanny] als Uncanny Valley beschreibt, allerdings in einer unerwarteten Richtung: nicht ein fast-menschliches Gesicht, das Unbehagen auslöst, sondern ein Nicht-Gesicht, das vom Modell zwanghaft vervollständigt wird.

Die Erkenntnis war ernüchternd: Art Directability -- die Fähigkeit, die KI gezielt zu steuern -- war nicht gegeben. Schöns [-@schoen1983practitioner] "Reflection-in-Action" zeigte sich hier in seiner elementarsten Form: Die Situation sprach zurück, und zwar anders als erwartet. Meine Reaktion war nicht, den Prozess aufzugeben, sondern die Parameter zu variieren, den Workflow anzupassen, neue Referenzbilder zu testen. Die Modelle sind auf Mainstream-Ästhetiken trainiert. Keplers Nische fällt durch das Raster.

### Experiment 2: Generierte Welten (Marble / World Labs)

Nachdem Kepler als Charakter in der Bildgenerierung an Grenzen gestoßen war, verlagerte ich den Fokus auf Hintergrundwelten. Marble, das erste kommerzielle Produkt von Fei-Fei Lis World Labs, ermöglicht die browserbasierte Erstellung von 3D-Welten durch Gaussian Splats. Ich testete vier verschiedene Ansätze: ein Foto aus einem sowjetisch inspirierten Café, ein Foto von Kepler, ein Pinterest-Bild mit Prompt-Beschreibung und eine reine Text-Prompt, die Claude aus mehreren Pinterest-Bildern synthetisiert hatte.

Der aufschlussreichste Kontrast lag zwischen den letzten beiden Ansätzen. Das direkte Foto ergab eine technisch korrekte, aber kreativ uninteressante Rekonstruktion -- das Modell orientierte sich zu nah am Input. Die Claude-generierte Prompt hingegen produzierte eine Welt, die sich weniger wie eine Rekonstruktion und mehr wie eine Interpretation anfühlte. Vibes statt Referenzbilder: ein Workaround, der ästhetisch produktiver war als der intendierte Workflow.

Bei Personen und Spiegelungen zeigte sich erneut das Uncanny Valley: verzerrte Proportionen, gruselige Doppelgänger. Die Frage nach Coleridges [-@coleridge1817biographia] "willing suspension of disbelief" stellte sich hier unmittelbar: Kann man in eine generierte Welt eintauchen, wenn die Figuren darin Unbehagen auslösen? In der Reflexion entstand die Idee, genau diese "Fehler" als ästhetisches Mittel einzusetzen -- eine Perspektive, die sich durch alle folgenden Experimente ziehen sollte.

### Experiment 3: Musik für ein Alter Ego (Suno AI)

Im Januar 2026 testete ich Suno AI für die Generierung von Musik -- minimal, loopbar, sowjetisch-dystopisch. Zwei Prompt-Ansätze: "Lo-fi" produzierte zu kommerziell klingende Ergebnisse; "Pixel Game Soundtrack" ergab etwas, das eher nach Hero-Soundtrack eines Indie-Games klang als nach atmosphärischer Hintergrundmusik.

Das Kernphänomen dieses Experiments war die Diskrepanz zwischen Beschreibung und Output. Suno generiert zu jedem Track eine detaillierte Beschreibung: "Bitcrushed chiptune pads over a sparse, detuned synth choir; slow, mechanical pulse with occasional metallic hits and distant wind FX." Diese Beschreibung trifft exakt das, was ich mir vorstellte. Der tatsächliche Sound ging in eine andere Richtung -- zu poliert, zu kommerziell, Stock-Music-Qualität. Es war dasselbe Muster wie bei ComfyUI: Generalistische Modelle defaulten auf Mainstream-Ästhetik. Die Nische, die ich suchte, erfordert entweder viele Iterationen, spezialisierte Fine-Tunes oder menschliche Expertise.

### Experiment 4: KI-Dialog als Reflexionswerkzeug

Ein unkonventionelleres Experiment: Auf einer 30-minütigen Autofahrt führte ich ein Voice-Gespräch mit Claude über KI-Grundlagen -- von Shannons Informationstheorie über die Dartmouth Conference bis zur Transformer-Architektur. Das war kein Experiment im engeren Sinne, sondern eine Erkundung der KI als personalisiertem Lernpartner.

Die wichtigste Erkenntnis betraf die Fluency Illusion: Das Gespräch fühlte sich an wie tiefes Verstehen, aber ob ich die Konzepte tatsächlich internalisiert hatte, war unklar. Claude selbst wies mich darauf hin, dass es einen Unterschied gibt zwischen deklarativem Wissen ("wissen, dass") und prozeduralem Wissen ("wissen, wie"). Die Theorie wird erst real, wenn ich sie anwende -- eine Beobachtung, die auf Schöns [-@schoen1983practitioner] Konzept des "Reflection-in-Action" zurückführt: Erkenntnis entsteht nicht im Hören oder Lesen, sondern im Tun.

## Zentrale Beobachtungen aus dem Prozess

Aus der vergleichenden Analyse der Journal-Einträge und der systematischen Reflexion nach dem autoethnografischen Modell [@ellis2011autoethnography] lassen sich vier wiederkehrende Muster identifizieren, die beschreiben, wie KI meinen kreativen Prozess verändert hat. Sie sind "emergent" im Sinne von Borgdorff [-@borgdorff2012conflict]: nicht vorab theoretisch abgeleitet, sondern durch die Praxis selbst hervorgebracht.

### 1. Unvorhersehbarer Flow

Flow entstand dort, wo ich ihn nicht geplant hatte -- und blieb aus, wo ich ihn erwartet hatte. Der Website-Build mit Cursor funktionierte überraschend produktiv: Ich fühlte mich "wie eine Managerin mit Junior Developer", die KI übernahm repetitive Aufgaben, während ich die ästhetische Vision steuerte. Umgekehrt scheiterte die Bildgenerierung für Kepler trotz intensiver Bemühungen: ComfyUI halluzinierte Gesichter in Keplers Maske -- das Modell konnte die Abwesenheit eines Gesichts nicht akzeptieren, ein konkreter Fall des Uncanny Valley [@mori2012uncanny]. Suno produzierte zu kommerzielle Ergebnisse, weil das Modell auf Mainstream-Ästhetik trainiert ist. Die Erkenntnis: KI-gestützte Kreativität ist nicht planbar. Die produktivsten Momente entstanden in Domänen und Konstellationen, die ich vorher nicht als Kernbereich identifiziert hatte.

### 2. Speed vs. Control

KI beschleunigt und begrenzt den kreativen Prozess gleichzeitig. Exploration und Prototyping werden drastisch schneller -- beim Website-Build, bei der Generierung von Marble-Welten, im KI-Dialog als Lernwerkzeug. Aber die Kontrolle über ästhetische Details geht verloren. Das Suno-Experiment illustriert das: Das Modell generiert zu jedem Track eine detaillierte Beschreibung -- "bitcrushed chiptune pads over a sparse, detuned synth choir" -- die exakt das trifft, was ich mir vorstellte. Der tatsächliche Sound ging in eine andere Richtung: zu poliert, zu kommerziell. Bodens [-@boden2004creative] Konzept der explorativen Kreativität hilft hier: Das Modell erkundet den konzeptuellen Raum von "sowjetisch-dystopischer Pixel-Musik" auf der Beschreibungsebene adäquat, scheitert aber an der Übersetzung in klangliche Materie. Die Diskrepanz zwischen Beschreibung und Output ist ein konkretes Symptom des Speed-vs-Control-Tradeoffs: Generierung ist schnell, aber Feinsteuerung ist nicht gegeben.

### 3. Verschiebung der Autorschaft

Über die Experimente hinweg verschob sich meine Rolle ständig. Beim Referenzen-Sammeln war ich Kuratorin -- ein rein menschlicher Akt. Bei ComfyUI war ich Lernende und Experimentierende, orientiert am Workflow einer anderen Person. Beim Website-Build war ich Dirigentin mit Gesamtvision. Bei Suno war ich enttäuschte Kuratorin, die nur auswählen, nicht gestalten konnte. Im KI-Dialog war ich die Fragende.

Diese Rollenvielfalt ist nicht Unschärfe, sondern Qualität. Ellis, Adams und Bochner [-@ellis2011autoethnography] beschreiben autoethnografische Forschung als Methode, die persönliche Erfahrung mit kultureller Analyse verbindet. Die wechselnden Rollen -- Kuratorin, Dirigentin, Kollaborateurin, Lernende -- sind Ausdruck einer Autorschaft, die sich fundamental verschoben hat: nicht mehr alleinige Urheberschaft, nicht vollständige Delegation. Und: "Garbage in, garbage out" -- Domänenwissen ist die Voraussetzung für produktive Kollaboration, nicht KI-Kompetenz. Wer nicht weiß, was gut ist, kann nicht kuratieren.

### 4. KI-Burnout und KI-Enthusiasmus

Die emotionale Dimension der KI-Arbeit erwies sich als eigenständige Prozessveränderung, die ich nicht erwartet hatte. Es gibt einen Zyklus: Begeisterung, wenn etwas unerwartet gut funktioniert -- der Website-Build, die ersten Marble-Welten, ein Claude-Dialog, der mich wirklich weiterbringt. Und dann Frustration und Erschöpfung: wenn ComfyUI stundenlang installiert werden muss und die Ergebnisse enttäuschen, wenn Suno Mainstream produziert statt Nische, wenn Tools sich schneller ändern als man sie lernen kann.

Dieses Pendeln ist nicht Nebensache, sondern reale Belastung im kreativen Prozess. Der ständige Zwang, neue Tools zu evaluieren, Workflows umzubauen, mit Limitierungen zu kämpfen, kostet kreative Energie, die eigentlich in die Kunst fließen sollte. Man muss sich aktiv davor schützen, in diesem Zyklus aufgerieben zu werden. Die Versprechen der Technologie -- schneller, besser, alles möglich -- stehen in Spannung zur Realität einer Praxis, die oft mühsamer ist als die analoge Alternative.

## Rückbezug auf die Forschungsfrage

Wie verändert der Einsatz multimodaler KI-Systeme den kreativen Prozess bei der Entwicklung einer digitalen Künstleridentität?

Vier Antworten kristallisieren sich heraus: Erstens entsteht Flow unvorhersehbar -- dort, wo ich ihn nicht geplant habe (Website-Build), und nicht dort, wo ich ihn erwartet habe (Bildgenerierung, Musik). Zweitens macht KI den Prozess gleichzeitig schneller und begrenzter: Exploration und Prototyping beschleunigen sich drastisch, aber die Kontrolle über ästhetische Details -- das, was Keplers Nische ausmacht -- geht verloren. Drittens hat sich meine Rolle fundamental verschoben: von der Ausführenden zur Kuratorin, Dirigentin, Lernenden, und diese Verschiebung ist nicht stabil, sondern oszilliert je nach Tool und Kontext. Viertens ist der emotionale Zyklus zwischen KI-Enthusiasmus und KI-Burnout selbst Teil der Prozessveränderung -- eine Belastung, die in den Versprechen der Technologie nicht vorkommt, aber in der Praxis allgegenwärtig ist.

Die Veränderungen sind nicht linear, nicht planbar. Sie entstehen im iterativen Prozess [@borgdorff2012conflict; @schoen1983practitioner] -- und sie kosten mehr Energie, als die Versprechen der Technologie vermuten lassen.

# Diskussion und Interpretation

## Zusammenfassung der Ergebnisse

Die vorliegende Arbeit ging der Frage nach, wie der Einsatz multimodaler KI-Systeme den kreativen Prozess bei der Entwicklung des virtuellen Alter Egos Kepler verändert. Die Practice-Based Research, dokumentiert über [N] Experimente mit unterschiedlichen KI-Tools, identifiziert vier zentrale Prozessveränderungen.

Erstens entsteht *Flow unvorhersehbar*: Der Website-Build gelang produktiv, die Bildgenerierung scheiterte an Keplers Nischen-Ästhetik -- Phänomene wie Face Hallucination und Uncanny Valley [@mori2012uncanny] erwiesen sich dabei als konkrete Hindernisse. Zweitens zeigt sich ein durchgängiger *Speed-vs-Control-Tradeoff*: KI beschleunigt Exploration und Prototyping, aber die Kontrolle über ästhetische Details geht verloren -- das Modell "versteht" Nischen sprachlich, kann sie aber medial nicht umsetzen. Drittens hat sich *meine Rolle fundamental verschoben*: von der Ausführenden zur Kuratorin, Dirigentin, Lernenden, wobei Domänenwissen sich als entscheidende Voraussetzung erwies, nicht KI-Kompetenz. Viertens erweist sich der *emotionale Zyklus zwischen KI-Enthusiasmus und KI-Burnout* als eigenständige Prozessveränderung: Der ständige Zwang, neue Tools zu evaluieren und mit Limitierungen zu kämpfen, kostet kreative Energie.

Diese vier Beobachtungen sind keine isolierten Phänomene. Sie verbindet ein gemeinsames Prinzip: Die produktivsten Momente entstanden dort, wo Intention und KI-Eigenlogik in Spannung zueinander traten -- nicht wo sie sich deckten.

## Theoretische Implikationen

Die Ergebnisse legen nahe, dass bestehende Kreativitätstheorien im Kontext der Mensch-KI-Kollaboration neu betrachtet werden sollten. Boden [-@boden2004creative] unterscheidet kombinatorische, explorative und transformative Kreativität. Meine Praxis zeigt, dass generative KI primär als Katalysator für *explorative* Kreativität fungiert: Die Systeme eröffnen einen konzeptuellen Raum, den ich als Künstlerin navigiere, kuratiere und bewerte. Transformative Kreativität -- das Sprengen der Regeln eines konzeptuellen Raums -- ging hingegen durchgehend von meinen Entscheidungen aus, nicht von den Modellen. Die KI generiert Variationen; die Künstlerin entscheidet, welche Variation die Grenzen verschiebt. Der unvorhersehbare Flow, den ich beschreibe, ist letztlich eine Konsequenz dieser Asymmetrie: Exploration ist schnell, aber Transformation erfordert menschliches Urteil.

Borgdorff [-@borgdorff2012conflict] argumentiert, dass künstlerische Forschung implizites Wissen freilegt, das sich nur durch die Praxis selbst artikuliert. Diese These bestätigt sich in meiner Arbeit konkret: Mein Vorwissen über Keplers Ästhetik -- die dystopische Klangwelt, die voxelisierte Maskierung, die Spannung zwischen Lo-Fi und Hyperdigitalem -- war als explizites Briefing an KI-Systeme nur begrenzt übertragbar. Das Prinzip "garbage in, garbage out" erwies sich als Grundregel der Prozessveränderung: Ohne implizites Domänenwissen produziert die Kollaboration generische Ergebnisse. Dieses Wissen zeigte sich erst *im* iterativen Prozess, nicht vor ihm.

Besonders aufschlussreich ist die Verbindung zu Schön [-@schoen1983practitioner]: Reflection-in-Action, das spontane Reagieren auf unerwartete Situationen in der Praxis, beschreibt präzise den Modus, in dem ich auf KI-Halluzinationen, unerwartete Outputs und produktive Fehler reagierte. Das Scheitern eines Prompts war kein Abbruchkriterium, sondern Auslöser für reflektierte Anpassung. Diese Beobachtung erweitert Schöns Konzept um eine neue Dimension: In der Mensch-KI-Kollaboration ist die "Situation, die zurückspricht" kein physisches Material, sondern ein probabilistisches System mit eigener Handlungslogik. Der emotionale Zyklus zwischen Enthusiasmus und Burnout lässt sich als Konsequenz dieser permanenten Reflection-in-Action lesen: Die Situation spricht ständig zurück, und das kostet Kraft.

## Praktische Implikationen

Für Künstler\*innen und Medienproduzent\*innen, die generative KI in ihre Praxis integrieren wollen, ergeben sich aus dieser Arbeit konkrete Erkenntnisse. Die wichtigste: Domänenwissen ist keine optionale Zugabe, sondern Voraussetzung für ästhetisch relevante Ergebnisse. Wer ohne klare ästhetische Vision promptet, erhält den kleinsten gemeinsamen Nenner -- die Mainstream-Ästhetik, auf die Generalist-Modelle trainiert sind. Keplers Nischen-Ästhetik ließ sich nur dort realisieren, wo ich spezifisches Vokabular, präzise Referenzen und ein geschultes Urteilsvermögen einbrachte.

Darüber hinaus zeigt sich ein durchgängiger Speed-versus-Control-Trade-off: KI-Tools beschleunigen die Produktion erheblich, reduzieren aber gleichzeitig die Kontrolle über ästhetische Details. Für die Medienproduktion bedeutet das, dass KI-Werkzeuge sich besonders für Ideation, Prototyping und Exploration eignen, während die finale ästhetische Entscheidung bei der Künstlerin verbleiben muss. Die Rolle verschiebt sich von der Ausführenden zur Kuratorin -- eine Kompetenz, die in der Ausbildung von Medienproduzent\*innen künftig stärker adressiert werden sollte.

## Stärken und Limitierungen

### Stärken

Die methodische Kombination aus Practice-Based Research und Autoethnografie ermöglichte eine Dokumentationstiefe, die rein empirische Ansätze nicht erreichen. Durch die Veröffentlichung des gesamten Prozesses auf der Everything-Machine-Website stelle ich eine Transparenz her, die in künstlerischer Forschung selten ist: Jedes Experiment, jede Reflexion, jeder Fehlschlag ist nachvollziehbar. Die multimodale Perspektive -- Bild, Audio, Code, Text -- bildet zudem die Komplexität zeitgenössischer Medienproduktion ab, anstatt sie auf ein einzelnes Medium zu reduzieren.

### Limitierungen

Als autoethnografische Einzelfallstudie ist die Generalisierbarkeit der Ergebnisse eingeschränkt. Was für meine spezifische Praxis mit Kepler gilt, muss für andere künstlerische Kontexte nicht zutreffen. Die subjektive Perspektive, die in der Artistic Research als Stärke gilt [@ellis2011autoethnography], bleibt in anderen Forschungsparadigmen eine methodische Schwäche. Eine weitere Limitierung liegt im technologischen Wandel: Die Tools, mit denen ich gearbeitet habe, werden sich schneller weiterentwickeln als akademische Publikationszyklen erlauben. Die Ergebnisse beschreiben den Stand einer Technologie in Bewegung. Schließlich muss eine Meta-Ebene benannt werden: Der Schreibprozess dieser Arbeit selbst wurde durch KI-Assistenz unterstützt -- eine Verschränkung, die ich als konsequente Fortsetzung meiner Methodik verstehe, die aber offengelegt werden muss.

## Ausblick

Die Arbeit wirft Fragen auf, die über ihren Rahmen hinausgehen. Wie verändert sich die Kollaboration, wenn KI-Modelle präziser und kontrollierbarer werden? Wird der Speed-vs-Control-Tradeoff sich auflösen, wenn Modelle Nischen-Ästhetiken besser umsetzen können? Und vor allem: Wie nachhaltig ist kreatives Arbeiten mit KI, wenn der Burnout-Zyklus anhält -- wenn Tools sich schneller ändern als man sie lernen kann?

Für Kepler als Projekt sehe ich die Arbeit als Fundament, nicht als Abschluss. Das Alter Ego existiert nun in einem dokumentierten Prozessraum, der weiter bespielt werden kann -- mit zukünftigen Tools, in anderen Medien, mit neuen Kollaborationsmodellen. Die Forschungsfrage bleibt dabei offen, weil die Technologie, auf die sie sich bezieht, selbst in Bewegung ist. Artistic Research, die sich mit generativer KI beschäftigt, muss diesen Zustand der Vorläufigkeit nicht als Schwäche begreifen, sondern als methodische Grundbedingung akzeptieren.

# Literaturverzeichnis
