# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

all: think-rotate.1.gz think-dock.1.gz think-touchpad.1.gz

%.1.gz: %.1
	$(RM) $@
	gzip $<

%.1: %.1.rst
	rst2man $< $@

install:
	if [ -f think-dock.1.gz ]; then cp think-dock.1.gz "$(DESTDIR)/usr/share/man/man1/"; fi
	if [ -f think-rotate.1.gz ]; then cp think-rotate.1.gz "$(DESTDIR)/usr/share/man/man1/"; fi
	if [ -f think-touchpad.1.gz ]; then cp think-touchpad.1.gz "$(DESTDIR)/usr/share/man/man1/"; fi
	install -m 644 *.desktop "$(DESTDIR)/usr/share/applications/"
	install think-dock "$(DESTDIR)/usr/bin/"
	install think-rotate "$(DESTDIR)/usr/bin/"
	install think-touchpad "$(DESTDIR)/usr/bin/"
