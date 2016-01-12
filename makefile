# Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2015 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

SHELL = /bin/bash

.PHONY: all common-install install full-install test clean

all: $(mo)
	cd desktop && $(MAKE)
	cd doc && $(MAKE)

common-install:
	install -d "$(DESTDIR)/lib/udev/rules.d/"
	install -m 644 udevd/81-thinkpad-dock.rules -t "$(DESTDIR)/lib/udev/rules.d/"
#
	install -d "$(DESTDIR)/lib/udev/hwdb.d/"
	install -m 644 udevd/90-X2x0T-keyboard.hwdb -t "$(DESTDIR)/lib/udev/hwdb.d/"
#
	install -d "$(DESTDIR)/etc/acpi/events/"
	install -m 644 acpid/thinkpad-scripts-mutemic -t "$(DESTDIR)/etc/acpi/events/"
	install -m 644 acpid/thinkpad-scripts-rotate -t "$(DESTDIR)/etc/acpi/events/"
	install -m 644 acpid/thinkpad-scripts-rotated-start -t "$(DESTDIR)/etc/acpi/events/"
	install -m 644 acpid/thinkpad-scripts-rotated-stop -t "$(DESTDIR)/etc/acpi/events/"
	
	install -d "$(DESTDIR)/etc/modules-load.d/"
	install -m 644 modules-load.d/thinkpad-scripts.conf -t "$(DESTDIR)/etc/modules-load.d/"
	
	install -d "$(DESTDIR)/usr/lib/systemd/system/"
	install -m 644 init/thinkpad-rotated -t "$(DESTDIR)/usr/lib/systemd/system/"
#
	cd desktop && $(MAKE) install
	cd doc && $(MAKE) install
#

install: common-install
	@echo
	@echo '======== One more Step! =================='
	@echo
	@echo 'You might have to call `./setup.py install` to install the actual scripts after this and restart the services. Please consult the “Getting Started” guide which can be found at `doc/guides/getting-started.rst` or on the web at:'
	@echo
	@echo 'http://thinkpad-scripts.readthedocs.org/en/latest/guides/getting-started.html#build-manually'
	@echo
	@echo '=========================================='
	@echo

full-install: common-install
	@if [[ -n "$(DESTDIR)" ]]; then echo; echo '==> DESTDIR is set, so you have to install this stepwise. See `doc/guides/getting-started.rst` or http://thinkpad-scripts.readthedocs.org/en/latest/guides/getting-started.html#build-manually for more information. <=='; false; fi
	#
	./setup.py install
	udevadm hwdb --update
	if which service &> /dev/null; then
	    service acpid restart;
	elif which systemctl &> /dev/null; then
	    systemctl restart acpid;
	    systemctl enable thinkpad-rotated;
	fi

test:
	./setup.py test

clean:
	$(RM) ./*.pyc
	$(RM) -r ./*.egg-info
	$(RM) -r build
	$(RM) -r dist
	cd desktop && $(MAKE) clean
	cd doc && $(MAKE) clean
	find . -name '*.pyc' -print -delete
	find . -name __pycache__ -print -delete
