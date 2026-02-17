---
title: "EVERYTHING MACHINE"
subtitle: "Ein explorativer Artistic Research-Prozess zur visuellen Entwicklung der digitalen Künstleridentität 'Kepler' mittels multimodaler KI-Systeme"
author: "Jennifer Meier"
date: "Februar 2026"
institute: "Technische Hochschule Ostwestfalen-Lippe"
department: "Fachbereich Medien und Kultur, Master Medienproduktion"
course: "Artistic Research"
instructor: "Prof. Dr. Aristotelis Hadjakos"
lang: de-DE
bibliography: references/bibliography.bib
toc: true
abstract: |
  Die vorliegende Arbeit untersucht im Rahmen einer Practice-Led Research mit
  autoethnografischem Ansatz, wie der Einsatz multimodaler KI-Systeme den kreativen
  Prozess bei der Entwicklung einer digitalen Künstleridentität verändert. Am Beispiel
  von Kepler -- einer maskierten, voxelisierten Musiker-Persona -- werden sechs
  Experimente mit KI-Tools aus den Bereichen Bildgenerierung,
  Musikproduktion, Webentwicklung und Texterstellung dokumentiert. Die Analyse identifiziert vier
  zentrale Prozessveränderungen: (1) Flow entsteht unvorhersehbar -- der Website-Build
  mit KI gelang produktiv, während die Bildgenerierung für Kepler an der
  Nischen-Ästhetik scheiterte; (2) KI beschleunigt und begrenzt gleichzeitig --
  Exploration und Prototyping werden schneller, aber die Kontrolle über ästhetische
  Details geht verloren; (3) die Autorschaft verschiebt sich fundamental -- von der
  Ausführenden zur Kuratorin, Dirigentin, Lernenden; (4) der emotionale Zyklus
  zwischen KI-Enthusiasmus und KI-Burnout erweist sich als reale Belastung im
  kreativen Prozess -- der ständige Zwang, neue Tools zu evaluieren und mit
  Limitierungen zu kämpfen, kostet kreative Energie.

  *Keywords: Artistic Research, generative KI, Mensch-KI-Kollaboration, digitale Identität, Autoethnografie, kreativer Prozess, Practice-Led Research*
---

# Einleitung

## Hintergrund und Motivation

Die vorliegende Arbeit versteht Artistic Research im Sinne von Henk Borgdorff [-@borgdorff2012conflict] als künstlerische Praxis, die sich als Forschung qualifiziert: Man macht etwas, findet dabei etwas heraus und dokumentiert es so, dass andere davon lernen können. Zentral ist die Absicht, über die rein persönliche Entwicklung hinaus Wissen zu erzeugen -- durch die Praxis selbst, nicht nur über sie.

Diese Arbeit entsteht in einem Moment, in dem generative KI nahezu alle kreativen Domänen erfasst hat: DALL-E, Midjourney und Stable Diffusion für Bilder; ChatGPT und Claude für Text; Suno und Udio für Musik; Runway und Sora für Video. Eine einzelne Person kann nun Visuals, Texte, Musik und Videos in einer Qualität erstellen, die früher ganze Teams erforderte. Gleichzeitig wirft diese Entwicklung Fragen auf, die nicht abstrakt-philosophisch sind, sondern die konkrete Praxis von Künstler\*innen und Medienproduzent\*innen betreffen: Was bedeutet Autorschaft, wenn Maschinen mitschreiben? Was ist Kreativität, wenn Algorithmen Bilder generieren?

Dass diese Werkzeuge nahezu gleichzeitig verfügbar wurden, ist kein Zufall, sondern Folge konvergierender Durchbrüche: Goodfellow et al. [-@goodfellow2014generative] führten 2014 mit Generative Adversarial Networks (GANs) das Prinzip ein, dass zwei konkurrierende Netzwerke lernen, realistische Daten zu erzeugen -- die Grundlage für alle nachfolgenden Bildgenerierungsmodelle. Die Transformer-Architektur von Vaswani et al. [-@vaswani2017attention] ersetzte 2017 rekurrente Netzwerke durch einen Attention-Mechanismus, der parallele Verarbeitung ermöglichte und die Skalierung auf Milliarden von Parametern erlaubte -- die technische Voraussetzung für GPT, DALL-E und die multimodalen Systeme, mit denen diese Arbeit operiert. Rombach et al. [-@rombach2022ldm] verschoben 2022 den Diffusionsprozess in einen komprimierten latenten Raum und machten hochauflösende Bildgenerierung erstmals auf Consumer-Hardware möglich -- Stable Diffusion, das direkte Fundament von ComfyUI, dem zentralen Tool in Experiment 1.

