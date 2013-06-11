# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

SHELL = /bin/bash

.PHONY: all install clean

scripts = $(wildcard think-*)

all:

install:
	install -d "$(DESTDIR)/usr/bin/"
	for script in $(scripts); do \
		install "$$script" -t "$(DESTDIR)/usr/bin/"; \
		done
#
	install -d "$(DESTDIR)/etc/init.d/"
	install think-keycodes -t "$(DESTDIR)/etc/init.d/"
# FIXME What happens if we are not installing it to the actual system, but some
# other DESTDIR, like when packaging this? The package install script would
# need to run the following line then.
	if [[ -z "$(DESTDIR)" ]]; then update-rc.d think-keycodes defaults; fi
#
	install -d "$(DESTDIR)/usr/bin/"
	install think-mutemic -t "$(DESTDIR)/usr/bin/"

clean:
