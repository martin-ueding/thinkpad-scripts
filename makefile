# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

all: rotate.1.gz

%.1.gz: %.1
	gzip $<

%.1: %.1.rst
	rst2man $< $@

install:
	install rotate "$(DESTDIR)/usr/bin/"
	if [ -f rotate.1.gz ]; then cp rotate.1.gz "$(DESTDIR)/usr/share/man/man1/"; fi
