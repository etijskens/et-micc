# Minimal makefile for Sphinx documentation
# This file is no longer in the micc templates.

# You can set these variables from the command line.
SPHINXOPTS    =
# if et-micc is pipx installed:
SPHINXBUILD   = $(HOME)/.local/pipx/venvs/et-micc/bin/python -msphinx
# otherwise
#SPHINXBUILD   = python -msphinx
SPHINXPROJ    = micc
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
