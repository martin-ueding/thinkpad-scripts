#!/bin/bash
# Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

kdialog-init() {
	if ! [[ "$kdialog" == "true" ]]
	then
		return
	fi

	# Abort, it kdialog is not installed.
	if ! type kdialog &> /dev/null
	then
		kdialog=false
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
