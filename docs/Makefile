# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = Neo
SOURCEDIR     = source
BUILDDIR      = build
PYCMD 				= python

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

	figures:
		@$(PYCMD) source/scripts/compile_images.py

	docset: html
		doc2dash --name $(SPHINXPROJ) --icon $(SOURCEDIR)/_static/img/neo.logo.png --enable-js --online-redirect-url http://neo.sintefneodroid.github.io/docs/ --force $(BUILDDIR)/html/

		# Manually fix because Zeal doesn't deal well with `icon.png`-only at 2x resolution.
		cp $(SPHINXPROJ).docset/icon.png $(SPHINXPROJ).docset/icon@2x.png
	convert $(SPHINXPROJ).docset/icon@2x.png -resize 16x16 $(SPHINXPROJ).docset/icon.png

.PHONY: help Makefile docset

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean:
	@echo "Removing everything under 'build'.."
	@rm -r $(BUILDDIR)/html/ $(BUILDDIR)/doctrees