Im Kontext meiner eigenen Praxis traf diese Frage auf ein konkretes Projekt: „[Kepler](https://www.instagram.com/kepler.mp3/)" -- das musikalische Alter Ego meines Kollaborateurs Gavin, eine maskierte, voxelisierte Musiker-Persona. Kepler steht in einer Transformation: von einer 2D-Figur mit Illustrationen hin zu einer 3D-Präsenz mit Covern, Reels und einer eigenen visuellen Welt. Turkle [-@turkle1995life] zeigte bereits 1995, dass digitale Identitäten nicht bloße Abbilder physischer Personen sind, sondern eigenständige Konstruktionen, die in der Interaktion mit digitalen Umgebungen entstehen und sich verändern. Kepler ist ein solcher Fall: Seine Identität wird nicht abgebildet, sondern durch die Wahl von Maske, Voxel-Stil und visueller Welt aktiv konstruiert -- und genau dieser Konstruktionsprozess wird durch generative KI fundamental verändert. Ich unterstütze diesen Übergang im visuellen Bereich, und genau dieser Prozess wurde zum Ausgangspunkt meiner Forschung: Kann generative KI die visuelle Konsistenz liefern, die Kepler braucht? Und was passiert dabei mit meinem kreativen Prozess, wenn ich nicht mehr nur Werkzeuge benutze, sondern mit ihnen zusammenarbeite?

Das Projekt „Everything Machine" dokumentiert diesen Prozess transparent auf einer öffentlichen [Website](https://jenniferied.github.io/everything-machine/), der vollständige Quellcode ist in einem [GitHub-Repository](https://github.com/jenniferied/everything-machine/) einsehbar. Der Name verweist auf die Idee einer Maschine, die „alles" produzieren kann -- und fragt zugleich, was dieses „alles" wert ist. Denn je mehr ich mit generativer KI arbeitete, desto deutlicher wurde: Sie kann vieles schnell, aber nicht alles gut. Die „Everything Machine" ist zugleich mächtig und begrenzt, und genau diese Spannung macht sie zum Gegenstand künstlerischer Forschung.

## Forschungsfrage und Überblick

Die zentrale Forschungsfrage lautet:

**Wie verändert der Einsatz multimodaler KI-Systeme (Text, Bild, Audio) den kreativen Prozess bei der Entwicklung einer digitalen Künstleridentität?**

Im Laufe der Praxis veränderte sich nicht nur der kreative Prozess selbst, sondern auch die Art, ihn zu dokumentieren: Die Website nahm einen größeren Raum ein als geplant, das KI-gestützte Reflexionsinterview etablierte sich als Methode, wurde dann als zu knapp kritisiert. Diese Verschiebungen bestätigten, dass die Prozessfrage die richtige war: Nicht das Ergebnis, sondern die Veränderung des kreativen Prozesses durch KI erwies sich als zentrale Erkenntnis.

Zur Beantwortung dieser Frage verbindet die Arbeit:

1. **Praktische Experimente:** Iterative Entwicklung von Kepler durch verschiedene KI-Tools, beobachtet auf Prozessveränderungen
2. **Theoretische Reflexion:** Einordnung in Diskurse zu Kreativität, Autorschaft und Human-AI Interaction. Die strukturierten Reflexionsinterviews orientieren sich dabei an fünf Subfragen: Wie verändert sich der Workflow? Wie verschiebt sich die Autorschaft? Welche Rolle spielt Iteration? Wie wird mit Scheitern umgegangen? Und wie entwickelt sich die Ästhetik im Prozess?
3. **Methodische Transparenz:** Öffentliche Dokumentation des gesamten Prozesses

Die Arbeit gliedert sich in fünf Abschnitte: Nach der Einleitung folgt eine Darstellung des Forschungsstands (Abschnitt 2), dann die methodische Beschreibung (Abschnitt 3), die Darstellung meiner Forschung (Abschnitt 4) und schließlich die Diskussion (Abschnitt 5).

# Stand der Forschung

## Artistic Research als Erkenntnisform

Die theoretische Grundlage für dieses Projekt bildet das Feld des Artistic Research. Borgdorff [-@borgdorff2012conflict] unterscheidet zwischen Forschung *über*, *für* und *in* den Künsten. Die vorliegende Arbeit fällt in die dritte Kategorie: Sie forscht nicht über Kunst von außen, sondern aus der Praxis heraus. Artistic Research positioniert künstlerische Praxis nicht als Illustration wissenschaftlicher Erkenntnisse, sondern als eigenständige Erkenntnisform.

Candy unterscheidet in ihrem einflussreichen Report am Creativity & Cognition Studios der University of Technology Sydney zwischen *practice-based* und *practice-led* Research. Practice-based Research bedeutet, dass die kreative Praxis zentral für die Forschung ist und das Kunstwerk selbst Teil des Forschungsergebnisses wird; practice-led Research hingegen nutzt die Praxis, um neues Wissen über Praxis zu generieren, ohne dass das Kunstwerk notwendigerweise Ergebnis ist. Die vorliegende Arbeit ist practice-led: Die Praxis (KI-Experimente, Website-Bau, Musikgenerierung) führt zu neuem Wissen über den kreativen Prozess. Die Artefakte belegen die Erkenntnisse, sind aber nicht selbst das primäre Forschungsergebnis.

## Kreativität und Mensch-KI-Kollaboration

Boden [-@boden2004creative] unterscheidet drei Formen von Kreativität: explorative, kombinatorische und transformative. Generative KI-Systeme operieren primär explorativ und kombinatorisch — sie erkunden einen „conceptual space" und kombinieren erlernte Muster auf neue Weise. Ob sie zu transformativer Kreativität fähig sind, bleibt umstritten. Für diese Arbeit ist die Frage weniger relevant als die praktische Beobachtung: In der Kollaboration mit KI entstehen Ergebnisse, die weder ich allein noch das System allein hervorgebracht hätte.

Galanter [-@galanter2003generative] definiert generative Kunst als jede Praxis, bei der ein autonomes System zum Produktionsprozess beiträgt — vom Computerprogramm über physikalische Prozesse bis zu Regelwerken. KI-gestützte Kunstproduktion steht damit in einer langen Tradition. Gleichzeitig ist der aktuelle Moment qualitativ anders: Multimodale KI-Systeme operieren in Text, Bild und Audio gleichzeitig, mit historisch beispielloser Geschwindigkeit und Zugänglichkeit. Galanter ordnet generative Systeme auf einer Ordnung-Chaos-Skala an, wobei „effektive Komplexität" — die Zone zwischen perfekter Ordnung und totalem Chaos — den ästhetisch interessantesten Bereich markiert. Dieses Konzept wird in den Experimenten dieser Arbeit mehrfach aufgegriffen.

Deterding et al. [-@deterding2017mixed] beschreiben ein Spektrum kreativer Mensch-Computer-Interaktion: von „Mensch als Schöpfer, Computer als Werkzeug" über „Mixed-Initiative" — beide Seiten kollaborieren in einem engen Feedback-Loop — bis „Computer als Schöpfer, Mensch als Publikum". Die Entwicklung von Kepler findet genau in diesem Mixed-Initiative-Raum statt, in dem weder ich noch das KI-System die volle Kontrolle hat.

Franceschelli und Musolesi [-@franceschelli2024creativity] identifizieren in ihrem systematischen Überblick eine zentrale Unterscheidung: Kreativität *des* Systems versus Kreativität *mit* dem System. In dieser Arbeit geht es um Letzteres — nicht ob die KI kreativ „ist", sondern wie sich der kreative Prozess in der Kollaboration verändert.

Mazzone und Elgammal [-@mazzone2019artcreativity] argumentieren, dass KI-Systeme sowohl als Werkzeug als auch als kreativer Partner fungieren können, betonen aber die Grenzen rein generativer Ansätze: Ohne menschliche Intention, Kontextwissen und ästhetisches Urteil bleibt der Output generisch. Diese Beobachtung deckt sich mit dem „Garbage in, garbage out"-Prinzip, das sich durch meine Experimente zieht: Domänenwissen erweist sich als Voraussetzung für ästhetisch relevante Ergebnisse.

Suh et al. [-@suh2021aiglue] untersuchen, wie generative KI in kollaborativen Kompositionsprozessen wirkt. Ihre Ergebnisse zeigen, dass KI nicht nur als technisches Werkzeug, sondern als „sozialer Klebstoff" fungieren kann, der Kommunikation und kreative Aushandlung zwischen menschlichen Beteiligten verändert. Dieser Befund resoniert mit meinem Suno-Experiment, bei dem die KI-generierten Beschreibungen — obwohl die Musik selbst enttäuschte — ein gemeinsames ästhetisches Vokabular lieferten, das für die Weiterarbeit produktiv wurde.

Zwei bekannte Phänomene treten beim praktischen Arbeiten mit generativer KI wiederholt auf. Das *Uncanny Valley* [@mori2012uncanny] beschreibt das Unbehagen, das entsteht, wenn künstliche Darstellungen menschenähnlich, aber nicht perfekt realistisch sind. In der Arbeit mit Kepler zeigt sich dieses Phänomen als konkretes Hindernis — Bildmodelle halluzinieren Gesichtszüge in seine Maske, weil sie die Abwesenheit eines Gesichts nicht akzeptieren. Eng damit verbunden ist Coleridges Konzept der *Suspension of Disbelief* [@coleridge1817biographia]: die Bereitschaft des Publikums, sich auf eine fiktionale Welt einzulassen. Für Kepler als virtuelle Persona stellt sich die Frage, ob Rezipient\*innen ihn als „authentischen" Künstler akzeptieren — eine Frage, die im kreativen Prozess ständig mitverhandelt wird und durch KI-Artefakte immer wieder gestört wird.

## Artistic Research mit generativer KI

Neben der theoretisch-empirischen Forschung gibt es eine wachsende Zahl von Artist-Practitioner-Projekten, die generative KI aus der Praxis heraus untersuchen. Monin und Sadokierski [-@monin2025prompting] beschreiben Prompting als „Thinking-With" — einen Denkprozess, bei dem die Formulierung von Prompts selbst zur Erkenntnismethode wird. Ihr Projekt zur Visualisierung eines ausgestorbenen Zwerg-Emus verbindet Collagepraktiken mit KI-Bildgenerierung und zeigt, wie die iterative Auseinandersetzung mit KI-generierten Bildern das Verständnis des Forschungsgegenstands vertieft.

Hansen [-@hansen2023designers] entwickelt ein Modell für die sich verändernde Rolle von Grafikdesigner\*innen im KI-Zeitalter. Gestützt auf die Trias von Deduktion, Induktion und Abduktion argumentiert er, dass deduktive und induktive Designaufgaben effektiv an KI delegierbar sind, während abduktive Aufgaben weiterhin menschliche Kompetenz erfordern — die Kernkompetenz verschiebt sich von der Ausführung zur Kuration und kritischen Bewertung, eine Beobachtung, die sich mit meinem Befund der Autorschaftsverschiebung deckt. Torres Núñez del Prado [-@torresnunez2025encoding] untersucht in „Encoding Culture", wie kulturelle Kodierungen in KI-Trainingsdaten eingebettet sind und wie Künstler\*innen diese sichtbar machen und unterlaufen können — eine Perspektive, die für Keplers Konfrontation mit normativen Gesichtsmodellen direkt relevant ist.

Diese Projekte teilen den reflexiven Ansatz der vorliegenden Arbeit, arbeiten aber primär in einer einzelnen Modalität (Bild oder Text). Die vorliegende Arbeit unterscheidet sich durch ihren multimodalen Ansatz: Die Experimente erstrecken sich über Bild, Audio, 3D und Code und ermöglichen so eine domänenübergreifende Analyse der Prozessveränderungen.

## Forschungslücke

Während autoethnografische Studien zu KI-gestützten kreativen Prozessen in einzelnen Domänen existieren -- insbesondere in der Musikkomposition und der visuellen Kunst -- fehlen Tiefenstudien, die den iterativen Entstehungsprozess *multimodaler* hybrider Kunstwerke aus der Perspektive der beteiligten Künstler\*innen dokumentieren. Die oben genannten Arbeiten von Franceschelli und Musolesi [-@franceschelli2024creativity], Mazzone und Elgammal [-@mazzone2019artcreativity] sowie die Artist-Practitioner-Quellen zeigen zwar das wachsende Feld, aber keine dieser Arbeiten verbindet systematische autoethnografische Reflexion mit multimodaler KI-Praxis -- über Text, Bild und Audio hinweg -- im Kontext der Entwicklung einer konkreten digitalen Künstleridentität. Diese Arbeit adressiert diese Lücke.

# Methodologie

## Methodischer Rahmen: Practice-Led Research

Das Projekt folgt dem Paradigma des Practice-Led Research, bei dem die künstlerische Praxis als Erkenntnisquelle dient und Wissen über den kreativen Prozess generiert. Die Entwicklung von Kepler ist nicht Gegenstand einer externen Untersuchung, sondern der Ort, an dem Forschung stattfindet.

## Konkrete Methoden

Die Forschung verbindet drei methodische Stränge: autoethnografisches Journaling mit iterativer Experimentierung, eine öffentliche Website als Forschungsartefakt und einen KI-gestützten Reflexionsprozess.

Regelmäßige Journal-Einträge dokumentieren den kreativen Prozess nach einer strukturierten Vorlage (Intention, Prozess, Ergebnis, Reflexion, nächste Schritte). Systematische Experimente mit verschiedenen KI-Tools -- Stable Diffusion, DALL-E, ChatGPT, Claude, Suno, Udio -- folgen einem Zyklus von Hypothese, Experiment, Dokumentation und Anpassung. Beide Stränge greifen ineinander: Jedes Experiment mündet in einen Journal-Eintrag, jeder Eintrag informiert das nächste Experiment.

Die Website „Everything Machine" macht den gesamten Prozess transparent zugänglich und ist selbst Teil des künstlerischen Outputs. Sie wurde bewusst ohne CMS, sondern als maßgeschneiderte Webanwendung entwickelt, deren technische Architektur die methodischen Prinzipien spiegelt: Transparenz durch Versionierung (Git), Iterativität durch modularen Aufbau, Selbstreflexion durch ein integriertes Journal-System.

Ein zentrales methodisches Element ist der KI-gestützte Reflexionsprozess: Nach jedem Experiment schreibe ich einen Journal-Eintrag und führe anschließend eine strukturierte Konversation mit Claude, die den Eintrag liest, Rückfragen stellt und die Reflexion entlang fester Fragen verdichtet. Diese Fragen basieren auf autoethnografischer Praxis [@ellis2011autoethnography] und Schöns „Reflection-in-Action" [@schoen1983practitioner] und decken Kontext, Prozess, Erkenntnisse und Weiterentwicklung ab. Die KI wird dabei zum Sparringspartner für die Selbstreflexion, nicht zum Autor: Sie strukturiert und verdichtet, aber die Erkenntnisse kommen aus meiner Erfahrung.

## Ethische Überlegungen und KI-Offenlegung

Da es sich um ein autoethnografisches Projekt handelt, werden keine personenbezogenen Daten Dritter erhoben. Die verwendeten KI-Modelle wurden auf Datensätzen trainiert, deren Zusammensetzung nicht vollständig transparent ist und deren urheberrechtlicher Status Gegenstand laufender Debatten bleibt. Dieses Spannungsfeld wird als Teil der Forschung reflektiert, nicht verschwiegen.

Generative KI kam in dieser Arbeit auf vier Ebenen zum Einsatz: (1) als **Experimentgrundlage** -- Stable Diffusion, DALL-E, Suno AI und Marble bildeten den Forschungsgegenstand; (2) als **Reflexionspartner** -- nach jedem Experiment wurde eine strukturierte Reflexion im Dialog mit Claude durchgeführt (vollständige Transkripte in Anhang B); (3) als **Schreibassistenz** -- Claude unterstützte bei Strukturierung und Formulierung dieser Dokumentation; (4) als **Entwicklungstool** -- die Projektwebsite wurde mit Cursor gebaut (selbst Gegenstand von Experiment 4). Argumentation, Quellenauswahl und alle inhaltlichen Entscheidungen liegen bei der Autorin. Der gesamte Prozess ist auf der Website und im GitHub-Repository öffentlich dokumentiert.

# Meine Forschung: Der Weg zu Kepler

## Ausgangspunkt und erste Schritte

Am Anfang dieser Forschung stand kein theoretisches Konzept, sondern ein ganz praktisches Problem: Kepler brauchte Bilder. Videos. Eine Welt. Kepler existierte bereits als musikalische Identität -- als Name, als Idee, als Figur mit Maske und voxelisiertem Stil. Aber visuell war er fragmentarisch: ein paar Fotos, ein paar Renders aus Unreal Engine, zusammengehalten von einer ästhetischen Intuition, die ich teilte mit Gavin, meinem musikalischen Kollaborateur. Was fehlte, war Konsistenz. Und die Frage, ob generative KI diese Konsistenz liefern konnte, wurde zum Ausgangspunkt meiner Forschung.

Der erste Schritt kam ohne KI aus. Gavin und ich sammelten Referenzen: Pinterest-Boards für Cover-Inspiration, Kleidung, Song-spezifische Vibes. Ein Google-Drive-Ordner für geteilte Ressourcen: Fotos, existierende Artworks, Konzeptideen. Kein KI-Tool kam zum Einsatz. Was mir dabei bewusst wurde: Der Prozess des Sammelns, Sortierens und Kuratierens ist ein zutiefst menschlicher. Selbst wenn einige der gesammelten Bilder selbst KI-generiert gewesen sein mögen, die Auswahl, die Kombination, das Gespür für das Richtige, das bleibt bei uns. Diese Beobachtung wurde zum stillen Leitmotiv der gesamten Forschung: Wo genau verläuft die Grenze zwischen menschlicher Kuration und maschineller Generierung?

## Entscheidungen und Abzweigungen

### Die Wahl des visuellen Stils

Kepler trägt eine Maske. Er hat kein sichtbares Gesicht. Sein Stil ist voxelisiert, blockhaft, bewusst abstrahiert. Das ist keine kosmetische Entscheidung, sondern eine identitätsstiftende: Die Maske ist das, was Kepler von einem gewöhnlichen Avatar unterscheidet. Sie schafft Distanz und Projektionsfläche zugleich.

Genau diese Designentscheidung erwies sich als fundamentale Herausforderung für die Arbeit mit generativer KI. Bildgenerierungsmodelle wie Flux oder Stable Diffusion sind auf Trainingsdaten aufgebaut, die überwiegend menschliche Gesichter enthalten. Das Modell "will" ein Gesicht sehen, wo keines sein soll; es projiziert hartnäckig Gesichtszüge in Keplers Maske, selbst wenn der Prompt explizit dagegen formuliert ist. Keplers Ästhetik liegt in einer Nische, die das Modell nicht versteht, weil sie in den Trainingsdaten nicht oder kaum repräsentiert ist. Was bei einer realistischen, Anime- oder Cartoon-Figur funktioniert hätte, scheiterte an Keplers bewusster Andersartigkeit.

### Die Website als Forschungsartefakt

Eine zentrale Entscheidung war, die Dokumentationswebsite nicht mit einem fertigen CMS zu erstellen, sondern von Grund auf mit Cursor zu bauen -- einem KI-gestützten Code-Editor. Das war keine rein pragmatische Wahl. Die Website ist selbst Teil des künstlerischen Outputs: Ihr dunkles Theme, die Pixel-Headings in "Press Start 2P"-Font, der animierte Matrix-Gradient, der integrierte Musikplayer -- all das transportiert Keplers digitale Identität. Die Website ist nicht Rahmen für die Forschung, sie ist Forschung.

Der Bauprozess mit Cursor offenbarte eine weitere Facette der Mensch-KI-Kollaboration. Ich fühlte mich, wie ich in meinem Journal notierte, "wie eine Managerin mit Gesamtvision, die einen Junior Developer dirigiert". Die KI war schnell bei repetitiven Aufgaben, aber bei komplexen ästhetischen Entscheidungen -- dem richtigen Abstand, dem richtigen Farbton, der richtigen Interaktion -- war ich diejenige, die führte. Mein Vorwissen in Webentwicklung war dabei entscheidend: "Garbage in, garbage out", notierte ich. Je spezifischer die Anforderungen und je größer die Codebase, desto schwieriger wird es für jemanden ohne Vorwissen, die Qualität zu steuern.

### Von der Intention zum Experiment

Die Forschungsfrage lenkte die Experimentwahl nicht wie ein Skript, sondern wie ein Kompass. Ich wollte verschiedene Modalitäten testen: Bild, 3D, Code, Audio. Nicht um Vollständigkeit zu demonstrieren, sondern weil Kepler multimodal existiert und weil ich verstehen wollte, ob die Muster der Kollaboration über Domänen hinweg stabil bleiben. Die Methodik des Practice-Led Research [@candy2006practice] legitimierte dabei einen explorativen Ansatz: Die Praxis selbst generiert die Erkenntnisse, nicht ein vorab definiertes Versuchsdesign.

## Experimente und Ergebnisse

### Experiment 1: Visuelle Konsistenz (ComfyUI + Flux)

Mein erster ernsthafter Versuch, Kepler visuell konsistent mit KI zu generieren, nutzte ComfyUI mit dem Flux-Modell, ergänzt durch IP-Adapter, ControlNet und Face Detailer. Die Installation auf meinem M1 MacBook Pro dauerte Stunden und verschlang viele Gigabyte, schon das ein Hinweis darauf, dass es sich nicht um die "Zaubertools" handelt, als die generative KI oft dargestellt wird.

Die Ergebnisse waren gemischt. Wenn ich ein Foto als Referenz nutzte, auf dem Kepler einen Basketball hielt, wurde der Basketball im generierten Bild beibehalten, obwohl er dort nicht hingehörte. Das Modell hat kein semantisches Verständnis davon, welche Elemente zusammengehören. Gravierender war das Gesichtsproblem: Face Detailer, eigentlich zur Verbesserung von Gesichtsdetails entwickelt, interpretierte Gesichter in Keplers Maske hinein -- eine Art Face Hallucination, die selbst durch negative Prompts nicht vollständig unterdrückt werden konnte. Es handelt sich um das, was Mori [-@mori2012uncanny] als Uncanny Valley beschreibt, allerdings in einer unerwarteten Richtung: nicht ein fast-menschliches Gesicht, das Unbehagen auslöst, sondern ein Nicht-Gesicht, das vom Modell zwanghaft vervollständigt wird. In Galanters [-@galanter2003generative] Terminologie driften die Halluzinationen in den Bereich der Unordnung ab — weg von der "effektiven Komplexität", die Keplers Ästhetik ausmacht.

Die Erkenntnis war ernüchternd: Art Directability -- die Fähigkeit, die KI gezielt zu steuern -- war nicht gegeben. Schöns [-@schoen1983practitioner] "Reflection-in-Action" zeigte sich hier in seiner elementarsten Form: Die Situation sprach zurück, und zwar anders als erwartet. Meine Reaktion war nicht, den Prozess aufzugeben, sondern die Parameter zu variieren, den Workflow anzupassen, neue Referenzbilder zu testen. Die Modelle sind auf Mainstream-Ästhetiken trainiert. Keplers Nische fällt durch das Raster.

### Experiment 2: Generierte Welten (Marble / World Labs)

Nachdem Kepler als Charakter in der Bildgenerierung an Grenzen gestoßen war, verlagerte ich den Fokus auf Hintergrundwelten. Marble, das erste kommerzielle Produkt von Fei-Fei Lis World Labs, ermöglicht die browserbasierte Erstellung von 3D-Welten durch Gaussian Splats. Ich testete vier verschiedene Ansätze: ein Foto aus einem sowjetisch inspirierten Café, ein Foto von Kepler, ein Pinterest-Bild mit Prompt-Beschreibung und eine reine Text-Prompt, die Claude aus mehreren Pinterest-Bildern synthetisiert hatte.

Der aufschlussreichste Kontrast lag zwischen den letzten beiden Ansätzen. Das direkte Foto ergab eine technisch korrekte, aber kreativ uninteressante Rekonstruktion: Das Modell orientierte sich zu nah am Input. Die Claude-generierte Prompt hingegen produzierte eine Welt, die sich weniger wie eine Rekonstruktion und mehr wie eine Interpretation anfühlte. Vibes statt Referenzbilder: ein Workaround, der ästhetisch produktiver war als der intendierte Workflow.

Bei Personen und Spiegelungen zeigte sich erneut das Uncanny Valley: verzerrte Proportionen, gruselige Doppelgänger. Die Frage nach Coleridges [-@coleridge1817biographia] "willing suspension of disbelief" stellte sich hier unmittelbar: Kann man in eine generierte Welt eintauchen, wenn die Figuren darin Unbehagen auslösen? In der Reflexion entstand die Idee, genau diese "Fehler" als ästhetisches Mittel einzusetzen, eine Perspektive, die sich durch alle folgenden Experimente ziehen sollte.

### Experiment 3: Musik für ein Alter Ego (Suno AI)

Im Januar 2026 testete ich Suno AI für die Generierung von Musik -- minimal, loopbar, sowjetisch-dystopisch. Zwei Prompt-Ansätze: "Lo-fi" produzierte zu kommerziell klingende Ergebnisse; "Pixel Game Soundtrack" ergab etwas, das eher nach Hero-Soundtrack eines Indie-Games klang als nach atmosphärischer Hintergrundmusik.

Das Kernphänomen dieses Experiments war die Diskrepanz zwischen Beschreibung und Output. Suno generiert zu jedem Track eine detaillierte Beschreibung: "Bitcrushed chiptune pads over a sparse, detuned synth choir; slow, mechanical pulse with occasional metallic hits and distant wind FX." Diese Beschreibung trifft exakt das, was ich mir vorstellte. Der tatsächliche Sound ging in eine andere Richtung: zu poliert, zu kommerziell, Stock-Music-Qualität. In Galanters [-@galanter2003generative] Terminologie produziert Suno Output mit hoher Ordnung, aber niedriger effektiver Komplexität — zu glatt und vorhersehbar für die angestrebte Lo-Fi-Pixel-Ästhetik. Es war dasselbe Muster wie bei ComfyUI: Generalistische Modelle defaulten auf Mainstream-Ästhetik. Die Nische, die ich suchte, erfordert entweder viele Iterationen, spezialisierte Fine-Tunes oder menschliche Expertise.

### Experiment 4: KI-Dialog als Reflexionswerkzeug

Ein unkonventionelleres Experiment: Auf einer 30-minütigen Autofahrt führte ich ein Voice-Gespräch mit Claude über KI-Grundlagen -- von Shannons Informationstheorie über die Dartmouth Conference bis zur Transformer-Architektur. Das war kein Experiment im engeren Sinne, sondern eine Erkundung der KI als personalisiertem Lernpartner.

Die wichtigste Erkenntnis betraf die Fluency Illusion: Das Gespräch fühlte sich an wie tiefes Verstehen, aber ob ich die Konzepte tatsächlich internalisiert hatte, war unklar. Claude selbst wies mich darauf hin, dass es einen Unterschied gibt zwischen deklarativem Wissen ("wissen, dass") und prozeduralem Wissen ("wissen, wie"). Die Theorie wird erst real, wenn ich sie anwende, eine Beobachtung, die auf Schöns [-@schoen1983practitioner] Konzept des "Reflection-in-Action" zurückführt: Erkenntnis entsteht nicht im Hören oder Lesen, sondern im Tun.


### Experiment 5: Automatisierte Bildpipeline (fal.ai API + Claude Code)

Nach vier Einzelexperimenten stellte sich eine methodische Frage: Was passiert, wenn ich den Prozess systematisiere? Gemeinsam mit Claude Code baute ich eine automatisierte Pipeline, die über die fal.ai API neun verschiedene Bildgenerierungsmodelle mit denselben Prompts und Referenzbildern ansteuerte. Die Kollaboration war dreistufig: Ich definierte die ästhetische Vision und die Evaluationskriterien, Claude Code schrieb den Pipeline-Code und orchestrierte die API-Aufrufe, die Bildmodelle generierten die Outputs -- eine neue Konstellation, in der ich als Auftraggeberin eines KI-Agenten fungierte, der seinerseits KI-Modelle steuert.

Die Pipeline durchlief sieben Phasen, die den Möglichkeitsraum zwischen neun Modellen, zwei Input-Typen und drei Signature Scenes systematisch absteckten. Insgesamt entstanden 134 Bilder in 24 Output-Ordnern, evaluiert nach "Gefällt mir", "Halluzinationen" und Kommentar.

```{=latex}
\clearpage
```

#### Phase 1: Modell-Screening (5 Modelle, A-Pose)

Als Referenzbild diente Keplers A-Pose-Render -- ein quadratischer 1024×1024 Render mit seitlich ausgestreckten Armen. Fünf Modelle wurden getestet:

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/inputs/kepler-a-pose-1024.jpg}
\caption{Input: Kepler A-Pose (1024\texttimes1024)}
\end{figure}
```

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.20\textwidth]{experiments/fal-pipeline/outputs/01_minimax_subject/01_minimax_subject_000.jpg}\hfill
\includegraphics[width=0.20\textwidth]{experiments/fal-pipeline/outputs/01_minimax_subject/01_minimax_subject_010.jpg}\hfill
\includegraphics[width=0.20\textwidth]{experiments/fal-pipeline/outputs/01_minimax_subject/01_minimax_subject_020.jpg}
\\[1pt]{\scriptsize\color{darktext!60} MiniMax Subject Reference}

\vspace{3pt}

\includegraphics[width=0.20\textwidth]{experiments/fal-pipeline/outputs/02_zimage_controlnet/02_zimage_controlnet_000.jpg}\hfill
\includegraphics[width=0.20\textwidth]{experiments/fal-pipeline/outputs/02_zimage_controlnet/02_zimage_controlnet_010.jpg}\hfill
\includegraphics[width=0.20\textwidth]{experiments/fal-pipeline/outputs/02_zimage_controlnet/02_zimage_controlnet_020.jpg}
\\[1pt]{\scriptsize\color{darktext!60} Z-Image Turbo ControlNet}

\vspace{3pt}

\includegraphics[width=0.20\textwidth]{experiments/fal-pipeline/outputs/03_flux_depth/03_flux_depth_000.jpg}\hfill
\includegraphics[width=0.20\textwidth]{experiments/fal-pipeline/outputs/03_flux_depth/03_flux_depth_010.jpg}\hfill
\includegraphics[width=0.20\textwidth]{experiments/fal-pipeline/outputs/03_flux_depth/03_flux_depth_020.jpg}
\\[1pt]{\scriptsize\color{darktext!60} FLUX Depth LoRA}

\vspace{3pt}

\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/04_flux_canny/04_flux_canny_010.jpg}\hfill
\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/04_flux_canny/04_flux_canny_020.jpg}
\\[1pt]{\scriptsize\color{darktext!60} FLUX Canny LoRA}

\caption{Phase 1: Modell-Screening -- MiniMax, Z-Image, FLUX Depth, FLUX Canny. Bilder in der \href{https://jennifer-meier.github.io/everything-machine/\#images}{Bild-Galerie} vergrößerbar.}
\end{figure}
```

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.3\textwidth]{experiments/fal-pipeline/outputs/05_era3d/05_era3d_000.jpg}\hfill
\includegraphics[width=0.3\textwidth]{experiments/fal-pipeline/outputs/05_era3d/05_era3d_001.jpg}\hfill
\includegraphics[width=0.3\textwidth]{experiments/fal-pipeline/outputs/05_era3d/05_era3d_002.jpg}

