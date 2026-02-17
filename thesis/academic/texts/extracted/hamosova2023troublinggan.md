# TroublingGAN: Generated Visual Ambiguity as a Speculative Alternative to Photojournalism

**Authors:** Lenka Hámošová & Pavol Rusnák
**Source:** Journal for Artistic Research (JAR), Issue 31, 2023
**ISSN:** 2235-0225
**DOI/URL:** https://jar-online.net/en/exposition/abstract/troublinggan-generated-visual-ambiguity-speculative-alternative-photojournalism
**Full exposition:** https://www.researchcatalogue.net/view/1486468/1586300
**Project website:** https://troublinggan.hamosova.com/

---

## What the Paper Is About

TroublingGAN is an artistic research exposition published in JAR that documents a practice-led investigation into generative neural networks and AI-driven visual synthesis. The project centres on a custom-trained StyleGAN model designed to produce intentionally ambiguous, non-photorealistic images representing the concept of "troubling times" — the rapid socio-ecological disruptions caused by shifts in global economic, political, and technological power, including pandemics, armed conflicts, and environmental crises.

The central research questions are:
1. What kind of knowledge do generative neural networks produce?
2. Can a GAN change the researcher's perspective on the subject being studied (i.e., the dataset)?
3. Can generative neural networks function as a viable tool for artistic research?

The exposition argues against the common practice of recontextualising photojournalistic images as stock photos and proposes visually ambiguous GAN-generated imagery as a speculative, ethically preferable alternative.

---

## Methods

### Dataset
- Training data: Reuters "Photos of the Week" collection from the year 2020
- Approximately 1,000 photographs
- Content: almost exclusively images documenting natural disasters, social unrest, political protests, military conflicts, and pandemic events — a deliberately heterogeneous, thematically unified dataset
- Dataset was compiled with the assistance of data collector Adriana Homolová

### Model
- Architecture: StyleGAN2 (based on Karras et al., 2020 — "Analyzing and Improving the Image Quality of StyleGAN")
- Technical guidance: Pavol Rusnák
- Developed at the Academy of Performing Arts in Prague, 2021
- Funding: Czech Ministry of Education and Science (targeted university research funding)

### Training Strategy
- Deliberate exposure of the generative model to failure conditions
- Intentionally heterogeneous dataset: the high variability of scene types (many people, chaotic compositions, different lighting, different locations) structurally prevents the network from achieving photorealism
- This failure is treated as a methodological feature, not a bug
- The training process was critically observed step by step, with close attention paid to unexpected outputs and surprising moments

### Analytical Framework
- Theoretical grounding in Pasquinelli and Joler's "The Nooscope Manifested" (2020), which conceptualises machine learning as an "instrument of knowledge"
- The key metaphor from that text: "the information flow of machine learning is like a light beam that is projected by the training data, compressed by the algorithm and diffracted towards the world by the lens of the statistical model"
- StyleGAN is thus treated as a pattern-recognition and knowledge-production device, not merely an image generator

---

## Key Findings

### 1. Visual Ambiguity as an Intentional Outcome
- TroublingGAN outputs combine concrete and abstract elements
- Typical GAN artefacts appear: blobs, smudges, blurred regions in contrast with sharply rendered details
- Some figures display dark voids where eyes and mouths would be — a disturbing visual effect compared by the authors to the paintings of Francis Bacon
- These ambiguous outputs resist fixed interpretation: viewer perception continuously shifts between possible readings, generating dynamic rather than static meaning
- The network cannot achieve photorealism given the dataset's heterogeneity — but the outputs still retain a photographic quality, resembling a photograph without depicting any specific recognisable scene

### 2. GAN Failure as Knowledge Production
- The deliberate induction of failure modes is central to the methodology
- Unexpected, surprising outputs during training are treated as epistemically significant — as moments of revelation about what the network has "learned" from the dataset
- The process of training itself, not only the final outputs, is understood as a form of research
- Emphasis on process over product allows for critical reflection on each step of StyleGAN training

### 3. Critique of Photojournalism's Decontextualization
- The project identifies a widespread problem: documentary photographs are recycled as illustrative stock photos, primarily to evoke emotion rather than document context
- Example cited: the reuse of conflict photographs (particularly from Ukraine) stripped of their original documentary context
- When a photograph originally made to document a specific event is redeployed as an affective image, it becomes a "stock photo" — a process that diminishes specific narratives and raises ethical concerns
- The distinction between documentary photography (context-bound) and affective illustration (context-free) is identified as a key ethical problem in contemporary media

