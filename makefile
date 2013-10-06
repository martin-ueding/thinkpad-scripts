# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

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
	install -d "$(DESTDIR)/lib/udev/hwdb.d/"
	install -m 644 90-X220T-keyboard.hwdb -t "$(DESTDIR)/lib/udev/hwdb.d/"
# FIXME What happens if we are not installing it to the actual system, but some
# other DESTDIR, like when packaging this? The package install script would
# need to run the following line then.
	if [[ -z "$(DESTDIR)" ]]; then udevadm hwdb --update; fi
#
	install -d "$(DESTDIR)/etc/acpi/events/"
	install think-mutemic-acpi-hook -t "$(DESTDIR)/etc/acpi/events/"
#
	install -d "$(DESTDIR)/usr/share/locale/de/LC_MESSAGES"
	install locale/de/LC_MESSAGES/think-rotate.mo -t "$(DESTDIR)/usr/share/locale/de/LC_MESSAGES"
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