\vspace{2pt}

\includegraphics[width=0.3\textwidth]{experiments/fal-pipeline/outputs/05_era3d/05_era3d_003.jpg}\hfill
\includegraphics[width=0.3\textwidth]{experiments/fal-pipeline/outputs/05_era3d/05_era3d_004.jpg}\hfill
\includegraphics[width=0.3\textwidth]{experiments/fal-pipeline/outputs/05_era3d/05_era3d_005.jpg}

\caption{Phase 1: Era3D Multiview -- nutzlos im Vergleich zu eigenen Renders. \href{https://jennifer-meier.github.io/everything-machine/\#images}{Bild-Galerie}}
\end{figure}
```

```{=latex}
\begin{table}[H]
\centering\small
\caption{Phase 1: Modell-Screening (A-Pose, quadratisch)}
\begin{tabularx}{\textwidth}{lll>{\raggedright\arraybackslash}X}
\toprule
\textbf{Modell} & \textbf{Bewertung} & \textbf{Halluz.} & \textbf{Kommentar} \\
\midrule
MiniMax Subject & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & Minecraft-Stil, Gesichtszüge \\
Z-Image ControlNet & bedingt & \textcolor{evalgreen}{nein} & A-Pose erhalten, clean \\
FLUX Depth LoRA & \textcolor{evalred}{nein} & -- & Körper wird humanoid \\
FLUX Canny LoRA & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & Volles Gesicht halluziniert \\
Era3D & \textcolor{evalred}{nein} & -- & Nutzlos -- eigene Renders besser \\
\bottomrule
\end{tabularx}
\end{table}
```

**Verworfene Modelle.** Keines der fünf Modelle lieferte überzeugende Ergebnisse. MiniMax Subject Reference interpretierte Keplers Voxel-Ästhetik als Minecraft-Welt und halluzinierte menschliche Gesichtszüge, obwohl der Prompt "faceless" explizit vorgab. FLUX Depth LoRA bewahrte zwar die Körperhaltung über eine Tiefenkarte, glättete aber die blockige Geometrie zu einem humanoid wirkenden Körper. FLUX Canny LoRA produzierte das gravierendste Problem: Ein vollständiges menschliches Gesicht erschien auf Keplers faceless Kopf -- dasselbe Halluzinationsphänomen wie in Experiment 1. Era3D generierte Multiview-Ansichten, die in besserer Qualität direkt in Unreal Engine gerendert werden können. Einzig Z-Image Turbo ControlNet vermied Halluzinationen und bewahrte die A-Pose, blieb aber insgesamt zu limitiert für Szenen-Kontexte.

**Methodisches Ergebnis.** Depth-basierte Steuerung erwies sich als überlegen gegenüber Canny-Edges, und die Halluzinationsanfälligkeit variierte erheblich zwischen Modellen, die nominell dieselbe Aufgabe lösten. Für Phase 2 recherchierte ich gezielt leistungsstärkere Modelle -- insbesondere FLUX Kontext Pro, GPT-Image-1.5, SeedDream und NanoBanana Pro --, die sich in Benchmarks als State-of-the-Art für Charakter-Konsistenz erwiesen hatten.

```{=latex}
\clearpage
```

#### Phase 2: Top-Modelle in Szenen (A-Pose)

Die vier vielversprechendsten Modelle wurden in Szenen-Kontexte eingeführt, jeweils drei Varianten mit demselben A-Pose-Input.

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/06_flux_kontext/06_flux_kontext_000.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/06_flux_kontext/06_flux_kontext_010.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/06_flux_kontext/06_flux_kontext_020.jpg}
\\[1pt]{\scriptsize\color{darktext!60} FLUX Kontext Pro}

\vspace{4pt}

\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/07_gpt_image_15/07_gpt_image_15_000.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/07_gpt_image_15/07_gpt_image_15_010.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/07_gpt_image_15/07_gpt_image_15_020.jpg}
\\[1pt]{\scriptsize\color{darktext!60} GPT-Image-1.5}

\vspace{4pt}

\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/08_seeddream/08_seeddream_000.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/08_seeddream/08_seeddream_010.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/08_seeddream/08_seeddream_020.jpg}
\\[1pt]{\scriptsize\color{darktext!60} SeedDream v4.5}

\vspace{4pt}

\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/09_nanobanana_pro/09_nanobanana_pro_000.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/09_nanobanana_pro/09_nanobanana_pro_010.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/09_nanobanana_pro/09_nanobanana_pro_020.jpg}
\\[1pt]{\scriptsize\color{darktext!60} NanoBanana Pro}

\caption{Phase 2: Top-Modelle in Szenen (A-Pose). \href{https://jennifer-meier.github.io/everything-machine/\#images}{Bild-Galerie}}
\end{figure}
```

```{=latex}
\begin{table}[H]
\centering\small
\caption{Phase 2: Top-Modelle in Szenen (A-Pose)}
\begin{tabularx}{\textwidth}{lll>{\raggedright\arraybackslash}X}
\toprule
\textbf{Modell} & \textbf{Bewertung} & \textbf{Halluz.} & \textbf{Kommentar} \\
\midrule
FLUX Kontext Pro & bedingt & -- & Wird besser \\
GPT-Image-1.5 & bedingt & teilweise & Solide, aber Halluzinationen \\
SeedDream v4.5 & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & Volles Gesicht halluziniert \\
NanoBanana Pro & \textcolor{evalgreen}{gut} & teilweise & Beste Phase-2-Ergebnisse \\
\bottomrule
\end{tabularx}
\end{table}
```

SeedDream schied wegen Gesichtshalluzinationen aus. Drei Finalisten blieben: FLUX Kontext Pro, GPT-Image-1.5 und NanoBanana Pro.

```{=latex}
\clearpage
```

#### Phase 2b: Der Posed-Input-Durchbruch

Der entscheidende Durchbruch kam mit dem Wechsel zum "Posed Input" -- einem Render, in dem Kepler natürlich steht. Die A-Pose führte zu einem Overfitting-Effekt: Das Modell übernahm die starre Haltung wörtlich.

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/inputs/kepler-a-pose-1024.jpg}\hfill
{\Large\color{accentgreen}$\rightarrow$}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/inputs/kepler-posed-1024.jpg}
\caption{Input-Wechsel: A-Pose $\rightarrow${} Posed -- natürliche Haltung statt T-Pose}
\end{figure}
```

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/10_flux_kontext_posed/10_flux_kontext_posed_000.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/10_flux_kontext_posed/10_flux_kontext_posed_010.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/10_flux_kontext_posed/10_flux_kontext_posed_020.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/10_flux_kontext_posed/10_flux_kontext_posed_030.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/10_flux_kontext_posed/10_flux_kontext_posed_040.jpg}
\\[1pt]{\scriptsize\color{darktext!60} FLUX Kontext Posed}

\vspace{4pt}

\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/11_gpt15_posed/11_gpt15_posed_000.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/11_gpt15_posed/11_gpt15_posed_010.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/11_gpt15_posed/11_gpt15_posed_020.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/11_gpt15_posed/11_gpt15_posed_030.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/11_gpt15_posed/11_gpt15_posed_040.jpg}
\\[1pt]{\scriptsize\color{darktext!60} GPT-Image-1.5 Posed}

\vspace{4pt}

\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/12_nanobanana_posed/12_nanobanana_posed_000.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/12_nanobanana_posed/12_nanobanana_posed_010.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/12_nanobanana_posed/12_nanobanana_posed_020.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/12_nanobanana_posed/12_nanobanana_posed_030.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/12_nanobanana_posed/12_nanobanana_posed_040.jpg}
\\[1pt]{\scriptsize\color{darktext!60} NanoBanana Posed}

\caption{Phase 2b: Drei Finalisten mit Posed Input (je 5 Varianten). \href{https://jennifer-meier.github.io/everything-machine/\#images}{Bild-Galerie}}
\end{figure}
```

```{=latex}
\begin{table}[H]
\centering\small
\caption{Phase 2b: Posed Input (3 Finalisten)}
\begin{tabularx}{\textwidth}{lll>{\raggedright\arraybackslash}X}
\toprule
\textbf{Modell} & \textbf{Bewertung} & \textbf{Halluz.} & \textbf{Kommentar} \\
\midrule
FLUX Kontext Posed & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & Gesichter halluziniert \\
GPT-Image-1.5 Posed & \textcolor{evalgreen}{ja} & teilweise & Solideste Ergebnisse \\
NanoBanana Posed & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} & Stärkste Voxel-Ästhetik \\
\bottomrule
\end{tabularx}
\end{table}
```

FLUX Kontext schied aus -- Posed Input verstärkte die Gesichtshalluzinationen. Zwei Finalisten mit komplementären Stärken: GPT-Image-1.5 (atmosphärischer) und NanoBanana Pro (stilistisch konsistenter).

```{=latex}
\clearpage
```

#### Phase 3a: Signature Scenes v1 -- Ratio-Bug

