# Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2013 Jim Turner <jturner314@gmail.com>

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = $(shell ./find_sphinx.py)
BUILDDIR      = _build
DESTDIR       =

# Internal variables.
ALLSPHINXOPTS = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) .
SHELL = /bin/bash

.PHONY: all install clean html man

all: html man

install:
	if ls $(BUILDDIR)/man/*.1.gz &> /dev/null; then \
	    install -d "$(DESTDIR)/usr/share/man/man1/"; \
	    install -m 644 $(BUILDDIR)/man/*.1.gz -t "$(DESTDIR)/usr/share/man/man1/"; \
	fi

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

man:
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(BUILDDIR)/man
	gzip -f $(BUILDDIR)/man/*.1

clean:
	$(RM) -rf $(BUILDDIR)/*
