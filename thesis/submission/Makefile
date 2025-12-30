# Makefile for Artistic Research Submission Documents
# Everything Machine - Dark Theme PDFs
#
# Usage:
#   make all          - Build all documents
#   make forschung    - Build Forschungsfrage PDF
#   make literatur    - Build Literaturrecherche PDF
#   make methodik     - Build Methodologie PDF
#   make doku         - Build Final Dokumentation PDF
#   make clean        - Remove generated files

.PHONY: help all clean forschung literatur methodik doku watch

# === CONFIGURATION ===
PANDOC := pandoc
TEMPLATE := template-dark.tex
ENGINE := lualatex
OUTDIR := output
DOCSDIR := docs
BIBFILE := references/bibliography.bib

# Common Pandoc flags
PANDOC_FLAGS := --template=$(TEMPLATE) \
                --pdf-engine=$(ENGINE) \
                --citeproc \
                --bibliography=$(BIBFILE)

# === DEFAULT TARGET ===
help:
	@echo ""
	@echo "  Everything Machine - Artistic Research Submission"
	@echo "  =================================================="
	@echo ""
	@echo "  Individual Documents:"
	@echo "    make forschung    Build Forschungsfrage (research questions)"
	@echo "    make literatur    Build Literaturrecherche (literature review)"
	@echo "    make methodik     Build Methodologie (methodology)"
	@echo "    make doku         Build Dokumentation (final ~10 page paper)"
	@echo ""
	@echo "  Combined:"
	@echo "    make all          Build all documents"
	@echo "    make clean        Remove generated files"
	@echo ""
	@echo "  Output: $(OUTDIR)/"
	@echo ""

# === INDIVIDUAL TARGETS ===

forschung: $(OUTDIR)/01-forschungsfrage.pdf
	@echo "Done: $(OUTDIR)/01-forschungsfrage.pdf"

literatur: $(OUTDIR)/02-literaturrecherche.pdf
	@echo "Done: $(OUTDIR)/02-literaturrecherche.pdf"

methodik: $(OUTDIR)/03-methodologie.pdf
	@echo "Done: $(OUTDIR)/03-methodologie.pdf"

doku: $(OUTDIR)/04-dokumentation.pdf
	@echo "Done: $(OUTDIR)/04-dokumentation.pdf"

# === BUILD RULES ===

$(OUTDIR)/01-forschungsfrage.pdf: $(DOCSDIR)/01-forschungsfrage.md $(TEMPLATE) $(BIBFILE)
	@echo "Building Forschungsfrage..."
	@$(PANDOC) $< -o $@ $(PANDOC_FLAGS)

$(OUTDIR)/02-literaturrecherche.pdf: $(DOCSDIR)/02-literaturrecherche.md $(TEMPLATE) $(BIBFILE)
	@echo "Building Literaturrecherche..."
	@$(PANDOC) $< -o $@ $(PANDOC_FLAGS)

$(OUTDIR)/03-methodologie.pdf: $(DOCSDIR)/03-methodologie.md $(TEMPLATE) $(BIBFILE)
	@echo "Building Methodologie..."
	@$(PANDOC) $< -o $@ $(PANDOC_FLAGS)

$(OUTDIR)/04-dokumentation.pdf: $(DOCSDIR)/04-dokumentation.md $(TEMPLATE) $(BIBFILE)
	@echo "Building Dokumentation..."
	@$(PANDOC) $< -o $@ $(PANDOC_FLAGS)

# === COMBINED TARGETS ===

all: forschung literatur methodik doku
	@echo ""
	@echo "=========================================="
	@echo "  All documents generated successfully!"
	@echo "=========================================="
	@echo ""
	@echo "  Output files:"
	@echo "    $(OUTDIR)/01-forschungsfrage.pdf"
	@echo "    $(OUTDIR)/02-literaturrecherche.pdf"
	@echo "    $(OUTDIR)/03-methodologie.pdf"
	@echo "    $(OUTDIR)/04-dokumentation.pdf"
	@echo ""

# === CLEANUP ===

clean:
	@echo "Cleaning output directory..."
	@rm -f $(OUTDIR)/*.pdf
	@rm -f $(OUTDIR)/*.aux $(OUTDIR)/*.log $(OUTDIR)/*.out
	@rm -f $(OUTDIR)/*.toc $(OUTDIR)/*.bbl $(OUTDIR)/*.bcf
	@rm -f $(OUTDIR)/*.blg $(OUTDIR)/*.run.xml
	@echo "Done."

# === UTILITIES ===

# Check if required tools are installed
check:
	@echo "Checking requirements..."
	@which $(PANDOC) > /dev/null || (echo "ERROR: pandoc not found" && exit 1)
	@which $(ENGINE) > /dev/null || (echo "ERROR: lualatex not found" && exit 1)
	@which biber > /dev/null || (echo "ERROR: biber not found" && exit 1)
	@echo "All requirements satisfied."