Ab Phase 3a wurden GPT-Image-1.5 und NanoBanana Pro parallel in "Signature Scenes" getestet: Studio, Retro Car Bridge, Spiral Staircase, Pool Floaty. Ein Ratio-Bug in der Pipeline betraf GPT -- alle Outputs kamen quadratisch statt im gewünschten Format. NanoBanana Pro lieferte korrekte Portrait- und Landscape-Formate.

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/13_gpt15_scenes_portrait/studio.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/13_gpt15_scenes_portrait/retro_car_bridge.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/13_gpt15_scenes_portrait/spiral_staircase.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/13_gpt15_scenes_portrait/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} GPT-1.5 ``Portrait'' (13) -- quadratisch durch Ratio-Bug}

\vspace{4pt}

\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/13_gpt15_scenes_landscape/studio.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/13_gpt15_scenes_landscape/retro_car_bridge.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/13_gpt15_scenes_landscape/spiral_staircase.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/13_gpt15_scenes_landscape/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} GPT-1.5 ``Landscape'' (13) -- ebenfalls quadratisch}

\vspace{8pt}

\includegraphics[width=0.14\textwidth]{experiments/fal-pipeline/outputs/14_nanobanana_scenes_portrait/studio.jpg}\hfill
\includegraphics[width=0.14\textwidth]{experiments/fal-pipeline/outputs/14_nanobanana_scenes_portrait/retro_car_bridge.jpg}\hfill
\includegraphics[width=0.14\textwidth]{experiments/fal-pipeline/outputs/14_nanobanana_scenes_portrait/spiral_staircase.jpg}\hfill
\includegraphics[width=0.14\textwidth]{experiments/fal-pipeline/outputs/14_nanobanana_scenes_portrait/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} NanoBanana Portrait (14) -- korrektes Format}

\vspace{4pt}

\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/14_nanobanana_scenes_landscape/studio.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/14_nanobanana_scenes_landscape/retro_car_bridge.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/14_nanobanana_scenes_landscape/spiral_staircase.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/14_nanobanana_scenes_landscape/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} NanoBanana Landscape (14) -- korrektes Format}

\caption{Phase 3a: GPT-1.5 mit Ratio-Bug (oben, quadratisch), NanoBanana korrekt (unten). \href{https://jennifer-meier.github.io/everything-machine/\#images}{Bild-Galerie}}
\end{figure}
```

```{=latex}
\begin{table}[H]
\centering\small
\caption{Phase 3a: Signature Scenes v1}
\begin{tabularx}{\textwidth}{llll>{\raggedright\arraybackslash}X}
\toprule
\textbf{Modell} & \textbf{Format} & \textbf{Bew.} & \textbf{Halluz.} & \textbf{Kommentar} \\
\midrule
GPT-1.5 & portrait \textcolor{evalred}{(sq.)} & gemischt & -- & Buggy 1:1 Ratio \\
GPT-1.5 & landscape \textcolor{evalred}{(sq.)} & gemischt & -- & Auch 1:1 leider \\
NanoBanana & portrait & gemischt & teilweise & Halb cool, halb Halluz. \\
NanoBanana & landscape & gemischt & teilweise & Ohne Halluz. stark \\
\bottomrule
\end{tabularx}
\end{table}
```

```{=latex}
\clearpage
```

#### Phase 3b: Gestretchte Inputs

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/inputs/kepler-posed-portrait.jpg}\hfill
\includegraphics[width=0.27\textwidth]{experiments/fal-pipeline/inputs/kepler-posed-landscape.jpg}
\\[1pt]{\scriptsize\color{darktext!60} Gestretchte Inputs: Portrait (links), Landscape (rechts)}
\caption{Phase 3b: Fehlerhafte Referenzbilder (gestretcht statt gepaddet)}
\end{figure}
```

```{=latex}
\begin{table}[H]
\centering\small
\caption{Phase 3b: Gestretchte Inputs}
\begin{tabularx}{\textwidth}{lllll>{\raggedright\arraybackslash}X}
\toprule
\textbf{Ordner} & \textbf{Modell} & \textbf{Format} & \textbf{Bew.} & \textbf{Halluz.} & \textbf{Kommentar} \\
\midrule
15/16 & GPT-1.5 & portrait & gemischt & -- & Gestretchte Referenz \\
15/16 & GPT-1.5 & landscape & gemischt & teilweise & Stretching + Cap fehlt \\
15/16 & NanoBanana & portrait & gemischt & \textcolor{evalgreen}{nein} & Stretching, keine Halluz. \\
15/16 & NanoBanana & landscape & gemischt & teilweise & Weniger Stretching, gut \\
\midrule
17/18 & GPT-1.5 & portrait & gemischt & teilweise & 1:1 + leichte Halluz. \\
17/18 & GPT-1.5 & landscape & gemischt & teilweise & Dasselbe \\
17/18 & NanoBanana & portrait & gemischt & -- & -- \\
17/18 & NanoBanana & landscape & \textcolor{evalgreen}{stark} & -- & -- \\
\bottomrule
\end{tabularx}
\end{table}
```

Der Ratio-Bug wurde behoben, Tokyo Rain ersetzte Bridge. Doch ein neuer Automatisierungsfehler trat auf: Das quadratische Referenzbild wurde naiv auf Portrait- bzw. Landscape-Format skaliert statt korrekt gepaddet -- Kepler erschien verzerrt. Die Outputs zeigen deutlich sichtbare Proportionsverzerrungen: ein zu schmaler Körper im Portrait-Format, ein zu breiter im Landscape-Format. Trotzdem lieferte NanoBanana Pro selbst mit verzerrtem Input überzeugende Voxel-Ästhetik -- ein Hinweis auf die Robustheit des Modells.

In der zweiten Iteration (Ordner 17/18) wurden die Prompts verfeinert: Voxel-Treppen statt Marmor, präzisere Szenenbeschreibungen. Das Stretching blieb jedoch bestehen, da der Fehler in der Input-Vorbereitung lag, nicht im Prompting. GPT-Image-1.5 produzierte erneut quadratische Outputs (1024×1024) trotz Portrait-Anfrage -- derselbe API-Bug wie in Phase 3a. NanoBanana Pro hingegen lieferte korrekte Formate und die stärksten Landscape-Ergebnisse der gesamten Pipeline. Die Phasen 3a--3b zeigen Schöns [-@schoen1983practitioner] "Situation, die zurückspricht" im Zeitraffer: Jede Iteration löste ein Problem und offenbarte das nächste. Die Bewertung erfolgte in diesen Phasen noch pauschal pro Modell und Format, da die Outputs insgesamt zu fehlerbehaftet waren, um sinnvoll zwischen einzelnen Szenen zu differenzieren.

```{=latex}
\clearpage
```

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.15\textwidth]{experiments/fal-pipeline/outputs/15_gpt15_fixed_portrait/studio.jpg}\hfill
\includegraphics[width=0.15\textwidth]{experiments/fal-pipeline/outputs/15_gpt15_fixed_portrait/tokyo_rain.jpg}\hfill
\includegraphics[width=0.15\textwidth]{experiments/fal-pipeline/outputs/15_gpt15_fixed_portrait/spiral_staircase.jpg}\hfill
\includegraphics[width=0.15\textwidth]{experiments/fal-pipeline/outputs/15_gpt15_fixed_portrait/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} GPT-1.5 Portrait (15)}

\vspace{4pt}

\includegraphics[width=0.15\textwidth]{experiments/fal-pipeline/outputs/16_nanobanana_fixed_portrait/studio.jpg}\hfill
\includegraphics[width=0.15\textwidth]{experiments/fal-pipeline/outputs/16_nanobanana_fixed_portrait/tokyo_rain.jpg}\hfill
\includegraphics[width=0.15\textwidth]{experiments/fal-pipeline/outputs/16_nanobanana_fixed_portrait/spiral_staircase.jpg}\hfill
\includegraphics[width=0.15\textwidth]{experiments/fal-pipeline/outputs/16_nanobanana_fixed_portrait/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} NanoBanana Portrait (16)}

\vspace{6pt}

\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/17_gpt15_v2_portrait/studio.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/17_gpt15_v2_portrait/tokyo_rain.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/17_gpt15_v2_portrait/spiral_staircase.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/17_gpt15_v2_portrait/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} GPT-1.5 Portrait (17)}

\vspace{4pt}

\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/18_nanobanana_v2_landscape/studio.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/18_nanobanana_v2_landscape/tokyo_rain.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/18_nanobanana_v2_landscape/spiral_staircase.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/18_nanobanana_v2_landscape/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} NanoBanana Landscape (18)}

\caption{Phase 3b: Outputs mit gestretchten Referenzbildern. \href{https://jennifer-meier.github.io/everything-machine/\#images}{Bild-Galerie}}
\end{figure}
```

```{=latex}
\clearpage
```

#### Phase 3c: Korrigierte Pipeline

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/inputs/kepler-posed-portrait-padded.jpg}\hfill
\includegraphics[width=0.27\textwidth]{experiments/fal-pipeline/inputs/kepler-posed-landscape-padded.jpg}
\\[1pt]{\scriptsize\color{darktext!60} Korrekt gepaddete Inputs: Portrait (links), Landscape (rechts)}
\caption{Phase 3c: Korrekt gepaddete Referenzbilder}
\end{figure}
```

```{=latex}
\begin{table}[H]
\centering\small
\caption{Phase 3c: Korrigierte Pipeline}
\begin{tabularx}{\textwidth}{llll>{\raggedright\arraybackslash}X}
\toprule
\textbf{Modell} & \textbf{Format} & \textbf{Bew.} & \textbf{Halluz.} & \textbf{Kommentar} \\
\midrule
GPT-1.5 & portrait & gemischt & -- & -- \\
GPT-1.5 & landscape & gemischt & -- & -- \\
NanoBanana & portrait & gemischt & -- & -- \\
NanoBanana & landscape & \textcolor{evalgreen}{stark} & -- & -- \\
\bottomrule
\end{tabularx}
\end{table}
```

Mit korrekt gepaddeten Inputs -- schwarze Balken statt Stretching -- lieferte die Pipeline erstmals konsistente Ergebnisse. Night Drive ersetzte Tokyo Rain als dritte Szene, die Szenen-Auswahl stabilisierte sich auf das finale Set: Night Drive, Spiral Staircase, Pool Floaty und Studio. Die finalen Prompts waren nun hochspezifisch (siehe Prompt-Verzeichnis).

Der Unterschied war unmittelbar sichtbar: Keplers Proportionen stimmten, die Voxel-Geometrie blieb erhalten, und beide Modelle produzierten erstmals Outputs, die ohne Einschränkung als Promo-Material verwendbar wären. NanoBanana Pro dominierte im Landscape-Format mit durchgehend starken Bewertungen, während GPT-Image-1.5 im Portrait-Format atmosphärischere Szenen erzeugte. Die Korrektur eines einzigen Pipeline-Parameters -- Padding statt Stretching -- machte den Unterschied zwischen unbrauchbaren und überzeugenden Ergebnissen. Ab dieser Phase wurde jede Szene einzeln bewertet, da die Qualität nun hoch genug war, um szenenbezogene Unterschiede sinnvoll zu differenzieren.

```{=latex}
\clearpage
```

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/19_gpt15_final_portrait/night_drive.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/19_gpt15_final_portrait/spiral_staircase.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/19_gpt15_final_portrait/pool_floaty.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/19_gpt15_final_portrait/studio.jpg}
\\[1pt]{\scriptsize\color{darktext!60} GPT-1.5 Portrait (19)}

\vspace{4pt}

\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/20_nanobanana_final_portrait/night_drive.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/20_nanobanana_final_portrait/spiral_staircase.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/20_nanobanana_final_portrait/pool_floaty.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/20_nanobanana_final_portrait/studio.jpg}
\\[1pt]{\scriptsize\color{darktext!60} NanoBanana Portrait (20)}

\vspace{4pt}

\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/19_gpt15_final_landscape/night_drive.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/19_gpt15_final_landscape/spiral_staircase.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/19_gpt15_final_landscape/pool_floaty.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/19_gpt15_final_landscape/studio.jpg}
\\[1pt]{\scriptsize\color{darktext!60} GPT-1.5 Landscape (19)}

\vspace{4pt}

\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/20_nanobanana_final_landscape/night_drive.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/20_nanobanana_final_landscape/spiral_staircase.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/20_nanobanana_final_landscape/pool_floaty.jpg}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/outputs/20_nanobanana_final_landscape/studio.jpg}
\\[1pt]{\scriptsize\color{darktext!60} NanoBanana Landscape (20)}

\caption{Phase 3c: Outputs mit korrekt gepaddeten Inputs. \href{https://jennifer-meier.github.io/everything-machine/\#images}{Bild-Galerie}}
\end{figure}
```

```{=latex}
\clearpage
```

#### Phase 3d: Posed vs. A-Pose Vergleich

Dieselben drei Signature Scenes -- Night Drive, Spiral Staircase, Pool Floaty -- wurden mit Posed (Ordner 21/22) und A-Pose (Ordner 23/24) Input parallel generiert.

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/inputs/kepler-posed-portrait-padded.jpg}\hfill
{\Large\color{accentgreen}$\rightarrow$}\hfill
\includegraphics[width=0.22\textwidth]{experiments/fal-pipeline/inputs/kepler-a-pose-portrait-padded.jpg}
\caption{Input-Vergleich Phase 3d: Posed (links) vs. A-Pose (rechts)}
\end{figure}
```

Das Ergebnis war eindeutig: Posed Input war A-Pose in fast allen Szenen überlegen. GPT-Image-1.5 produzierte die atmosphärischsten Ergebnisse, halluzinierte aber häufiger Details. NanoBanana Pro war konsistenter, aber weniger ausdrucksstark.

```{=latex}
\begin{table}[H]
\centering\footnotesize
\caption{Phase 3d: Posed vs. A-Pose Vergleich (detailliert)}
\begin{tabularx}{\textwidth}{llllll>{\raggedright\arraybackslash}X}
\toprule
\textbf{Ordner} & \textbf{Modell} & \textbf{Input} & \textbf{Format} & \textbf{Szene} & \textbf{Bew.} & \textbf{Halluz.} \\
\midrule
21 & GPT-1.5 & posed & portrait & night\_drive & \textcolor{evalgreen}{ja} & \textcolor{evalred}{ja} \\
21 & GPT-1.5 & posed & portrait & staircase & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} \\
21 & GPT-1.5 & posed & portrait & pool & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} \\
21 & GPT-1.5 & posed & landscape & night\_drive & \textcolor{evalgreen}{ja} & \textcolor{evalred}{ja} \\
21 & GPT-1.5 & posed & landscape & staircase & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} \\
21 & GPT-1.5 & posed & landscape & pool & neutral & \textcolor{evalred}{ja} \\
\midrule
22 & NanoBanana & posed & portrait & night\_drive & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} \\
22 & NanoBanana & posed & portrait & staircase & \textcolor{evalred}{nein} & \textcolor{evalgreen}{nein} \\
22 & NanoBanana & posed & portrait & pool & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} \\
22 & NanoBanana & posed & landscape & night\_drive & \textcolor{evalgreen}{ja} & \textcolor{evalred}{ja} \\
22 & NanoBanana & posed & landscape & staircase & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} \\
22 & NanoBanana & posed & landscape & pool & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} \\
\midrule
23 & GPT-1.5 & a-pose & portrait & night\_drive & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} \\
23 & GPT-1.5 & a-pose & portrait & staircase & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} \\
23 & GPT-1.5 & a-pose & portrait & pool & neutral & \textcolor{evalred}{ja} \\
23 & GPT-1.5 & a-pose & landscape & night\_drive & \textcolor{evalgreen}{ja} & \textcolor{evalred}{ja} \\
23 & GPT-1.5 & a-pose & landscape & staircase & \textcolor{evalred}{nein} & \textcolor{evalgreen}{nein} \\
23 & GPT-1.5 & a-pose & landscape & pool & \textcolor{evalgreen}{ja} & \textcolor{evalred}{ja} \\
\midrule
24 & NanoBanana & a-pose & portrait & night\_drive & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} \\
24 & NanoBanana & a-pose & portrait & staircase & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} \\
24 & NanoBanana & a-pose & portrait & pool & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} \\
24 & NanoBanana & a-pose & landscape & night\_drive & neutral & \textcolor{evalred}{ja} \\
24 & NanoBanana & a-pose & landscape & staircase & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} \\
24 & NanoBanana & a-pose & landscape & pool & neutral & \textcolor{evalred}{ja} \\
\bottomrule
\end{tabularx}
\end{table}

\clearpage
```

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/21_gpt15_refined_portrait/night_drive.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/21_gpt15_refined_portrait/spiral_staircase.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/21_gpt15_refined_portrait/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} GPT-1.5 Posed Portrait (21)}

