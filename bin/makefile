# Copyright © 2012-2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

SHELL = /bin/bash

.PHONY: all install clean

scripts = $(wildcard thinkpad-*)

all:

install:
	install -d "$(DESTDIR)/usr/bin/"
	for script in $(scripts); do \
		install "$$script" -t "$(DESTDIR)/usr/bin/"; \
		done

clean:
