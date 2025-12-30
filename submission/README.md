# Artistic Research Submission Documents

Dark-themed PDF documents for the MA thesis Artistic Research course at TH OWL.

## Title Page Features

- **TH OWL logo** (top-left)
- **MP logo gradient-red** (top-right)
- **Kepler voxel image** (centered above title)
- **Green uppercase title** (website heading style)

## Content Distinction

The documents distinguish between **required structure** and **sample content**:

| Element | Format | How to identify |
|---------|--------|-----------------|
| Structure (from Abgabe.md) | HTML comments | `<!-- [STRUKTUR] ... -->` |
| Sample content (Claude-generated) | Italic with guillemets | `*«Sample text here»*` |

**To use the documents:**
1. Read the `<!-- [STRUKTUR] -->` comments to understand what's required
2. Replace all `*«...»*` italic text with your own content
3. Remove the structure comments when done

## Quick Start

```bash
# Build all documents
make all

# Build individual document
make forschung    # Forschungsfrage
make literatur    # Literaturrecherche
make methodik     # Methodologie
make doku         # Final Documentation
```

## Structure

```
submission/
├── assets/                       # Images for title page
│   ├── kepler-voxel.png          # Kepler pixel-style image
│   ├── th-owl-logo.png           # TH OWL logo
│   └── mp-logo.png               # MP gradient-red logo
├── docs/                         # Markdown source files
│   ├── 01-forschungsfrage.md     # Research questions
│   ├── 02-literaturrecherche.md  # Literature review
│   ├── 03-methodologie.md        # Methodology
│   └── 04-dokumentation.md       # Final paper (~10 pages)
├── references/
│   └── bibliography.bib          # APA bibliography
├── output/                       # Generated PDFs (gitignored)
├── template-dark.tex             # Dark theme LaTeX template
├── Makefile                      # Build automation
└── README.md                     # This file
```

## Requirements

- **LuaLaTeX** (via TeX Live 2025 / MacTeX)
- **Pandoc** 3.x
- **Biber** (for bibliography)

Check installation:
```bash
make check
```

## Workflow

1. **Edit** Markdown files in `docs/`
2. **Add** references to `references/bibliography.bib`
3. **Build** with `make all` or individual targets
4. **Review** PDFs in `output/`

## Document Metadata

All documents use this YAML frontmatter:

```yaml
---
title: "Document Title"
subtitle: "Everything Machine - Artistic Research"
author: "Jennifer Meier"
date: "Month Year"
institute: "Technische Hochschule Ostwestfalen-Lippe"
department: "Fachbereich Medienproduktion, Master Medienproduktion"
course: "Artistic Research"
instructor: "Prof. Dr. Aristotelis Hadjakos"
lang: de-DE
bibliography: references/bibliography.bib  # if citations needed
toc: true                                   # for longer documents
---
```

## Color Scheme

Matches the Everything Machine website:

| Element | Color |
|---------|-------|
| Background | `#111111` |
| Text | `#d1d5db` |
| Accent (headings, links) | `#4ade80` |
| Muted text | `#9ca3af` |

## Citations

Use Pandoc citation syntax in Markdown:

```markdown
According to Boden [-@boden2004creative], creativity involves...

This is supported by recent research [@banh2023generative].
```

Add entries to `references/bibliography.bib` in BibLaTeX format.

## Fonts

The template uses IBM Plex Sans/Mono (falls back to Open Sans if not available).

Install IBM Plex fonts for best results:
```bash
brew install --cask font-ibm-plex
```

## Troubleshooting

**Font not found:**
```bash
# Check available fonts
fc-list | grep -i "ibm plex"
fc-list | grep -i "open sans"
```

**Bibliography not rendering:**
```bash
# Clear aux files and rebuild
make clean && make all
```

**LuaLaTeX error:**
```bash
# Verify installation
which lualatex
lualatex --version
```
