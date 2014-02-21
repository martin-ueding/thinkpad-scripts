#!/bin/bash
# Copyright © 2013-2014 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2013 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

find-external() {
    local i=0
    until external=$(xrandr | grep -Eo '(\S+) connected' | grep -Eo '^(\S+)' | grep -v "$internal") || (( i >= 5 ))
    do
        sleep 1
        i=$(( i + 1 ))
    done
}
