---
name: reflection-interview
triggers: ["/reflection", "/interview", "Reflexion schreiben", "reflection interview"]
description: Interactive interview for journal entry reflections. Covers all 5 research sub-questions (Workflow, Autorschaft, Iteration, Scheitern, Ästhetik) aligned with the main research question.
last_validated: "2026-02-12"
---

# Reflection Interview Skill

## Trigger

Use when writing or rewriting reflection sections for journal entries in the Everything Machine project.

## Research Context

**Hauptfrage:** Wie verändert der Einsatz multimodaler KI-Systeme (Text, Bild, Audio) den kreativen Prozess bei der Entwicklung einer digitalen Künstleridentität?

**Unterfragen:**
1. Workflow — Welche neuen Arbeitsschritte entstehen? Welche fallen weg?
2. Autorschaft — Wer ist Autor:in? Wie verschiebt sich meine Rolle?
3. Iteration — Wie beeinflusst die Unmittelbarkeit von KI-Output meinen Prozess?
4. Scheitern — Was lerne ich aus fehlgeschlagenen Experimenten?
5. Ästhetik — Entwickelt sich eine eigene visuelle Sprache?

## Interview Process

### Phase 1: Kontext

Ask using `AskUserQuestion`:
- **Tools:** "Welche Tools hast du in dieser Session verwendet?" (Freitext)
- **Intention:** "Was wolltest du erreichen?"

### Phase 2: Die 5 Unterfragen

Use `AskUserQuestion` with multiSelect where appropriate:

**1. Workflow**
```
Frage: "Hat sich dein Arbeitsablauf verändert? Was war neu, was ist weggefallen?"
Header: "Workflow"
Options:
- "Neue Schritte entstanden" + description field
- "Schritte weggefallen" + description field
- "Ähnlich wie vorher"
- "Komplett anders"
```

**2. Autorschaft**
```
Frage: "Wie hast du deine Rolle in diesem Prozess erlebt?"
Header: "Autorschaft"
Options:
- "Ich war Regisseur:in" — KI hat ausgeführt
- "Kollaboration" — Ping-Pong zwischen mir und KI
- "KI hat geführt" — Ich habe reagiert
- "Kurator:in" — Ich habe ausgewählt
```

**3. Iteration**
```
Frage: "Wie hat die schnelle KI-Ausgabe deinen Prozess beeinflusst?"
Header: "Iteration"
Options:
- "Mehr Experimente" — Ich habe mehr ausprobiert
- "Weniger Planung" — Direkter ins Machen
- "Überwältigend" — Zu viele Optionen
- "Kein Unterschied"
```

**4. Scheitern**
```
Frage: "Was ist schiefgelaufen und was hast du daraus gelernt?"
Header: "Scheitern"
(Freitext empfohlen — oder Option "Nichts ist gescheitert")
```

**5. Ästhetik**
```
Frage: "Hat sich durch die Arbeit eine eigene visuelle/stilistische Sprache entwickelt?"
Header: "Ästhetik"
Options:
- "Ja, deutlich" — Beschreibe es
- "Ansatzweise"
- "Nein, eher generisch"
- "Nicht relevant für diese Session"
```

### Phase 3: Generierte Frage

Based on the journal entry content, generate ONE contextual question that:
- Is specific to what happened in this session
- Probes deeper into an interesting aspect
- Cannot be answered with yes/no

Example: "Du hast erwähnt, dass ComfyUI abstürzte — hat das Warten deine Idee verändert?"

### Phase 4: Output

Generate the reflection section with THREE parts:

1. **Bullet-Point Summary** — 5-6 Stichpunkte mit Aspekt-Labels, je max. 1 kurzer Satz
2. **Keywords** — 3-5 Hashtags
3. **Interview-Transkript** — HTML chat format with all Q&A from Phases 1-3

**NO** Kontext/Forschungsfragen/Synthese sections — the bullets replace those.

## Example Output

```markdown
## Reflexion

- **Tools:** ComfyUI lokal, M1 MacBook — aufwendige Installation
- **Workflow:** neuer Workflow, Ergebnisse inkonsistent
- **Autorschaft:** Lernende — an fremdem Netzwerk orientiert
- **Scheitern:** Gesichter in Keplers Maske halluziniert, negative Prompts helfen nicht
- **Erkenntnis:** keine magischen Tools — Art Directability fehlt noch
- **Offene Frage:** eigenes Modell trainieren oder anderen Workflow?

**Keywords:** #ComfyUI #Frustration #Kepler #ArtDirectability

<div class="interview-transcript">
<div class="chat-message claude">
  <div class="chat-avatar"><img src="/assets/icons/claude.svg" alt="Claude"></div>
  <div class="chat-bubble"><p>Welche Tools hast du verwendet?</p></div>
</div>
<div class="chat-message user">
  <div class="chat-avatar"><img src="/assets/icons/user.png" alt="User"></div>
  <div class="chat-bubble"><p>ComfyUI mit einem Network von Mickmumpitz.</p></div>
</div>
<!-- ... all Q&A from interview ... -->
</div>
```

## Notes

- Always conduct the interview before writing — don't assume
- Keep bullet labels from: Tools, Workflow, Autorschaft, Iteration, Scheitern, Ästhetik, Erkenntnis, Offene Frage
- Pick 5-6 most relevant labels per entry — not all are required every time
- Each bullet max. 1 short sentence — no flowing text
- Include 3-5 relevant keywords
- Interview transcript includes ALL questions and answers from Phases 1-3
