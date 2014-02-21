#!/bin/bash
# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

run-upgrades() {
    run-3.3-to-3.4
}

run-3.3-to-3.4 () {
    local olddir="$HOME/.config/think-rotate"
    local newdir="$HOME/.config/thinkpad-scripts"

    if [[ -d "$olddir" ]] && [[ ! -d "$newdir" ]]
    then
        mv "$olddir" "$newdir"
    fi
}
