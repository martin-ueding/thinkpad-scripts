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

all: think-rotate.1.gz think-dock.1.gz think-touchpad.1.gz

%.1.gz: %.1
	$(RM) $@
	gzip $<

%.1: %.1.rst
	rst2man $< $@

install:
	if [ -f think-dock.1.gz ]; then install -d "$(DESTDIR)/usr/share/man/man1/"; cp think-dock.1.gz "$(DESTDIR)/usr/share/man/man1/"; fi
	if [ -f think-rotate.1.gz ]; then install -d "$(DESTDIR)/usr/share/man/man1/"; cp think-rotate.1.gz "$(DESTDIR)/usr/share/man/man1/"; fi
	if [ -f think-touchpad.1.gz ]; then install -d "$(DESTDIR)/usr/share/man/man1/"; cp think-touchpad.1.gz "$(DESTDIR)/usr/share/man/man1/"; fi
	#
	install -d "$(DESTDIR)/usr/share/applications/"
	install -m 644 think-dock-off.desktop -t "$(DESTDIR)/usr/share/applications/"
	install -m 644 think-dock-on.desktop -t "$(DESTDIR)/usr/share/applications/"
	install -m 644 think-rotate-flip.desktop -t "$(DESTDIR)/usr/share/applications/"
	install -m 644 think-rotate-left.desktop -t "$(DESTDIR)/usr/share/applications/"
	install -m 644 think-rotate.desktop -t "$(DESTDIR)/usr/share/applications/"
	#
	install -d "$(DESTDIR)/usr/bin/"
	install think-dock -t "$(DESTDIR)/usr/bin/"
	install think-dock-hook -t "$(DESTDIR)/usr/bin/"
	install think-rotate -t "$(DESTDIR)/usr/bin/"
	install think-touchpad -t "$(DESTDIR)/usr/bin/"
	#
	install -d "$(DESTDIR)/lib/udev/rules.d/"
	install 81-thinkpad-dock.rules -t "$(DESTDIR)/lib/udev/rules.d/"


clean:
	$(RM) *.1
	$(RM) *.1.gz
