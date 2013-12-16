# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2013 Jim Turner <jturner314@gmail.com>

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = _build
DESTDIR       =

# Internal variables.
manuals = $(addsuffix .gz,$(notdir $(basename $(wildcard man/*.1.rst))))
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .
SHELL = /bin/bash

.PHONY: all install clean html

all: html man

install:
	if ls $(BUILDDIR)/man/*.1.gz; then \
		install -d "$(DESTDIR)/usr/share/man/man1/"; \
		install -m 644 $(BUILDDIR)/man/*.1.gz -t "$(DESTDIR)/usr/share/man/man1/"; \
	fi

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

man: $(addprefix $(BUILDDIR)/man/,$(manuals))

$(BUILDDIR)/man/%.1.gz: $(BUILDDIR)/man/%.1
	$(RM) $@
	gzip $<

$(BUILDDIR)/man/%.1: man/%.1.rst
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man

clean:
	-rm -rf $(BUILDDIR)/*
