# Everything Machine (Kepler)

MA thesis artistic research website — generative AI, digital identity, music production.

## What This Is
Static website (GitHub Pages) + academic thesis. Two workstreams:
- **Website**: Vanilla JS, ES6 modules, EventBus architecture
- **Thesis**: MA Artistic Research paper with literature review

## Commands
```bash
python3 -m http.server 8001              # Website dev
node scripts/generate-journal-manifest.js # Update journal
cd thesis/submission && make all          # Thesis PDFs
```

## Structure
```
/              # Website (js/, journal/, content/)
thesis/        # MA thesis (academic/, submission/, ROADMAP.md)
```

## Skills
| Skill | Trigger | Purpose |
|-------|---------|---------|
| `/website` | js, component, viewer | Website dev, architecture |
| `/thesis` | academic, literature | Thesis writing, lit review |
| `/reflection-interview` | Reflexion schreiben | Journal reflection based on 5 research sub-questions |

## Guardrails
- **Language**: German for thesis, English for code
- **Citations**: Never invent — state if source not found
- **Large PDFs**: Use `thesis/academic/texts/extracted/*.txt`

## When To Read More
- **Website**: `.claude/skills/website/skill.md`
- **Thesis**: `.claude/skills/thesis/skill.md`
- **Architecture**: `.claude/references/architecture.md`
