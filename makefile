# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.

# You should have received a copy of the GNU General Public License along with
# this program. If not, see http://www.gnu.org/licenses/.

SHELL = /bin/bash

.PHONY: all install clean

all:
	make -C bin
	make -C desktop
	make -C doc

install:
	install -d "$(DESTDIR)/lib/udev/rules.d/"
	install -m 644 81-thinkpad-dock.rules -t "$(DESTDIR)/lib/udev/rules.d/"
#
	install -d "$(DESTDIR)/etc/pm/sleep.d/"
	install 00_think-resume.sh -t "$(DESTDIR)/etc/pm/sleep.d/"

	make -C bin install
	make -C desktop install
	make -C doc install

clean:
	make -C bin clean
	make -C desktop clean
	make -C doc clean
