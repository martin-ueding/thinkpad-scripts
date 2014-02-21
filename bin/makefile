# Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>

SHELL = /bin/bash

.PHONY: all install clean

scripts = $(wildcard thinkpad-*)

all:

install:
	install -d "$(DESTDIR)/usr/bin/"
	for script in $(scripts); do \
		install "$$script" -t "$(DESTDIR)/usr/bin/"; \
		done
#
	install -d "$(DESTDIR)/usr/bin/"
	install thinkpad-mutemic -t "$(DESTDIR)/usr/bin/"

clean:
