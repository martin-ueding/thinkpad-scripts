# Copyright © 2012-2013 Martin Ueding <dev@martin-ueding.de>

SHELL = /bin/bash

.PHONY: all install clean

desktopfiles = $(wildcard *.desktop)

all:

install:
	install -d "$(DESTDIR)/usr/share/applications/"
	for desktopfile in $(desktopfiles); do \
		install -m 644 "$$desktopfile" -t "$(DESTDIR)/usr/share/applications/"; \
		done

clean:
