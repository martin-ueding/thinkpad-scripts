# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

SHELL = /bin/bash

po := $(wildcard locale/*/LC_MESSAGES/think-rotate.po)
mo := $(po:.po=.mo)

.PHONY: all install clean

all: $(mo)
	make -C bin
	make -C desktop
	make -C doc

install:
	install -d "$(DESTDIR)/lib/udev/rules.d/"
	install -m 644 81-thinkpad-dock.rules -t "$(DESTDIR)/lib/udev/rules.d/"
#
	install -d "$(DESTDIR)/etc/acpi/events/"
	install think-mutemic-acpi-hook -t "$(DESTDIR)/etc/acpi/events/"
	install think-rotate-acpi-hook -t "$(DESTDIR)/etc/acpi/events/"
	if [[ -z "$(DESTDIR)" ]]; then service acpid restart; fi
#
	install -d "$(DESTDIR)/usr/share/locale/de/LC_MESSAGES"
	for mofile in $(mo); \
	    do \
	    cp "$$mofile" "$(DESTDIR)/usr/share/$$mofile"; \
	    done
#
#
	make -C bin install
	make -C desktop install
	make -C doc install
	make -C lib install

clean:
	make -C bin clean
	make -C desktop clean
	make -C doc clean

locale/think-rotate.pot: bin/*
	xgettext --language Shell -o $@ $^

%.mo: %.po
	msgfmt -o $@ $^
