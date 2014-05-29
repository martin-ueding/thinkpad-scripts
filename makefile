# Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

SHELL = /bin/bash

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
#
	install -d "$(DESTDIR)/etc/acpi/events/"
	install -m 644 thinkpad-mutemic-acpi-hook -t "$(DESTDIR)/etc/acpi/events/"
	install -m 644 thinkpad-rotate-acpi-hook-1 -t "$(DESTDIR)/etc/acpi/events/"
	install -m 644 thinkpad-rotate-acpi-hook-2 -t "$(DESTDIR)/etc/acpi/events/"
#
	cd desktop && $(MAKE) install
	cd doc && $(MAKE) install

full-install: install
	if [[ -z "$(DESTDIR)" ]]; then udevadm hwdb --update; fi
	if [[ -z "$(DESTDIR)" ]] && which service &> /dev/null; then service acpid restart; fi
	if [[ -z "$(DESTDIR)" ]] && which systemctl &> /dev/null; then systemctl restart acpid; fi

clean:
	$(RM) ./*.pyc
	$(RM) -r ./*.egg-info
	$(RM) -r build
	$(RM) -r dist
	cd desktop && $(MAKE) clean
	cd doc && $(MAKE) clean
	find . -name '*.pyc' -print -delete
	find . -name __pycache__ -print -delete
