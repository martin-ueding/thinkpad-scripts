#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import collections

Direction = collections.namedtuple('Direction', ['xrandr', 'xsetwacom', 'subpixel'])
'''
Holds the direction names of different tools.

``xrandr`` and ``xsetwacom`` use different names for the rotations. To avoid
proliferation of various names, this class holds the differing names. The
module provides four constants which have to be used within :mod:`tps`.
'''

LEFT = Direction('left', 'ccw', 'vrgb')
'Left'

RIGHT = Direction('right', 'cw', 'vbgr')
'Right'

NORMAL = Direction('normal', 'none', 'rgb')
'Normal'

INVERTED = Direction('inverted', 'half', 'bgr')
'Inverted'

class UnknownDirectionException(Exception):
    '''
    Unknown direction given at the command line.
    '''

def translate_direction(direction):
    if direction == 'normal':
        return NORMAL

    if direction == 'left':
        return LEFT

    if direction == 'right':
        return RIGHT

    if direction == 'flip':
        return INVERTED
    if direction == 'inverted':
        return INVERTED

    raise UnknownDirectionException('Direction “{}” cannot be understood.'.format(direction))