### 4. GAN as Speculative Alternative
- The proposition: replace recycled photojournalistic stock photos with GAN-generated semi-abstract visuals trained on thematically equivalent photography
- This approach removes the ethical problem of decontextualization because no specific documentary photograph is being reused
- The generated visuals carry the "affective quality" of the training dataset — they project the emotional essence of crisis photography — without depicting any identifiable person, place, or event
- This is framed as "speculative" rather than prescriptive: a proposition for a possible alternative practice, not a finished solution

### 5. Ethical and Critical Dimensions
- Multiple unforeseen developments arose during the research, generating new ethical questions about the use of generative neural networks
- The project raises questions about bias in training data: AI outputs are only as good as their inputs
- The closing argument is a systemic metaphor: generating new solutions from unchanged inputs perpetuates existing problems. True AI "enlightenment" requires training data free from stereotypes and biases

---

## How They Use GANs in Artistic Practice

The GAN is used not primarily as an image-generation tool but as a pattern-recognition and research instrument. Key aspects:

- **Training as practice**: The act of training the model — selecting data, observing intermediate outputs, responding to failure — is itself the artistic and research process
- **Dataset curation as artistic decision**: The choice of Reuters "Photos of the Week" 2020 is both an archival act and a curatorial interpretation of "troubling times"
- **Failure as material**: The network's inability to achieve photorealism is not corrected but observed, documented, and interpreted
- **Output as speculation**: Final generated images are presented as speculative alternatives to existing photojournalism practice, not as finished artworks in a conventional sense
- **StyleGAN2 latent space**: The model works within StyleGAN2's latent space, producing seed-numbered outputs (seed000.jpg through seed999.jpg) available via the project website

---

## What They Say About Visual Ambiguity and Failure

The treatment of visual ambiguity and failure is the theoretical core of the exposition:

- **Ambiguity as cognitive activation**: Ambiguous outputs cause the viewer's mind to continuously assign shifting meanings to abstract compositions. Unlike a clear photographic image, which closes interpretation, the GAN output opens and sustains interpretive flux. This is presented as a distinct perceptual and potentially political quality.
- **Failure as epistemological signal**: When the network fails to converge on photorealism, this failure reveals something about the dataset itself — specifically, that "troubling times" resists clear visual synthesis. The heterogeneity of crisis imagery is too complex to be distilled into a coherent photographic average.
- **Francis Bacon comparison**: Figures with absent or voided facial features (dark holes where eyes and mouth would be) are compared to Bacon's painted faces — invoking a tradition of deliberate figural distortion to create psychological unease.
- **The artefact as trace**: GAN artefacts (blobs, smudges) are understood not as noise to be eliminated but as traces of the network's learning process — indexical marks of the training data's complexity pressing through the model.
- **Against photorealism**: The project explicitly argues that photorealistic AI-generated imagery is ethically and aesthetically problematic in the context of news media because it deceives viewers into believing they are seeing documentation. Visual ambiguity, by contrast, is honest about its artificial origin.

---

## Theoretical References Cited

- Pasquinelli, M. and Joler, V. (2020). "The Nooscope Manifested: AI as Instrument of Knowledge Extractivism." *AI & Society*. DOI: 10.1007/s00146-020-01097-6
- Karras, T. et al. (2020). "Analyzing and Improving the Image Quality of StyleGAN." [StyleGAN2 paper — foundational technical reference]

---

## Notes for Thesis Use

- This paper is directly relevant to discussions of GAN-based artistic research methodology
- The concept of "GAN failure as epistemological material" is applicable to any practice-led research using generative AI
- The speculative framing (proposition rather than solution) is a methodological stance worth citing when defending artistic research that does not produce definitive answers
- The Nooscope metaphor (light beam / lens / diffraction) offers a clear language for describing how training data shapes AI outputs
- The ethical critique of recontextualization and decontextualization in AI-generated imagery is relevant to any discussion of AI and visual identity construction
- Comparison to Francis Bacon is useful for grounding GAN artefacts in art-historical tradition of deliberate figural distortion
