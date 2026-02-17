# Encoding Culture

**Authors:** Torres Núñez del Prado, Paola (with Martin Seipel and Måns Helldin)
**Source:** PARSE Journal, University of Gothenburg, 2025
**DOI:** https://doi.org/10.70733/l7k5bnrxu4f2
**URL:** https://parsejournal.com/article/encoding-culture/
**Institutional context:** Critical AI Working Group (KAIA), Stockholm University of the Arts (SKH)

---

## Extraction Notes

Full text not directly accessible — this summary is based on:
1. WebFetch on the PARSE Journal article page (multiple passes)
2. WebSearch results returning the article's own abstract/description text
3. KAIA project listing at Stockholm University of the Arts
4. Author profile pages (Academia.edu, Koyne, Alpaca 2025)

The article appears to be an essay/research article without a paywall, but WebFetch was limited to summaries rather than verbatim text due to copyright restrictions enforced by the AI model rendering the page content.

---

## Paper Summary

### Central Argument

"Encoding Culture" argues that the process of curating image datasets for generative AI training mirrors — and thereby reproduces — the mechanisms of cultural canon formation. What appears to be a neutral, technical process of collecting and labeling data is, in fact, a politically and aesthetically loaded act that encodes cultural hierarchies, selection criteria, and power dynamics into AI systems.

The core claim, in the article's own words (as returned by the search index):

> "Putting together cultural data as images and text for generative AI training may replicate the mechanisms of canon formation — both reflecting and reinforcing the underlying systems of cultural selection and valuation."

### What the Paper Is About

The paper is both a critical essay and an account of an ongoing artistic research project. Torres Núñez del Prado leads the KAIA (Kritiska AI-Arbetsgruppen / Critical AI Working Group) at Stockholm University of the Arts, an interdisciplinary hub that runs workshops, reading groups, and research projects examining AI's implications for the arts.

The specific project described fine-tunes **Stable Diffusion 3.5** (an open-source text-to-image model) using a curated dataset of **Swedish visual art historical images** — with the Swedish Cultural Canon as a framing case study. The generated outputs are examined both as artworks and as evidence of what gets encoded (and excluded) when datasets are built from institutionally validated cultural material.

The Swedish Cultural Canon, announced in 2025, is a government-curated list of 100 works, ideas, and cultural artifacts meant to define "Swedishness." This becomes the paper's central provocation: if AI is trained on such a canon, what view of culture does it reproduce? Whose Sweden does it learn?

---

## Methodology

- **Model:** Stable Diffusion 3.5 (open-source, chosen deliberately to allow inspection and modification)
- **Technique:** Fine-tuning on a curated dataset of Swedish art historical images
- **Dataset construction:** Images sourced from institutionally legitimized Swedish visual art history — this curation process is itself the object of critical analysis
- **Framing:** The Swedish Cultural Canon is used as a case study for how canon-formation logic operates
- **Research mode:** Artistic research / practice-led research — the act of building the dataset and generating images is itself the primary method of inquiry
- **Institutional frame:** KAIA working group at Stockholm University of the Arts; collaborative project with Martin Seipel and Måns Helldin

The paper treats the technical pipeline (data collection → labeling → fine-tuning → image generation) as a site of cultural production, not merely as a computational procedure.

---

## Key Findings / Arguments

### 1. Dataset Curation as Canon Formation

The process of selecting images for AI training reproduces the same gatekeeping logic as traditional cultural canons: decisions about what counts as worthy, representative, or aesthetically significant become embedded in the model. The paper calls this "canon-as-model."

### 2. Algorithms Are Not Neutral

Torres Núñez del Prado directly challenges the perception of algorithmic objectivity:

> "Algorithms are not impartial, despite the common perception that they are objective or neutral."
> "Algorithms reflect the values, beliefs and cultural biases of their creators."

Human biases — aesthetic, institutional, national, colonial — enter AI systems through every stage of dataset construction, not just through the model architecture itself.

### 3. Structural Norms Become Embedded

AI models trained on institutionally validated datasets internalize the "structural norms and biases that govern the intended data selection and organisation." These norms are not always visible; they operate below the surface of the output image.

### 4. The Process Is Political, Not Technical

The paper argues that dataset creation should be understood as a political and cultural act. This is especially consequential when models are deployed at scale: algorithmic bias in widely deployed systems affects broad audiences and can reinforce existing inequalities in representation.

### 5. Copyright and Creative Automation

The paper also engages (less centrally) with concerns about copyright in AI training data and the automation of creative processes — both of which the KAIA working group addresses in its broader program.

---

## On Stable Diffusion and Training Data

The choice of Stable Diffusion 3.5 is deliberate: as an open-source model, it allows researchers to inspect its architecture, fine-tune it on custom datasets, and study what the fine-tuning encodes. This is positioned against proprietary black-box systems where the training data is inaccessible to scrutiny.

By training on Swedish art historical images, the project makes visible what would otherwise remain implicit: the model learns a specific visual grammar associated with institutionally approved Swedish culture. The generated images then function as a kind of diagnostic — they show what the model has internalized, and by extension, what the dataset selected and excluded.

The paper does not appear to present systematic quantitative analysis of the outputs, but rather engages with the images as part of artistic research practice — reading them as symptoms of the encoded cultural logic.

---

## On Cultural Bias in AI

The paper's contribution to the cultural bias discourse is framed around **canon formation** rather than the demographic/representation biases more typical in ML research (e.g., facial recognition bias, geographic bias). The argument is:

- Cultural canons are systems of exclusion as much as inclusion
- AI systems trained on canonized datasets inherit these exclusions
- The biases are structural and aesthetic, not merely statistical
- Training data from a single national or institutional tradition produces a model that naturalizes that tradition's assumptions

This connects to broader debates about decolonizing AI — an area Torres Núñez del Prado also addresses in her other work (e.g., the AIELSON project, which investigates Andean khipus and computation outside Western frameworks).

---

## Relation to Other Work / Theoretical Context

- **Canon formation theory** (implicit — the Swedish Cultural Canon as case study)
- **Critical AI / algorithmic accountability** discourse
- **Artistic research methodology** (practice-led, reflective)
- **Decolonial computing** (broader context of Torres Núñez del Prado's practice)
- KAIA functions as an interdisciplinary research hub, linking art practice with critical technology studies

---

## Relevance for "Everything Machine" Thesis

- Directly relevant to the cultural bias dimension of AI-generated identity
- The "canon-as-model" concept is useful: when Kepler is generated via commercial models (fal.ai, Stable Diffusion), those models encode a specific visual culture — largely Western, predominantly trained on English-language internet imagery
- Torres Núñez del Prado's point that dataset creation is a political act reinforces the importance of prompt engineering and model selection as critical (not merely technical) decisions
- The Swedish Canon case study offers a concrete, citable example of how institutional cultural logic enters AI training data
- The open-source / fine-tuning approach (SD 3.5 with custom dataset) contrasts with the proprietary pipeline used in Everything Machine — worth noting as a methodological difference

---

## Citation (APA 7th)

Torres Núñez del Prado, P. (2025). Encoding culture. *PARSE Journal*. https://doi.org/10.70733/l7k5bnrxu4f2
