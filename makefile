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

manuals = think-rotate.1.gz think-dock.1.gz think-touchpad.1.gz think-touch.1.gz think-resume.1.gz think-startup.1.gz
desktopfiles = think-dock-off.desktop think-dock-on.desktop think-rotate-flip.desktop think-rotate-left.desktop think-rotate.desktop
scripts = think-dock think-dock-hook think-resume think-resume-hook think-rotate think-startup think-startup-hook think-touch think-touchpad

all: $(manuals)

%.1.gz: %.1
	$(RM) $@
	gzip $<

%.1: %.1.rst
	rst2man $< $@

install:
	for manual in $(manuals); \
		do \
		if [[ -f "$$manual" ]]; \
		then \
		install -d "$(DESTDIR)/usr/share/man/man1/"; cp "$$manual" "$(DESTDIR)/usr/share/man/man1/"; \
		fi; \
		done
	#
	install -d "$(DESTDIR)/usr/share/applications/"
	for desktopfile in $(desktopfiles); \
		do \
		install -m 644 "$$desktopfile" -t "$(DESTDIR)/usr/share/applications/"; \
		done
	#
	install -d "$(DESTDIR)/usr/bin/"
	for script in $(scripts); \
		do \
		install "$$script" -t "$(DESTDIR)/usr/bin/"; \
		done
	#
	install -d "$(DESTDIR)/lib/udev/rules.d/"
	install 81-thinkpad-dock.rules -t "$(DESTDIR)/lib/udev/rules.d/"
	#
	install -d "$(DESTDIR)/etc/pm/sleep.d/"
	install 00_think-resume.sh -t "$(DESTDIR)/etc/pm/sleep.d/"
	if ! grep -q "setkeycodes 6e 109 6d 104 69 28 6b 01 6c 120" "$(DESTDIR)/etc/rc.local"; then sed -i '$$isetkeycodes 6e 109 6d 104 69 28 6b 01 6c 120' "$(DESTDIR)/etc/rc.local"; fi
	#
	if ! grep -q "think-startup" "$(DESTDIR)/etc/rc.local"; then sed -i '$$ithink-startup-hook' "$(DESTDIR)/etc/rc.local"; fi

clean:
	$(RM) *.1
	$(RM) *.1.gz
