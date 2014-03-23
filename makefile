# Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

SHELL = /bin/bash

po := $(wildcard locale/*/LC_MESSAGES/thinkpad-scripts.po)
mo := $(po:.po=.mo)

.PHONY: all install clean

all: $(mo)
	cd desktop && $(MAKE)
	cd doc && $(MAKE)

install:
	install -d "$(DESTDIR)/lib/udev/rules.d/"
	install -m 644 81-thinkpad-dock.rules -t "$(DESTDIR)/lib/udev/rules.d/"
#
	install -d "$(DESTDIR)/lib/udev/hwdb.d/"
	install -m 644 90-X2x0T-keyboard.hwdb -t "$(DESTDIR)/lib/udev/hwdb.d/"
	if [[ -z "$(DESTDIR)" ]]; then udevadm hwdb --update; fi
#
	install -d "$(DESTDIR)/etc/acpi/events/"
	install -m 644 thinkpad-mutemic-acpi-hook -t "$(DESTDIR)/etc/acpi/events/"
	install -m 644 thinkpad-rotate-acpi-hook-1 -t "$(DESTDIR)/etc/acpi/events/"
	install -m 644 thinkpad-rotate-acpi-hook-2 -t "$(DESTDIR)/etc/acpi/events/"
#
	install -d "$(DESTDIR)/usr/share/locale/de/LC_MESSAGES"
	for mofile in $(mo); \
	    do \
	    install -m 644 "$$mofile" "$(DESTDIR)/usr/share/$$mofile"; \
	    done
#
	cd desktop && $(MAKE) install
	cd doc && $(MAKE) install
	cd lib && $(MAKE) install

clean:
	$(RM) *.pyc
	$(RM) -r *.egg-info
	$(RM) -r build
	$(RM) -r dist
	$(RM) locale/*/LC_MESSAGES/*.mo
	cd desktop && $(MAKE) clean
	cd doc && $(MAKE) clean
	find . -name '*.pyc' -print -delete
	find . -name __pycache__ -print -delete

%.mo: %.po
	msgfmt -o $@ $^
