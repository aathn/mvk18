# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

latexpdf:
	$(SPHINXBUILD) -b latex $(SOURCEDIR) $(BUILDDIR)/latex $(SPHINXOPTS) $(O)
	sed -i 's/\\begin{tabulary}{\\linewidth}\[t\]{|T|\(.*\)}/\\begin{ltabulary}[t]{|L|\1}/' $(BUILDDIR)/latex/*.tex
	sed -i 's/\\end{tabulary}/\\end{ltabulary}/' $(BUILDDIR)/latex/*.tex
	sed -i '/\\begin{ltabulary}/ i\\\settowidth\\tymin{Outgoing}\\setlength\\extrarowheight{2pt}' $(BUILDDIR)/latex/*.tex

	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(BUILDDIR)/latex all-pdf
	@echo "pdflatex finished; the PDF files are in $(BUILDDIR)/latex."

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)