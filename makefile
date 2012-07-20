# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

all: think-rotate.1.gz think-dock.1.gz think-touchpad.1.gz

%.1.gz: %.1
	$(RM) $@
	gzip $<

%.1: %.1.rst
	rst2man $< $@

install:
	if [ -f think-dock.1.gz ]; then install -d "$(DESTDIR)/usr/share/man/man1/"; cp think-dock.1.gz "$(DESTDIR)/usr/share/man/man1/"; fi
	if [ -f think-rotate.1.gz ]; then install -d "$(DESTDIR)/usr/share/man/man1/"; cp think-rotate.1.gz "$(DESTDIR)/usr/share/man/man1/"; fi
	if [ -f think-touchpad.1.gz ]; then install -d "$(DESTDIR)/usr/share/man/man1/"; cp think-touchpad.1.gz "$(DESTDIR)/usr/share/man/man1/"; fi
	install -d "$(DESTDIR)/usr/share/applications/"
	install -m 644 think-rotate.desktop -t "$(DESTDIR)/usr/share/applications/"
	install -m 644 think-rotate-flip.desktop -t "$(DESTDIR)/usr/share/applications/"
	install -d "$(DESTDIR)/usr/bin/"
	install think-dock -t "$(DESTDIR)/usr/bin/"
	install think-rotate -t "$(DESTDIR)/usr/bin/"
	install think-touchpad -t "$(DESTDIR)/usr/bin/"

clean:
	$(RM) *.1
	$(RM) *.1.gz
