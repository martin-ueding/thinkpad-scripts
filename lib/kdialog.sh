#!/bin/bash
# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

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

kdialog-init() {
	if ! [[ "$kdialog" == "true" ]]
	then
		return
	fi

	kdialog_handle="$(kdialog --title "$1" --progressbar "Start" "$2")"
	kdialog_number=0
}

kdialog-update() {
	if ! [[ "$kdialog" == "true" ]]
	then
		return
	fi

	qdbus $kdialog_handle setLabelText "$1" > /dev/null
	qdbus $kdialog_handle Set "" value "$kdialog_number" > /dev/null
	: $(( kdialog_number++ ))
}

kdialog-exit() {
	if ! [[ "$kdialog" == "true" ]]
	then
		return
	fi

	qdbus $kdialog_handle close > /dev/null
}
