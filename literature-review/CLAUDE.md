# CLAUDE.md - Artistic Research Literature Review Agent

This file provides guidance to Claude Code when conducting the systematic literature review for Artistic Research methodology.

## Project Overview

**Research Question (German):**
Wie kann das methodologische Prinzip der ‚suspension of disbelief' (Coleridge, 1817) als produktiver Rahmen für Human-AI Collaboration in der künstlerischen Praxis dienen, und welche Implikationen ergeben sich daraus für die Entwicklung einer künstlerischen AI-Methodologie?

**English Translation:**
How can the methodological principle of 'suspension of disbelief' (Coleridge, 1817) serve as a productive framework for Human-AI collaboration in artistic practice, and what implications arise for developing an artistic AI methodology?

**Project:** everything-machine (Kepler PC-based artwork)
**Course:** Master Media Production, TH OWL

## Exploratory Philosophy

This literature review follows a **learning-first** approach:

1. Start with professor-provided texts to understand what Artistic Research *is*
2. Explore the field through searches to see what exists
3. **Discover** appropriate domains based on findings (not prescribed upfront)
4. Adapt citation tier thresholds based on actual citation landscapes
5. Iterate on structure as understanding deepens

**Key principle:** We don't know the AR field yet. Domains and tiers are discovered through exploration, not defined beforehand.

## Phase 1: Required Reading (Professor-Provided)

These texts from `academic/texts/` are **Tier 0** - mandatory inclusion:

| Author | Year | Title | Focus |
|--------|------|-------|-------|
| Borgdorff | 2012 | The Conflict of the Faculties | AR epistemology |
| Frayling | 1993 | Research in Art and Design | Research for/through/into art |
| Ellis | 2010 | Autoethnography | Methodology |
| Henke | 2019 | Manifesto of AR | AR principles |
| Schoen | 1983 | The Reflective Practitioner | Practice-based knowledge |
| Wall | 2006 | Autoethnography | Methodology |
| Wesseling | 2017 | Q&A | AR fundamentals |

**Task:** Read each, summarize key concepts, note relevance to Kepler project.

## Phase 2: Exploratory Searches

**Goal:** Discover what's out there before defining rigid domains.

### Search Queries to Try

```
"artistic research" + methodology
"practice-based research" + digital
"research through practice" + media
"autoethnography" + creative practice
"generative AI" + artistic research
"human-AI collaboration" + art
"suspension of disbelief" + methodology
"creative AI" + practice
```

### AR-Specific Venues (Priority)

| Venue | URL | Type |
|-------|-----|------|
| Research Catalogue | researchcatalogue.net | Expositions |
| JAR | jar-online.net | Journal |
| PARSE | parsejournal.com | Journal |
| VIS | visjournal.nu | Nordic AR |

### Traditional Databases

- Semantic Scholar (`mcp__papers__search_semantic_scholar`)
- OpenAlex (`mcp__science__search_papers`)
- arXiv (for AI/creative practice intersection)

## Phase 3: Domain Discovery

**Domains are TBD** - they will be defined after Phase 1-2 exploration.

Potential clusters to look for:
- AR methodology/epistemology
- Practice-based research methods
- AI in creative/artistic practice
- Autoethnography and reflective practice
- Human-AI collaboration frameworks

**Document what you find** - themes, gaps, citation patterns.

## Citation Tier System

### For Academic Sources (Calibrate After Exploration)

AR is a smaller field than CS/AI. Expect lower citation counts.

| Tier | Criteria | Rule |
|------|----------|------|
| **0** | Professor-provided | MUST include |
| **1** | High citations (TBD) OR landmark book | MUST include |
| **2** | Medium citations (TBD) | Include if relevant |
| **3** | Lower citations | Include if quality venue |
| **4** | Very low/new | Requires justification |

**Thresholds will be calibrated** after seeing actual citation landscape.

### For AR-Specific Venues

JAR, PARSE, VIS, Research Catalogue are different:
- Often practice-based expositions, not traditional papers
- Peer-reviewed but smaller community
- **Judge by relevance to project, not just citations**

Include with format:
```
**[Author (Year)]** - Title
Venue: JAR/PARSE/VIS/RC
Relevance: [Why this matters for Kepler project]
```

## Available MCP Tools

| Tool | Best For |
|------|----------|
| `mcp__papers__search_semantic_scholar` | Academic papers with citations |
| `mcp__science__search_papers` | OpenAlex broad search |
| `mcp__zotero__search_library` | Your existing library |
| Firecrawl (if configured) | AR venue indexing |
| WebFetch | Specific URLs |

## Workflow Files

| File | Purpose |
|------|---------|
| `checkpoint.md` | Session state, progress tracking |
| `todo.md` | Task list |
| `reviews.log` | Critique loop feedback |
| `Skill.md` | Workflow invocation |

## Autonomous Behavior Rules

### Execution
- Use `gh` CLI for GitHub interactions
- Commits follow Conventional Commits: `feat:`, `docs:`, `chore:`, `fix:`
- Update `checkpoint.md` after each session
- Update `todo.md` in real-time

### Search Behavior
- If a search yields no results, pivot keywords and try 3 more times
- Document all search attempts in checkpoint.md
- Note citation counts to help calibrate tier thresholds

### Self-Critique Loop
- For each domain summary, run a critique pass
- Review for: bias, gaps, missing citations, logical coherence
- Log critiques to `reviews.log`
- Revise based on feedback

## Output Targets

**Primary output:** `../submission/docs/02-literaturrecherche.md`
**Bibliography:** `../submission/references/bibliography.bib`
**Build command:** `cd ../submission && make literatur`

## Existing Papers (Starting Points)

Already in bibliography.bib:
- Candy (2006) - Practice Based Research
- Borgdorff (2012) - Conflict of Faculties
- Boden (2004) - Creative Mind
- Banh & Strobel (2023) - Generative AI
- Ellis (2004) - Autoethnography
- Coleridge (1817) - Suspension of Disbelief
- Mori (2012) - Uncanny Valley
