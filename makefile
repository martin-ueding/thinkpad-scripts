# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

all: rotate.1

%.1: %.1.rst
	rst2man $< $@

install:
	install rotate "$(DESTDIR)/usr/bin/"
