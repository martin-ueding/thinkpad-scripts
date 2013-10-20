# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

SHELL = /bin/bash

.PHONY: all install clean

manuals_rst = $(wildcard *.rst)
manuals = $(manuals_rst:.rst=.gz)

all: $(manuals)

install:
	for manual in $(manuals); do \
		if [[ -f "$$manual" ]]; then \
		install -d "$(DESTDIR)/usr/share/man/man1/"; \
		install -m 644 "$$manual" -t "$(DESTDIR)/usr/share/man/man1/"; \
		fi; \
		done

clean:
	$(RM) *.1
	$(RM) *.1.gz

%.1.gz: %.1
	$(RM) $@
	gzip $<

%.1: %.1.rst
	rst2man $< $@
