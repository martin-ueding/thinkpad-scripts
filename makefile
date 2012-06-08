# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

help:
	@echo 'This makefile provides only `make install`.'

install:
	install rotate "$(DESTDIR)/usr/bin/"
