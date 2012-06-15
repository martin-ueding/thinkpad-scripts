# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

all: think-rotate.1.gz

%.1.gz: %.1
	$(RM) $@
	gzip $<

%.1: %.1.rst
	rst2man $< $@

install:
	install think-rotate "$(DESTDIR)/usr/bin/"
	if [ -f think-rotate.1.gz ]; then cp think-rotate.1.gz "$(DESTDIR)/usr/share/man/man1/"; fi
	install -m 644 *.desktop "$(DESTDIR)/usr/share/applications/"
