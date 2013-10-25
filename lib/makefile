# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

SHELL = /bin/bash

.PHONY: all install clean

scripts = $(wildcard *.sh)

all:

install:
	install -d "$(DESTDIR)/usr/share/think-rotate"
	for script in $(scripts); do \
		install "$$script" -t "$(DESTDIR)/usr/share/think-rotate"; \
		done

clean:
