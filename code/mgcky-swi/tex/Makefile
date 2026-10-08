# Build every tree document in this directory.
.DEFAULT_GOAL := all

export PATH := /opt/local/bin:$(PATH)
LATEX = latex
DVIPS = dvips
PS2PDF = ps2pdf

SOURCES := $(wildcard *.tex)
PDFS := $(SOURCES:.tex=.pdf)

.PHONY: all clean
.DELETE_ON_ERROR:

all: $(PDFS)

%.pdf: %.tex
	$(LATEX) -interaction=nonstopmode -halt-on-error "$<"
	$(DVIPS) -o "$*.ps" "$*.dvi"
	$(PS2PDF) "$*.ps" "$@"
	$(RM) "$*.aux" "$*.log" "$*.dvi" "$*.ps" "$*.out" "$*.toc"

# Keep sources and PDFs; remove only intermediate files.
clean:
	$(RM) *.aux *.log *.dvi *.ps *.out *.toc
