# Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

SHELL = /bin/bash

.PHONY: all install clean

scripts = $(wildcard *.sh)

all:

install:
	install -d "$(DESTDIR)/usr/share/thinkpad-scripts"
	for script in $(scripts); do \
		install "$$script" -t "$(DESTDIR)/usr/share/thinkpad-scripts"; \
		done

clean:
