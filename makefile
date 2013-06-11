# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

SHELL = /bin/bash

.PHONY: all install clean

all:
	make -C bin
	make -C desktop
	make -C doc

install:
	install -d "$(DESTDIR)/lib/udev/rules.d/"
	install -m 644 81-thinkpad-dock.rules -t "$(DESTDIR)/lib/udev/rules.d/"
#
	install -d "$(DESTDIR)/etc/pm/sleep.d/"
	install 00_think-resume.sh -t "$(DESTDIR)/etc/pm/sleep.d/"
#
	install -d "$(DESTDIR)/etc/acpi/events/"
	install think-mutemic-acpi-hook -t "$(DESTDIR)/etc/acpi/events/"
#
	make -C bin install
	make -C desktop install
	make -C doc install
	make -C lib install

clean:
	make -C bin clean
	make -C desktop clean
	make -C doc clean
