#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import collections

Direction = collections.namedtuple('Direction', ['xrandr', 'xsetwacom'])

LEFT = Direction('left', 'ccw')
RIGHT = Direction('right', 'cw')
NORMAL = Direction('normal', 'none')
INVERTED = Direction('inverted', 'half')