\vspace{3pt}

\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/23_gpt15_apose_portrait/night_drive.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/23_gpt15_apose_portrait/spiral_staircase.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/23_gpt15_apose_portrait/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} GPT-1.5 A-Pose Portrait (23)}

\vspace{3pt}

\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/22_nanobanana_refined_portrait/night_drive.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/22_nanobanana_refined_portrait/spiral_staircase.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/22_nanobanana_refined_portrait/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} NanoBanana Posed Portrait (22)}

\vspace{3pt}

\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/24_nanobanana_apose_portrait/night_drive.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/24_nanobanana_apose_portrait/spiral_staircase.jpg}\hfill
\includegraphics[width=0.18\textwidth]{experiments/fal-pipeline/outputs/24_nanobanana_apose_portrait/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} NanoBanana A-Pose Portrait (24)}

\caption{Phase 3d: Portrait-Vergleich -- Posed (21/22) vs. A-Pose (23/24). \href{https://jennifer-meier.github.io/everything-machine/\#images}{Bild-Galerie}}
\end{figure}
```

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/21_gpt15_refined_landscape/night_drive.jpg}\hfill
\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/21_gpt15_refined_landscape/spiral_staircase.jpg}\hfill
\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/21_gpt15_refined_landscape/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} GPT-1.5 Posed Landscape (21)}

\vspace{3pt}

\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/23_gpt15_apose_landscape/night_drive.jpg}\hfill
\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/23_gpt15_apose_landscape/spiral_staircase.jpg}\hfill
\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/23_gpt15_apose_landscape/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} GPT-1.5 A-Pose Landscape (23)}

\vspace{3pt}

\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/22_nanobanana_refined_landscape/night_drive.jpg}\hfill
\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/22_nanobanana_refined_landscape/spiral_staircase.jpg}\hfill
\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/22_nanobanana_refined_landscape/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} NanoBanana Posed Landscape (22)}

\vspace{3pt}

\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/24_nanobanana_apose_landscape/night_drive.jpg}\hfill
\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/24_nanobanana_apose_landscape/spiral_staircase.jpg}\hfill
\includegraphics[width=0.28\textwidth]{experiments/fal-pipeline/outputs/24_nanobanana_apose_landscape/pool_floaty.jpg}
\\[1pt]{\scriptsize\color{darktext!60} NanoBanana A-Pose Landscape (24)}

\caption{Phase 3d: Landscape-Vergleich -- Posed (21/22) vs. A-Pose (23/24). \href{https://jennifer-meier.github.io/everything-machine/\#images}{Bild-Galerie}}
\end{figure}
```

```{=latex}
\clearpage
```

#### Gesamtbewertung

Die folgende Tabelle fasst alle 52 Einzelbewertungen aus der Pipeline zusammen. Die verwendeten Prompts sind im Prompt-Verzeichnis nach der Tabelle dokumentiert.

```{=latex}
{\footnotesize
\begin{longtable}{lllllllp{3cm}}
\caption{Gesamtbewertung: Alle Evaluationen der fal.ai-Pipeline} \\
\toprule
\textbf{Nr.} & \textbf{Modell} & \textbf{Input} & \textbf{Format} & \textbf{Bew.} & \textbf{Halluz.} & \textbf{Kommentar} \\
\midrule
\endfirsthead
\toprule
\textbf{Nr.} & \textbf{Modell} & \textbf{Input} & \textbf{Format} & \textbf{Bew.} & \textbf{Halluz.} & \textbf{Kommentar} \\
\midrule
\endhead
\bottomrule
\endfoot
01 & MiniMax & a-pose & sq. & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & Minecraft-Stil, Gesichtszüge \\
02 & Z-Image & a-pose & sq. & bedingt & \textcolor{evalgreen}{nein} & A-Pose erhalten, clean \\
03 & FLUX Depth & a-pose & sq. & \textcolor{evalred}{nein} & -- & Körper humanoid geglättet \\
04 & FLUX Canny & a-pose & sq. & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & Volles Gesicht halluziniert \\
05 & Era3D & a-pose & sq. & \textcolor{evalred}{nein} & -- & Nutzlos, eigene Renders besser \\
\midrule
06 & FLUX Kontext & a-pose & sq. & bedingt & -- & Wird besser \\
07 & GPT-1.5 & a-pose & sq. & bedingt & teilweise & Solide, leichte Halluz. \\
08 & SeedDream & a-pose & sq. & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & Volles Gesicht halluziniert \\
09 & NanoBanana & a-pose & sq. & \textcolor{evalgreen}{gut} & teilweise & Beste Phase-2-Ergebnisse \\
\midrule
10 & FLUX Kont. & posed & sq. & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & Gesichter halluziniert \\
11 & GPT-1.5 & posed & sq. & \textcolor{evalgreen}{ja} & teilweise & Solideste Ergebnisse \\
12 & NanoBanana & posed & sq. & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} & Stärkste Voxel-Ästhetik \\
\midrule
13 & GPT-1.5 & posed & portrait \textcolor{evalred}{(sq.)} & gemischt & teilweise & 1:1 Ratio-Bug \\
13 & GPT-1.5 & posed & landsc. \textcolor{evalred}{(sq.)} & gemischt & teilweise & Auch 1:1 \\
14 & NanoBanana & posed & portrait \textcolor{evalred}{(sq.)} & gemischt & \textcolor{evalred}{ja} & Halb cool, halb Halluz. \\
14 & NanoBanana & posed & landsc. \textcolor{evalred}{(sq.)} & gemischt & \textcolor{evalgreen}{nein} & Ohne Halluz. stark \\
\midrule
15 & GPT-1.5 & posed & portrait & gemischt & teilweise & Gestretchte Referenz \\
15 & GPT-1.5 & posed & landsc. & gemischt & \textcolor{evalred}{ja} & Stretching + Cap fehlt \\
16 & NanoBanana & posed & portrait & gemischt & \textcolor{evalgreen}{nein} & Stretching, keine Halluz. \\
16 & NanoBanana & posed & landsc. & gemischt & \textcolor{evalgreen}{nein} & Weniger Stretching \\
\midrule
17 & GPT-1.5 & posed & portrait \textcolor{evalred}{(sq.)} & gemischt & \textcolor{evalred}{ja} & 1:1 Bug + Halluz. \\
17 & GPT-1.5 & posed & landsc. \textcolor{evalred}{(sq.)} & gemischt & \textcolor{evalred}{ja} & Dasselbe \\
18 & NanoBanana & posed & portrait & gemischt & \textcolor{evalgreen}{nein} & -- \\
18 & NanoBanana & posed & landsc. & \textcolor{evalgreen}{stark} & \textcolor{evalgreen}{nein} & -- \\
\midrule
19 & GPT-1.5 & posed & portrait & gemischt & teilweise & -- \\
19 & GPT-1.5 & posed & landsc. & gemischt & teilweise & -- \\
20 & NanoBanana & posed & portrait & gemischt & \textcolor{evalgreen}{nein} & -- \\
20 & NanoBanana & posed & landsc. & \textcolor{evalgreen}{stark} & \textcolor{evalgreen}{nein} & -- \\
\midrule
21 & GPT-1.5 & posed & portrait & \textcolor{evalgreen}{ja} & \textcolor{evalred}{ja} & ND: Scheibe fehlt \\
21 & GPT-1.5 & posed & portrait & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} & SS \\
21 & GPT-1.5 & posed & portrait & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} & PF \\
21 & GPT-1.5 & posed & landsc. & \textcolor{evalgreen}{ja} & \textcolor{evalred}{ja} & ND: Teil d. Autos fehlt \\
21 & GPT-1.5 & posed & landsc. & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} & SS \\
21 & GPT-1.5 & posed & landsc. & neutral & \textcolor{evalred}{ja} & PF: Cap/Haare fehlen \\
\midrule
22 & NanoBanana & posed & portrait & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} & ND \\
22 & NanoBanana & posed & portrait & \textcolor{evalred}{nein} & \textcolor{evalgreen}{nein} & SS: Stufen nicht schön \\
22 & NanoBanana & posed & portrait & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} & PF: Sehr cool \\
22 & NanoBanana & posed & landsc. & \textcolor{evalgreen}{ja} & \textcolor{evalred}{ja} & ND: Cockpit falsch \\
22 & NanoBanana & posed & landsc. & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & SS: Doppelte Treppe \\
22 & NanoBanana & posed & landsc. & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} & PF: Transparent, gefällt \\
\midrule
23 & GPT-1.5 & a-pose & portrait & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & ND: Scheinwerfer falsch \\
23 & GPT-1.5 & a-pose & portrait & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & SS: A-Pose overfitted \\
23 & GPT-1.5 & a-pose & portrait & neutral & \textcolor{evalred}{ja} & PF: Cap fehlt \\
23 & GPT-1.5 & a-pose & landsc. & \textcolor{evalgreen}{ja} & \textcolor{evalred}{ja} & ND: Cap fehlt \\
23 & GPT-1.5 & a-pose & landsc. & \textcolor{evalred}{nein} & \textcolor{evalgreen}{nein} & SS: Pose zu starr \\
23 & GPT-1.5 & a-pose & landsc. & \textcolor{evalgreen}{ja} & \textcolor{evalred}{ja} & PF: Pool Floaty falsch \\
\midrule
24 & NanoBanana & a-pose & portrait & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} & ND \\
24 & NanoBanana & a-pose & portrait & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & SS: Treppe nicht schön \\
24 & NanoBanana & a-pose & portrait & \textcolor{evalgreen}{ja} & \textcolor{evalgreen}{nein} & PF: Super \\
24 & NanoBanana & a-pose & landsc. & neutral & \textcolor{evalred}{ja} & ND: Halluz. stören \\
24 & NanoBanana & a-pose & landsc. & \textcolor{evalred}{nein} & \textcolor{evalred}{ja} & SS: Treppen nicht schön \\
24 & NanoBanana & a-pose & landsc. & neutral & \textcolor{evalred}{ja} & PF: Pool Floaty falsch \\
\end{longtable}
}
```

#### Prompt-Verzeichnis

Die folgende Übersicht dokumentiert alle in der Pipeline verwendeten Prompts, gruppiert nach Phase. Ab Phase 3b wurden für GPT-Image-1.5 und NanoBanana Pro unterschiedliche Prompt-Varianten verwendet -- GPT erhielt strukturierte Prompts (Background/Center/Details/Constraints), NanoBanana natürlichsprachliche. Hier ist jeweils die NanoBanana-Variante dokumentiert; die GPT-Variante beschrieb dieselbe Szene in strukturierter Form.

```{=latex}
{\scriptsize

\textbf{Phase 1 -- Modell-Screening} (alle Modelle, identischer Prompt)\\[2pt]
\textit{Base:} ``A voxel character made of small 3D cubes, faceless geometric humanoid figure, white shirt and dark pants, standing in a dramatic cinematic environment, volumetric lighting, no face, blocky pixel art style 3D character''\\
\textit{+ Szenen:} ``...in a neon-lit cyberpunk city at night'' / ``...in a foggy forest with golden light rays'' / ``...on a concert stage with dramatic spotlights''

\vspace{6pt}

\textbf{Phase 2 -- Top-Modelle in Szenen} (alle Modelle, identischer Prompt)\\[2pt]
\textit{Cyberpunk:} ``Place this voxel character in a neon-lit cyberpunk city at night, walking down the street with hands in pockets, cinematic lighting''\\
\textit{Forest:} ``...in a foggy forest clearing, sitting on a fallen tree, golden light rays filtering through the canopy''\\
\textit{Concert:} ``...on a concert stage, performing with arms raised, dramatic spotlights and fog machine effects''

\vspace{6pt}

\textbf{Phase 2b -- Posed-Input-Test} (5 Szenen, identischer Prompt)\\[2pt]
\textit{Cyberpunk:} ``Place this voxel character in a neon-lit cyberpunk city at night, walking down a rain-soaked street with hands in pockets, cinematic lighting, reflections on wet ground''\\
\textit{Park:} ``...sitting on a park bench in autumn, golden leaves falling around him, soft warm afternoon light''\\
\textit{Concert:} ``...on a dark concert stage, performing with a microphone, dramatic red and blue spotlights, fog machine, crowd silhouettes''\\
\textit{Rooftop:} ``...standing on a rooftop at sunset, looking over a vast city skyline, wind blowing, golden hour lighting''\\
\textit{Studio:} ``...in a recording studio, sitting at a mixing desk with headphones around neck, warm ambient lighting, monitors glowing''

\vspace{6pt}

\textbf{Phase 3a -- Signature Scenes v1} (GPT + NanoBanana, identischer Prompt)\\[2pt]
\textit{Studio:} ``Place this voxel character in a professional recording studio, sitting at a large mixing console with both hands on the faders, studio monitors glowing, headphones on, warm amber lighting [...]''\\
\textit{Retro Car:} ``...driving a vintage 1970s convertible car across a long suspension bridge at night, city lights reflecting on the water below [...]''\\
\textit{Spiral Staircase:} ``...walking up an endless spiral staircase that extends infinitely into the sky, passing through layers of clouds and stars, surreal dreamlike atmosphere, the staircase is white marble [...]''\\
\textit{Pool Floaty:} ``...lying on a pink flamingo pool float in a turquoise swimming pool, seen from directly above as a top-down bird's eye view [...]''

\vspace{6pt}

\textbf{Phase 3b -- Fixed Scenes} (separate GPT/NB-Prompts, hier NB)\\[2pt]
\textit{Studio:} ``Show this voxel character in a cozy recording studio. He's sitting at a big mixing desk with his hands on the faders, wearing headphones. Warm amber lighting [...] IMPORTANT: The character must remain completely faceless [...]''\\
\textit{Tokyo Rain:} ``This voxel character is walking through a rainy Tokyo alley at night. Neon signs everywhere in Japanese, steam rising from street vents [...] IMPORTANT: The character must remain completely faceless [...]''\\
\textit{Spiral Staircase:} ``...walks up an endless spiral staircase made of white marble, floating through deep space. Stars and galaxies surround the staircase [...] IMPORTANT: The character must remain completely faceless [...]''\\
\textit{Pool Floaty:} ``Top-down bird's eye view of a turquoise swimming pool. This voxel character is lying on an inflatable pool ring (donut shape with a hole in the middle) [...] IMPORTANT: The character must remain completely faceless [...]''

\vspace{6pt}

\textbf{Phase 3c -- Final Scenes} (hier NB-Variante)\\[2pt]
\textit{Studio:} wie Phase 3b\\
\textit{Night Drive} (neu, ersetzt Tokyo): ``This voxel character is driving a vintage 1970s convertible down a long empty road at night. A big full moon and stars fill the dark sky [...] IMPORTANT: The character must remain completely faceless [...]''\\
\textit{Spiral Staircase} (update): ``...walks up an endless spiral staircase [...] The staircase is built from the same voxel cubes as the character --- blocky geometric steps that glow with soft blue light. [...] NOT marble, NOT stone.''\\
\textit{Pool Floaty:} wie Phase 3b, erweitert um Poolside-Details (Liegen, Cocktails, Pflanzen)

\vspace{6pt}

\textbf{Phase 3d -- Refined + A-Pose-Vergleich} (hier NB-Variante)\\[2pt]
\textit{Night Drive} (refined): ``This voxel character is cruising down a night road in a sleek retro 1980s sports car with pop-up headlights. Behind him a glowing city skyline fades into the distance. Ahead, dark mountains rise on the horizon. [...] Retro synthwave vibes with teal and magenta tones. IMPORTANT: The character must remain completely faceless [...]''\\
\textit{Spiral Staircase} (refined): ``...walks up an endless spiral staircase floating through a dreamy cloudy sky. The sky is soft pastel blue and lavender with layered clouds [...] NOT intense galaxies, just a calm dreamy twilight atmosphere. [...] blocky geometric steps that glow with soft blue neon light. [...]''\\
\textit{Pool Floaty} (enriched): ``Top-down bird's eye view of a turquoise swimming pool at a luxurious summer resort. [...] Around the pool edge: white sun loungers, a small table with a cocktail and sunscreen, tropical potted plants, neatly folded towels, flip-flops on the tiles. [...]''

}
```

```{=latex}
\clearpage
```

#### Zusammenfassung und theoretische Einordnung

Theoretisch markiert dieses Experiment eine Verschiebung auf Deterdings [-@deterding2017mixed] Spektrum: Meine Rolle war nicht mehr die der Experimentierenden, die direkt mit einem Tool interagiert, sondern die einer Orchestratorin -- ich definierte das "Was" und "Warum", während Claude Code das "Wie" implementierte. Schöns [-@schoen1983practitioner] Reflection-in-Action fand im Zeitraffer statt: Wo ich in Experiment 1 stundenlang an ComfyUI-Parametern drehte, durchlief die Pipeline denselben explorativen Prozess in Minuten. Galanters [-@galanter2003generative] Konzept des systematischen Mappings eines generativen Raums wurde hier buchstäblich umgesetzt -- sieben Phasen, die den Möglichkeitsraum zwischen neun Modellen, zwei Input-Typen und drei Szenen systematisch absteckten.

Das Fazit war ambivalent. Einerseits gelang hier zum ersten Mal eine visuell überzeugende Kepler-Generierung ohne Fine-Tuning -- die besten Bilder aus den Posed-Phasen waren die ersten, die ich mir als Album-Cover vorstellen konnte. Andererseits blieben die Halluzinationen: fehlende Caps, falsche Cockpit-Details, gelegentlich angedeutete Gesichtszüge unter der Maske. Die Pipeline machte den Prozess skalierbar, aber nicht kontrollierbar. Und eine neue Frage drängte sich auf: Wenn ich nicht mehr selbst prompte, sondern einen KI-Agenten beauftrage, der für mich promptet -- wo endet dann meine Autorschaft?

### Experiment 6: Video-Generierung (fal.ai API + Claude Code)

Die automatisierte Bildpipeline aus Experiment 5 warf eine naheliegende Frage auf: Wenn statische Bilder von Kepler überzeugend gelingen -- lässt sich derselbe Ansatz auf Bewegtbild übertragen? Image-to-Video-Modelle versprechen, aus Einzelbildern kurze Clips zu generieren. Doch wo Bildgenerierung mit Halluzinationen kämpft, potenziert Video die Herausforderung: Jedes halluzinierte Detail muss über mehrere Sekunden konsistent bleiben.

#### Setup und Methodik

Sieben Modelle wurden systematisch verglichen: PixVerse v5.5, LTX-2, Wan 2.6, Seedance 1.0 Pro, Veo 3.1, Kling O3 und Kling 3.0 V3. Die Kosten reichten von \$0.20 (PixVerse) bis \$0.84 (Kling) pro Video. Als Testbilder dienten vier Szenen aus den besten Ergebnissen der Bildpipeline -- zwei bewusst unterschiedliche Herausforderungen:

- **Studio** (Landscape, 1376×768): Kepler am Mischpult -- kontrollierte Innenszene, wenig Bewegung
- **Pool** (Portrait, 768×1376): Kepler auf dem Pool-Ring, Vogelperspektive -- Wasser, ungewöhnlicher Blickwinkel
- **Night Drive** (Portrait, 768×1376): Kepler im Retro-Auto auf Wüstenhighway -- Nachtszene, Fahrtbewegung
- **Spiral Staircase** (Portrait, 768×1376): Kepler auf kosmischer Wendeltreppe -- Prompt forderte blaues Leuchten statt Marmor

Die Prompts waren bewusst einfach gehalten: kurze Bewegungsbeschreibung plus "Camera holds still." (siehe Ergebnisse). Jedes Modell erhielt identische Inputs. Insgesamt entstanden 28 Videos (7 Modelle × 4 Szenen) bei geschätzten Gesamtkosten von ca. \$16.

```{=latex}
\newpage
\begin{figure}[H]
\centering
\begin{minipage}[t]{0.47\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/pixverse_v55_studio}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/pixverse_v55_studio.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}PixVerse v5.5}
\end{minipage}\hfill
\begin{minipage}[t]{0.47\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/ltx2_studio}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/ltx2_studio.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}LTX-2}
\end{minipage}
\vspace{6pt}
\begin{minipage}[t]{0.47\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/wan_v26_studio}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/wan_v26_studio.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Wan 2.6}
\end{minipage}\hfill
\begin{minipage}[t]{0.47\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/seedance_pro_studio}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/seedance_pro_studio.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Seedance Pro}
\end{minipage}
\vspace{6pt}
\begin{minipage}[t]{0.47\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/veo31_studio}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/veo31_studio.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Veo 3.1}
\end{minipage}\hfill
\begin{minipage}[t]{0.47\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/kling_o3_studio}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/kling_o3_studio.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Kling O3}
\end{minipage}
\vspace{6pt}
\begin{minipage}[t]{0.47\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/kling_v3_studio}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/kling_v3_studio.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Kling 3.0 V3}
\end{minipage}
\caption{Mittlere Frames, Studio-Szene (Landscape, 7 Modelle). Verlinkt auf die \href{https://jennifer-meier.github.io/everything-machine/\#generations}{Video-Galerie}.}
\end{figure}

\vspace{-4pt}
{\scriptsize
\begin{tabularx}{\textwidth}{l c c X}
\textbf{Modell} & \textbf{Bew.} & \textbf{Halluz.} & \textbf{Kommentar} \\
\midrule
PixVerse v5.5 & okay & leicht & Kamerabewegung gefällt, aber Bewegung unpassend. Schwarzer Kasten entsteht. \\
LTX-2 & \textcolor{evalgreen}{gut} & leicht & Schwer zu beurteilen ob halluziniert (Audio). \\
Wan 2.6 & \textcolor{evalgreen}{gut} & \textcolor{evalgreen}{nein} & Bild wirkt leicht überzeichnet, Audio wurde trotzdem generiert. \\
Seedance Pro & okay & \textcolor{evalgreen}{nein} & Bewegt sich zwar nicht, aber okay. \\
Veo 3.1 & \textcolor{evalred}{schlecht} & leicht & Slider bewegen sich. Bewegung gefällt nicht. \\
Kling O3 & \textcolor{evalgreen}{gut} & leicht & Audio Meter unscharf. Bewegung gefällt sehr. \\
Kling 3.0 V3 & \textcolor{evalgreen}{gut} & leicht & Audio Meter schwammig. Bewegung ruckartig aber cool. \\
\end{tabularx}
}
```

```{=latex}
\newpage
\begin{figure}[H]
\centering
% Row 1: 3 portrait images
\begin{minipage}[t]{0.26\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/pixverse_v55_pool}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/pixverse_v55_pool.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}PixVerse v5.5}
\end{minipage}\hfill
\begin{minipage}[t]{0.26\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/wan_v26_pool}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/wan_v26_pool.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Wan 2.6}
\end{minipage}\hfill
\begin{minipage}[t]{0.26\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/seedance_pro_pool}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/seedance_pro_pool.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Seedance Pro}
\end{minipage}
\vspace{3pt}
% Row 2: 3 portrait images
\begin{minipage}[t]{0.26\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/veo31_pool}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/veo31_pool.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Veo 3.1}
\end{minipage}\hfill
\begin{minipage}[t]{0.26\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/kling_o3_pool}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/kling_o3_pool.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Kling O3}
\end{minipage}\hfill
\begin{minipage}[t]{0.26\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/kling_v3_pool}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/kling_v3_pool.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Kling 3.0 V3}
\end{minipage}
\vspace{3pt}
% Row 3: LTX-2 landscape (separate — changes aspect ratio)
\begin{minipage}[t]{0.34\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/ltx2_pool}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/ltx2_pool.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}LTX-2 (Landscape-Output)}
\end{minipage}
\caption{Mittlere Frames, Pool-Szene (Portrait, 7 Modelle). Verlinkt auf die \href{https://jennifer-meier.github.io/everything-machine/\#generations}{Video-Galerie}.}
\end{figure}

\vspace{-4pt}
{\scriptsize
\begin{tabularx}{\textwidth}{l c c X}
\textbf{Modell} & \textbf{Bew.} & \textbf{Halluz.} & \textbf{Kommentar} \\
\midrule
PixVerse v5.5 & \textcolor{evalred}{schlecht} & \textcolor{evalred}{stark} & Voxel-Gesicht verändert sich. Bewegung zu schnell. \\
LTX-2 & \textcolor{evalred}{schlecht} & \textcolor{evalred}{stark} & Aspect Ratio geändert, Kamera bewegt sich zu sehr. \\
Wan 2.6 & \textcolor{evalred}{schlecht} & \textcolor{evalred}{stark} & Gesicht entsteht mit der Zeit. Pool-Floaty-Bewegung gelungen. \\
Seedance Pro & \textcolor{evalred}{schlecht} & \textcolor{evalred}{stark} & Gesicht entsteht, Zehen zeichnen sich in Schuhen ab. \\
Veo 3.1 & \textcolor{evalgreen}{gut} & leicht & Voxel-Gesicht verändert sich leicht. Floaty-Bewegung cool. \\
Kling O3 & \textcolor{evalgreen}{gut} & leicht & Ripples an falscher Stelle. Wassersimulation top. \\
Kling 3.0 V3 & \textcolor{evalgreen}{gut} & \textcolor{evalgreen}{nein} & Das beste! \\
\end{tabularx}
}
```

```{=latex}
\newpage
\begin{figure}[H]
\centering
% Row 1: 3 portrait images
\begin{minipage}[t]{0.26\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/pixverse_v55_night_drive}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/pixverse_v55_night_drive.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}PixVerse v5.5}
\end{minipage}\hfill
\begin{minipage}[t]{0.26\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/wan_v26_night_drive}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/wan_v26_night_drive.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Wan 2.6}
\end{minipage}\hfill
\begin{minipage}[t]{0.26\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/seedance_pro_night_drive}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/seedance_pro_night_drive.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Seedance Pro}
\end{minipage}
\vspace{3pt}
% Row 2: 3 portrait images
\begin{minipage}[t]{0.26\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/veo31_night_drive}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/veo31_night_drive.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Veo 3.1}
\end{minipage}\hfill
\begin{minipage}[t]{0.26\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/kling_o3_night_drive}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/kling_o3_night_drive.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Kling O3}
\end{minipage}\hfill
\begin{minipage}[t]{0.26\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/kling_v3_night_drive}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/kling_v3_night_drive.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Kling 3.0 V3}
\end{minipage}
\vspace{3pt}
% Row 3: LTX-2 landscape (separate — changes aspect ratio)
\begin{minipage}[t]{0.34\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/ltx2_night_drive}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/ltx2_night_drive.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}LTX-2 (Landscape-Output)}
\end{minipage}
\caption{Mittlere Frames, Night-Drive-Szene (Portrait, 7 Modelle). Verlinkt auf die \href{https://jennifer-meier.github.io/everything-machine/\#generations}{Video-Galerie}.}
\end{figure}

\vspace{-4pt}
{\scriptsize
\begin{tabularx}{\textwidth}{l c c X}
\textbf{Modell} & \textbf{Bew.} & \textbf{Halluz.} & \textbf{Kommentar} \\
\midrule
PixVerse v5.5 & \textcolor{evalred}{schlecht} & \textcolor{evalred}{stark} & Gesicht wird zu Lego-Figur. Autofahrt unnatürlich. \\
LTX-2 & \textcolor{evalred}{schlecht} & \textcolor{evalred}{stark} & Auto fährt rückwärts, Licht hinten, Aspect Ratio geändert. \\
Wan 2.6 & \textcolor{evalred}{schlecht} & leicht & Gesicht wird dazu generiert, Animation sonst gut. \\
Seedance Pro & \textcolor{evalgreen}{gut} & \textcolor{evalgreen}{nein} & Überraschenderweise gut. \\
Veo 3.1 & okay & leicht & Funktioniert gut, fährt aber rückwärts -- könnte man umkehren. \\
Kling O3 & \textcolor{evalred}{schlecht} & \textcolor{evalred}{stark} & Okay, aber halluziniert am Rand und zoomt zu sehr heraus. \\
Kling 3.0 V3 & okay & leicht & Etwas besser als Kling O3. \\
\end{tabularx}
}
```

```{=latex}
\newpage
\begin{figure}[H]
\centering
% Row 1: 3 portrait images
\begin{minipage}[t]{0.28\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/pixverse_v55_spiral_staircase}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/pixverse_v55_spiral_staircase.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}PixVerse v5.5}
\end{minipage}\hfill
\begin{minipage}[t]{0.28\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/wan_v26_spiral_staircase}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/wan_v26_spiral_staircase.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Wan 2.6}
\end{minipage}\hfill
\begin{minipage}[t]{0.28\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/seedance_pro_spiral_staircase}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/seedance_pro_spiral_staircase.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Seedance Pro}
\end{minipage}
\vspace{6pt}
% Row 2: 3 portrait images
\begin{minipage}[t]{0.28\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/veo31_spiral_staircase}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/veo31_spiral_staircase.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Veo 3.1}
\end{minipage}\hfill
\begin{minipage}[t]{0.28\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/kling_o3_spiral_staircase}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/kling_o3_spiral_staircase.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Kling O3}
\end{minipage}\hfill
\begin{minipage}[t]{0.28\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/kling_v3_spiral_staircase}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/kling_v3_spiral_staircase.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}Kling 3.0 V3}
\end{minipage}
\vspace{6pt}
% Row 3: LTX-2 landscape (separate — changes aspect ratio)
\begin{minipage}[t]{0.38\textwidth}\centering
\href{https://jennifer-meier.github.io/everything-machine/\#video/ltx2_spiral_staircase}{\includegraphics[width=\linewidth]{experiments/fal-pipeline/outputs/video_test_02_frames/ltx2_spiral_staircase.jpg}}\\[1pt]
{\scriptsize\color{darktext!60}LTX-2 (Landscape-Output)}
\end{minipage}
\caption{Mittlere Frames, Spiral-Staircase-Szene (Portrait, 7 Modelle). Verlinkt auf die \href{https://jennifer-meier.github.io/everything-machine/\#generations}{Video-Galerie}.}
\end{figure}

\vspace{-4pt}
{\scriptsize
\begin{tabularx}{\textwidth}{l c c X}
\textbf{Modell} & \textbf{Bew.} & \textbf{Halluz.} & \textbf{Kommentar} \\
\midrule
PixVerse v5.5 & okay & leicht & Stufen etwas unnatürlich, aber interessanter Glow. \\
LTX-2 & \textcolor{evalred}{schlecht} & \textcolor{evalred}{stark} & Er läuft fast von der Stufe, Aspect Ratio ändert sich. \\
Wan 2.6 & okay & leicht & Bewegung leicht unnatürlich. \\
Seedance Pro & okay & leicht & Kopf verändert sich. Treppenanimation und Glow in Ordnung. \\
Veo 3.1 & okay & leicht & Er überspringt Stufen, Animation wirkt aber relativ okay. \\
Kling O3 & \textcolor{evalgreen}{gut} & leicht & Eine Stufe funktioniert nicht, aber Bewegung okay. Leuchten gefällt. \\
Kling 3.0 V3 & \textcolor{evalred}{schlecht} & leicht & Stufen funktionieren nicht, Leuchten komisch, Kamerabewegung unerwartet. \\
\end{tabularx}
}
```

#### Ergebnisse

```{=latex}
{\footnotesize
\begin{longtable}{p{2.8cm}p{1.5cm}p{1.5cm}p{1.5cm}p{1.5cm}p{1.2cm}p{0.8cm}p{0.8cm}}
\textbf{Modell} & \textbf{Studio} & \textbf{Pool} & \textbf{Night Dr.} & \textbf{Staircase} & \textbf{Kosten} & \textbf{Gut} & \textbf{Schl.} \\
\midrule
\endhead
Kling O3 & \textcolor{evalgreen}{gut} & \textcolor{evalgreen}{gut} & \textcolor{evalred}{schlecht} & \textcolor{evalgreen}{gut} & \$0.84 & 3 & 1 \\
Kling 3.0 V3 & \textcolor{evalgreen}{gut} & \textcolor{evalgreen}{gut} & okay & \textcolor{evalred}{schlecht} & \$0.84 & 2 & 1 \\
Veo 3.1 & \textcolor{evalred}{schlecht} & \textcolor{evalgreen}{gut} & okay & okay & \$0.80 & 1 & 1 \\
Seedance Pro & okay & \textcolor{evalred}{schlecht} & \textcolor{evalgreen}{gut} & okay & \$0.62 & 1 & 1 \\
Wan 2.6 & \textcolor{evalgreen}{gut} & \textcolor{evalred}{schlecht} & \textcolor{evalred}{schlecht} & okay & \$0.50 & 1 & 2 \\
PixVerse v5.5 & okay & \textcolor{evalred}{schlecht} & \textcolor{evalred}{schlecht} & okay & \$0.20 & 0 & 2 \\
LTX-2 & \textcolor{evalgreen}{gut} & \textcolor{evalred}{schlecht} & \textcolor{evalred}{schlecht} & \textcolor{evalred}{schlecht} & \$0.36 & 1 & 3 \\
\end{longtable}
}
```

#### Analyse und Reflexion

Die Ergebnisse zeigen ein klares Muster: **Preis korreliert mit Qualität, aber nicht linear.** Kling O3 (\$0.84) war mit drei von vier guten Ergebnissen der zuverlässigste Kandidat. LTX-2 (\$0.36) scheiterte an drei von vier Szenen, primär durch ein technisches Problem -- das Modell erzwingt ein 16:9-Seitenverhältnis und beschneidet Portrait-Inputs.

Das auffälligste Phänomen war die **Gesichts-Halluzination bei Portrait-Szenen**. Keplers bewusst gesichtsloser Voxel-Kopf wurde von mehreren Modellen (Wan, Seedance, PixVerse) mit realistischen Gesichtszügen versehen -- ein Problem, das bei der Landscape-Studio-Szene nicht auftrat. Die Modelle scheinen auf menschliche Gesichter als Default trainiert zu sein und können die bewusste Abwesenheit eines Gesichts nicht beibehalten. Dieses Phänomen spiegelt die Erfahrung aus Experiment 1 wider: Auch ComfyUI halluzinierte Gesichter in Keplers Maske. Hámošová und Rusnák [-@hamosova2023troublinggan] zeigen in ihrem Projekt *TroublingGAN*, dass das Scheitern generativer Modelle ästhetisch produktiv sein kann -- visuelle Ambiguität als bewusstes Gestaltungsmittel statt als Fehler. Keplers Gesichts-Halluzinationen sind ein konkreter Fall dieser Spannung: Was das Modell als Defizit behandelt (die Abwesenheit eines Gesichts), ist für die Künstleridentität konstitutiv.

Überraschend war die **Inkonsistenz innerhalb einzelner Modelle**. Seedance Pro war bei Studio und Pool schlecht bis mittelmäßig, lieferte aber beim Night Drive das überzeugendste Ergebnis aller Modelle -- ein Befund, der gegen simple Rankings spricht. Veo 3.1 scheiterte beim Studio, glänzte aber beim Pool. Diese Szenenabhängigkeit zeigt, dass kein Modell universal überlegen ist -- die Wahl muss pro Szene getroffen werden.

Methodisch erweiterte dieses Experiment die Orchestrator-Rolle aus Experiment 5: Dieselbe Pipeline, dasselbe Interview-basierte Evaluationsformat, nun auf Video angewandt. Die Bewertungskriterien -- "Gefällt mir", "Halluzination", "Kommentar" -- erwiesen sich als robust über Medientypen hinweg. Die zentrale Erkenntnis für die Praxis: Video-Generierung mit Kepler ist möglich, aber nur mit den teuersten Modellen zuverlässig. Der kreative Prozess bleibt ein iteratives Auswählen aus einem unvorhersehbaren Möglichkeitsraum -- Galanters [-@galanter2003generative] generativer Ansatz, nun in Bewegtbild übersetzt.

## Zentrale Beobachtungen aus dem Prozess

Aus der vergleichenden Analyse der Journal-Einträge und der systematischen Reflexion nach dem autoethnografischen Modell [@ellis2011autoethnography] lassen sich vier wiederkehrende Muster identifizieren, die beschreiben, wie KI meinen kreativen Prozess verändert hat. Sie waren nicht vorab geplant, sondern sind durch die Praxis selbst hervorgebracht worden.

### 1. Unvorhersehbarer Flow

Flow entstand dort, wo ich ihn nicht geplant hatte, und blieb aus, wo ich ihn erwartet hatte. Der Website-Build mit Cursor funktionierte überraschend produktiv -- „Oh mein Gott, das war einfach sehr krass! Das hat das Aufsetzen der Website einfach tausendfach schneller gemacht", notierte ich im Journal (Eintrag 4). Die KI übernahm repetitive Aufgaben, während ich die ästhetische Vision steuerte. Umgekehrt scheiterte die Bildgenerierung für Kepler trotz intensiver Bemühungen: ComfyUI halluzinierte Gesichter in Keplers Maske -- das Modell konnte die Abwesenheit eines Gesichts nicht akzeptieren, ein konkreter Fall des Uncanny Valley [@mori2012uncanny]. Suno produzierte zu kommerzielle Ergebnisse, weil das Modell auf Mainstream-Ästhetik trainiert ist. Die Erkenntnis: KI-gestützte Kreativität ist nicht planbar. Flow entstand dort, wo die Interaktion tatsächlich "mixed-initiative" [@deterding2017mixed] war — beim Website-Build mit engem Feedback-Loop, in dem beide Seiten beitrugen. Er blieb aus, wo die Interaktion einseitig wurde — bei Suno beschrieb ich, die KI generierte, ohne echte Rückkopplung. Die produktivsten Momente entstanden in Domänen und Konstellationen, die ich vorher nicht als Kernbereich identifiziert hatte.

### 2. Speed vs. Control

KI beschleunigt und begrenzt den kreativen Prozess gleichzeitig. Exploration und Prototyping werden drastisch schneller -- beim Website-Build, bei der Generierung von Marble-Welten, im KI-Dialog als Lernwerkzeug. Aber die Kontrolle über ästhetische Details geht verloren. „Prompt rein, Ergebnis in Sekunden. Aber genau diese Geschwindigkeit hat auch gezeigt, wie wenig Kontrolle ich über das Ergebnis hatte", reflektierte ich nach dem Suno-Experiment (Eintrag 6). Das Suno-Experiment illustriert das: Das Modell generiert zu jedem Track eine detaillierte Beschreibung -- "bitcrushed chiptune pads over a sparse, detuned synth choir" -- die exakt das trifft, was ich mir vorstellte. Der tatsächliche Sound ging in eine andere Richtung: zu poliert, zu kommerziell. Bodens [-@boden2004creative] Konzept der explorativen Kreativität hilft hier: Das Modell erkundet den konzeptuellen Raum von "sowjetisch-dystopischer Pixel-Musik" auf der Beschreibungsebene adäquat, scheitert aber an der Übersetzung in klangliche Materie. Die Diskrepanz zwischen Beschreibung und Output ist ein konkretes Symptom des Speed-vs-Control-Tradeoffs: Generierung ist schnell, aber Feinsteuerung ist nicht gegeben. Die automatisierte Pipeline aus Experiment 5 illustriert beide Seiten: 24 evaluierbare Bilder entstanden in Minuten, aber Details wie Keplers Cap oder die Cockpit-Perspektive blieben unkontrollierbar.

### 3. Verschiebung der Autorschaft

Über die Experimente hinweg verschob sich meine Rolle ständig. Beim Referenzen-Sammeln war ich Kuratorin, ein rein menschlicher Akt. Bei ComfyUI war ich Lernende und Experimentierende, orientiert am Workflow einer anderen Person. Beim Website-Build war ich Dirigentin: „Ich fühlte mich wie ein Manager mit Gesamtvision, der einen Junior Developer anleitet. Irgendwann wurde es eher Kollaboration, wenn wir zusammen nicht weiterkamen" (Eintrag 4). Bei Suno war ich enttäuschte Kuratorin, die nur auswählen, nicht gestalten konnte. Im KI-Dialog war ich die Fragende.

Die wechselnden Rollen lassen sich als Wanderung auf Deterdings [-@deterding2017mixed] Spektrum lesen — mal näher am "Mensch als Schöpfer" (Referenzen sammeln), mal in der Mixed-Initiative-Zone (Website-Build), mal näher am "Computer als Schöpfer" (Suno). Diese Rollenvielfalt ist nicht Unschärfe, sondern Qualität. Ellis, Adams und Bochner [-@ellis2011autoethnography] beschreiben autoethnografische Forschung als Methode, die persönliche Erfahrung mit kultureller Analyse verbindet. Die wechselnden Rollen -- Kuratorin, Dirigentin, Kollaborateurin, Lernende -- sind Ausdruck einer Autorschaft, die sich fundamental verschoben hat: nicht mehr alleinige Urheberschaft, nicht vollständige Delegation. Domänenwissen erweist sich erneut als Voraussetzung für produktive Kollaboration. Wer nicht weiß, was gut ist, kann nicht kuratieren. In Experiment 5 kam eine weitere Rolle hinzu: die der Orchestratorin, die nicht mehr direkt promptet, sondern einen KI-Agenten beauftragt, der seinerseits Bildmodelle steuert -- eine dreistufige Kette, die die Frage nach der Autorschaft weiter verkompliziert.

### 4. KI-Burnout und KI-Enthusiasmus

Die emotionale Dimension der KI-Arbeit erwies sich als eigenständige Prozessveränderung, die ich nicht erwartet hatte. Es gibt einen Zyklus: Begeisterung, wenn etwas unerwartet gut funktioniert -- der Website-Build, die ersten Marble-Welten, ein Claude-Dialog, der mich wirklich weiterbringt. Und dann Frustration und Erschöpfung, wie nach dem ComfyUI-Experiment: „Ich wollte ja genau durch die Verwendung von KI neue Möglichkeiten schaffen, die intuitiv sind und Spaß machen. Aber es sind halt keine magischen Tools, so wie es sich anfühlt" (Eintrag 2).

Dieses Pendeln ist nicht Nebensache, sondern reale Belastung im kreativen Prozess. Der ständige Zwang, neue Tools zu evaluieren, Workflows umzubauen, mit Limitierungen zu kämpfen, kostet kreative Energie, die eigentlich in die Kunst fließen sollte. Man muss sich aktiv davor schützen, in diesem Zyklus aufgerieben zu werden. Die Versprechen der Technologie, schneller, besser, alles möglich, stehen in Spannung zur Realität einer Praxis, die oft mühsamer ist als die analoge Alternative. Der systematische Pipeline-Ansatz in Experiment 5 wirkte dem entgegen: Sieben strukturierte Phasen mit klaren Evaluationskriterien reduzierten die Frustration gegenüber den Einzelversuchen erheblich.

## Rückbezug auf die Forschungsfrage

Am Ausgangspunkt dieser Arbeit stand eine praktische Frage: Kann generative KI die visuelle Konsistenz liefern, die Kepler braucht? Die Antwort ist: nicht zuverlässig. Bildgenerierungsmodelle scheitern an Keplers Nischen-Ästhetik — sie halluzinieren Gesichter in seine Maske, driften in Mainstream-Ästhetiken ab, und die Kontrolle über Details bleibt begrenzt. Aber genau dieses Scheitern wurde produktiv: Es offenbarte, wie fundamental sich der kreative Prozess durch die Kollaboration mit KI verändert — und damit die zweite, tiefere Frage der Einleitung: Was passiert, wenn ich nicht mehr nur Werkzeuge benutze, sondern mit ihnen zusammenarbeite?

Die zentrale Forschungsfrage — wie verändert der Einsatz multimodaler KI-Systeme den kreativen Prozess bei der Entwicklung einer digitalen Künstleridentität? — lässt sich anhand der vier Beobachtungen und der fünf Subfragen beantworten, die die strukturierten Reflexionsinterviews geleitet haben:

**Wie verändert sich der Workflow?** KI-Tools verschieben den kreativen Prozess von der linearen Ausführung zur iterativen Navigation. Flow entsteht unvorhersehbar (Beobachtung 1), und die Geschwindigkeit der Generierung steht in permanenter Spannung zur fehlenden Kontrolle über Details (Beobachtung 2). Der Workflow wird nicht einfach schneller — er wird anders: explorativer, weniger planbar, abhängiger von der Fähigkeit, Ergebnisse zu kuratieren statt zu produzieren.

**Wie verschiebt sich die Autorschaft?** Von der alleinigen Urheberschaft zu einem Spektrum wechselnder Rollen — Kuratorin, Dirigentin, Lernende, Orchestratorin. Domänenwissen, nicht KI-Kompetenz, erweist sich als entscheidende Voraussetzung (Beobachtung 3). Wer nicht weiß, was gut ist, kann nicht kuratieren.

**Welche Rolle spielt Iteration?** Iteration ist nicht Optimierung, sondern Erkenntnismethode. Jeder gescheiterte Prompt, jede unerwartete Halluzination wurde zum Ausgangspunkt für reflektierte Anpassung — Schöns [-@schoen1983practitioner] „Situation, die zurückspricht" in digitaler Form. Die automatisierte Pipeline in Experiment 5 zeigt, dass systematische Iteration den explorativen Raum erweitert, ohne die zentrale Spannung zwischen Kontrolle und Generierung aufzulösen.

**Wie wird mit Scheitern umgegangen?** Scheitern ist Dauerzustand und produktive Kraft zugleich. Der emotionale Zyklus zwischen Enthusiasmus und Burnout (Beobachtung 4) zeigt, dass der Umgang mit Scheitern nicht nur eine technische, sondern eine psychologische Herausforderung ist. ComfyUI scheiterte an Keplers Gesicht, Suno an seiner Klangwelt — aber beide Erfahrungen schärften das Verständnis dafür, wo die Grenzen aktueller Modelle liegen und wie man mit ihnen arbeiten kann.

**Wie entwickelt sich die Ästhetik im Prozess?** Die Ästhetik entsteht nicht trotz, sondern durch die Einschränkungen der KI. Keplers Nischen-Ästhetik ließ sich nicht direkt generieren, aber die Auseinandersetzung mit den Grenzen der Modelle — Halluzinationen, Mainstream-Drift, fehlende Feinsteuerung — schärfte das ästhetische Urteil und führte zur bewussten Integration von „Fehlern" als Gestaltungsmittel. In Galanters [-@galanter2003generative] Terminologie: Die Suche nach „effektiver Komplexität" wurde zum ästhetischen Kompass.

Diese Veränderungen sind nicht linear und nicht planbar; sie entstehen im iterativen Prozess und kosten mehr Energie, als die Versprechen der Technologie vermuten lassen. Die folgende Diskussion ordnet diese Befunde theoretisch ein.

# Diskussion und Interpretation

## Zusammenfassung der Ergebnisse

Die vorliegende Arbeit ging der Frage nach, wie der Einsatz multimodaler KI-Systeme den kreativen Prozess bei der Entwicklung des virtuellen Alter Egos Kepler verändert. Die Practice-Led Research, dokumentiert über sechs Experimente mit unterschiedlichen KI-Tools, identifiziert vier zentrale Prozessveränderungen.

Erstens entsteht *Flow unvorhersehbar*: Der Website-Build gelang produktiv, die Bildgenerierung scheiterte an Keplers Nischen-Ästhetik; Phänomene wie Face Hallucination und Uncanny Valley [@mori2012uncanny] erwiesen sich dabei als konkrete Hindernisse. Zweitens zeigt sich ein durchgängiger *Speed-vs-Control-Tradeoff*: KI beschleunigt Exploration und Prototyping, aber die Kontrolle über ästhetische Details geht verloren; das Modell "versteht" Nischen sprachlich, kann sie aber medial nicht umsetzen. Drittens hat sich *meine Rolle fundamental verschoben*: von der Ausführenden zur Kuratorin, Dirigentin, Lernenden, wobei Domänenwissen sich als entscheidende Voraussetzung erwies, nicht KI-Kompetenz. Viertens erweist sich der *emotionale Zyklus zwischen KI-Enthusiasmus und KI-Burnout* als eigenständige Prozessveränderung: Der ständige Zwang, neue Tools zu evaluieren und mit Limitierungen zu kämpfen, kostet kreative Energie.

Diese vier Beobachtungen sind keine isolierten Phänomene. Sie verbindet ein gemeinsames Prinzip: Die produktivsten Momente entstanden dort, wo Intention und KI-Eigenlogik in Spannung zueinander traten, nicht wo sie sich deckten. Experiment 5 belegt zudem die Skalierbarkeit des Ansatzes: Eine automatisierte Pipeline kann den explorativen Raum systematisch abstecken, ohne dass die zentrale Spannung zwischen Kontrolle und Generierung aufgelöst wird.

## Theoretische Implikationen

Die Ergebnisse legen nahe, dass bestehende Kreativitätstheorien im Kontext der Mensch-KI-Kollaboration neu betrachtet werden sollten. Boden [-@boden2004creative] unterscheidet kombinatorische, explorative und transformative Kreativität. Meine Praxis zeigt, dass generative KI primär als Katalysator für *explorative* Kreativität fungiert: Die Systeme eröffnen einen konzeptuellen Raum, den ich als Künstlerin navigiere, kuratiere und bewerte. Transformative Kreativität -- das Sprengen der Regeln eines konzeptuellen Raums -- ging hingegen durchgehend von meinen Entscheidungen aus, nicht von den Modellen. Die KI generiert Variationen; die Künstlerin entscheidet, welche Variation die Grenzen verschiebt. Der unvorhersehbare Flow, den ich beschreibe, ist letztlich eine Konsequenz dieser Asymmetrie: Exploration ist schnell, aber Transformation erfordert menschliches Urteil.

Galanter [-@galanter2003generative] zeigt, dass generative Kunst als Methode verstanden werden muss — es geht um das *Wie* der Produktion, nicht um das *Was* des Ergebnisses. Diese Perspektive verschiebt die Bewertung: Die Frage ist nicht, ob KI-generierte Bilder "authentisch" sind, sondern wie sich der kreative Prozess verändert, wenn ein autonomes System beteiligt ist. Der Speed-vs-Control-Tradeoff lässt sich als Navigation auf Galanters Ordnung-Chaos-Skala beschreiben: KI-Tools beschleunigen die Exploration des konzeptuellen Raums, aber die Kontrolle über die Zone effektiver Komplexität — das ästhetisch Interessante — bleibt beim Menschen.

Borgdorff [-@borgdorff2012conflict] argumentiert, dass künstlerische Forschung Wissen freilegt, das sich nur durch die Praxis selbst zeigt. Das bestätigt sich hier konkret: Mein Vorwissen über Keplers Ästhetik -- die dystopische Klangwelt, die voxelisierte Maskierung, die Spannung zwischen Lo-Fi und Hyperdigitalem -- ließ sich als Prompt-Anweisung an KI-Systeme nur begrenzt übertragen. Ohne Domänenwissen produziert die Kollaboration generische Ergebnisse — das bestätigt den in Abschnitt 2 eingeführten Zusammenhang zwischen Expertise und Outputqualität. Dieses Wissen zeigte sich erst *im* iterativen Prozess, nicht vor ihm.

Besonders aufschlussreich ist die Verbindung zu Schön [-@schoen1983practitioner]: Reflection-in-Action, das spontane Reagieren auf unerwartete Situationen in der Praxis, beschreibt präzise den Modus, in dem ich auf KI-Halluzinationen, unerwartete Outputs und produktive Fehler reagierte. Das Scheitern eines Prompts war kein Abbruchkriterium, sondern Auslöser für reflektierte Anpassung. Diese Beobachtung erweitert Schöns Konzept um eine neue Dimension: In der Mensch-KI-Kollaboration ist die "Situation, die zurückspricht" kein physisches Material, sondern ein probabilistisches System mit eigener Handlungslogik. Der emotionale Zyklus zwischen Enthusiasmus und Burnout lässt sich als Konsequenz dieser permanenten Reflection-in-Action lesen: Die Situation spricht ständig zurück, und das kostet Kraft.

Deterding et al. [-@deterding2017mixed] fragen, wie Mixed-Initiative Creative Interfaces "upskilling without deskilling" ermöglichen können. Diese Frage resoniert mit meiner vierten Beobachtung: Der KI-Burnout-Zyklus ist möglicherweise ein Symptom dafür, dass aktuelle KI-Tools die Mixed-Initiative-Balance noch nicht gefunden haben — sie sind entweder zu autonom (Suno: keine Eingriffsmöglichkeit) oder zu abhängig von Expertenwissen (ComfyUI: hohe technische Hürde). Die produktivsten Momente meiner Forschung entstanden dort, wo die Balance gelang: beim Website-Build, wo die KI repetitive Aufgaben übernahm und ich die ästhetische Vision steuerte.

## Praktische Implikationen

Für Künstler\*innen und Medienproduzent\*innen, die generative KI in ihre Praxis integrieren wollen, ergeben sich aus dieser Arbeit konkrete Erkenntnisse. Die wichtigste: Domänenwissen ist keine optionale Zugabe, sondern Voraussetzung für ästhetisch relevante Ergebnisse. Wer ohne klare ästhetische Vision promptet, erhält den kleinsten gemeinsamen Nenner, die Mainstream-Ästhetik, auf die Generalist-Modelle trainiert sind. Keplers Nischen-Ästhetik ließ sich nur dort realisieren, wo ich spezifisches Vokabular, präzise Referenzen und ein geschultes Urteilsvermögen einbrachte.

Darüber hinaus zeigt sich ein durchgängiger Speed-versus-Control-Trade-off: KI-Tools beschleunigen die Produktion erheblich, reduzieren aber gleichzeitig die Kontrolle über ästhetische Details. Für die Medienproduktion bedeutet das, dass KI-Werkzeuge sich besonders für Ideation, Prototyping und Exploration eignen, während die finale ästhetische Entscheidung bei der Künstlerin verbleiben muss. Die Rolle verschiebt sich von der Ausführenden zur Kuratorin, eine Kompetenz, die in der Ausbildung von Medienproduzent\*innen künftig stärker adressiert werden sollte.

## Stärken und Limitierungen

### Stärken

Die methodische Kombination aus Practice-Led Research und Autoethnografie ermöglichte eine Dokumentationstiefe, die rein empirische Ansätze nicht erreichen. Durch die Veröffentlichung des gesamten Prozesses auf der Everything-Machine-Website stelle ich eine Transparenz her, die in künstlerischer Forschung selten ist: Jedes Experiment, jede Reflexion, jeder Fehlschlag ist nachvollziehbar. Die multimodale Perspektive -- Bild, Audio, Code, Text -- bildet zudem die Komplexität zeitgenössischer Medienproduktion ab, anstatt sie auf ein einzelnes Medium zu reduzieren.

### Limitierungen

Als autoethnografische Einzelfallstudie ist die Generalisierbarkeit der Ergebnisse eingeschränkt. Was für meine spezifische Praxis mit Kepler gilt, muss für andere künstlerische Kontexte nicht zutreffen. Die subjektive Perspektive, die in der Artistic Research als Stärke gilt [@ellis2011autoethnography], bleibt in anderen Forschungsparadigmen eine methodische Schwäche. Eine weitere Limitierung liegt im technologischen Wandel: Die Tools, mit denen ich gearbeitet habe, werden sich schneller weiterentwickeln als akademische Publikationszyklen erlauben. Die Ergebnisse beschreiben den Stand einer Technologie in Bewegung. Schließlich muss eine Meta-Ebene benannt werden: Der Schreibprozess dieser Arbeit selbst wurde durch KI-Assistenz unterstützt, eine Verschränkung, die ich als konsequente Fortsetzung meiner Methodik verstehe, die aber offengelegt werden muss.

### Practice-Based Intention, Practice-Led Realität

Ein ehrlicher Rückblick muss eine Verschiebung benennen, die sich erst im Laufe der Arbeit zeigte. Zu Beginn war das Projekt als practice-based intendiert: Die Artefakte -- Keplers generierte Bilder, die Website, die Musik -- sollten selbst Teil des Forschungsergebnisses sein. Im Verlauf hat sich die Arbeit aber als practice-led erwiesen. Der eigentliche Beitrag sind die vier Beobachtungen über Prozessveränderungen, nicht die Artefakte. Die generierten Bilder und Clips sind Lernartefakte, die den Weg dokumentieren, nicht "Kunst" im Sinne eines eigenständigen Werks.

Paradoxerweise war die Website das Artefakt mit dem meisten Flow -- obwohl als Dokumentationstool konzipiert, wurde sie zum vielleicht künstlerischsten Element des Projekts. Die KI-generierten Bilder hingegen fühlen sich wie Zwischenergebnisse an: ästhetisch teils interessant, aber nicht "meine Kunst". Die Unsicherheit, ob das hier Kunst oder Technikerprobung ist, ist selbst eine Erkenntnis -- sie spiegelt das Spannungsfeld, in dem sich viele Kreative befinden, die zum ersten Mal mit generativer KI arbeiten.

Nebenbei entstand ein wiederverwendbarer Workflow: Die Kombination aus Claude Code als Orchestrator und der fal.ai API als Modell-Backend erwies sich als reproduzierbare Methode für systematisches Modell-Screening. Dieser methodische Beitrag war nicht geplant, entspricht aber dem, was Frayling [-@frayling1993research] als "research for art" beschreibt -- Forschung, die Werkzeuge und Methoden für die künstlerische Praxis bereitstellt.

## Ausblick

Die Arbeit wirft Fragen auf, die über ihren Rahmen hinausgehen. Wie verändert sich die Kollaboration, wenn KI-Modelle präziser und kontrollierbarer werden? Wird der Speed-vs-Control-Tradeoff sich auflösen, wenn Modelle Nischen-Ästhetiken besser umsetzen können? Und vor allem: Wie nachhaltig ist kreatives Arbeiten mit KI, wenn der Burnout-Zyklus anhält, wenn Tools sich schneller ändern als man sie lernen kann?

Für Kepler als Projekt sehe ich die Arbeit als Fundament, nicht als Abschluss. Das Alter Ego existiert nun in einem dokumentierten Prozessraum, der weiter bespielt werden kann, mit zukünftigen Tools, in anderen Medien, mit neuen Kollaborationsmodellen. Die Forschungsfrage bleibt dabei offen, weil die Technologie, auf die sie sich bezieht, selbst in Bewegung ist. Artistic Research, die sich mit generativer KI beschäftigt, muss diesen Zustand der Vorläufigkeit nicht als Schwäche begreifen, sondern als methodische Grundbedingung akzeptieren.

# Literaturverzeichnis

::: {#refs}
:::
