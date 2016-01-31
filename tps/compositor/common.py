# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

'''Definitions shared among different compositors.
'''

import collections
import logging


logger = logging.getLogger(__name__)

Direction = collections.namedtuple(
    'Direction', ['xrandr', 'subpixel', 'rot_mat']
)
'''
Holds the direction names of different tools.

``xrandr`` and other programs use different names for the rotations. To avoid
proliferation of various names, this class holds the differing names. The
module provides constants which have to be used within :mod:`tps`.
'''

LEFT = Direction('left', 'vrgb', [0,-1, 1,
                                  1, 0, 0,
                                  0, 0, 1])

RIGHT = Direction('right', 'vbgr', [0, 1, 0,
                                   -1, 0, 1,
                                    0, 0, 1])

NORMAL = Direction('normal', 'rgb', [1, 0, 0,
                                     0, 1, 0,
                                     0, 0, 1])

INVERTED = Direction('inverted', 'bgr', [-1, 0, 1,
                                          0,-1, 1,
                                          0, 0, 1])


class InputDeviceNotFoundException(Exception):
    '''
    ``xinput`` device could not be found.
    '''
    pass
    
class ScreenNotFoundException(Exception):
    '''
    ``xrandr`` device could not be found.
    '''
    pass

class UnknownDirectionException(Exception):
    '''
    Unknown direction given at the command line.
    '''

def translate_direction(direction):
    '''
    :param str direction: Direction string
    :returns: Direction object
    :rtype: Direction
    :raises UnknownDirectionException:
    '''

    if direction in ['normal', 'tablet-normal', 'none']:
        result = NORMAL
    elif direction in ['left', 'ccw']:
        result = LEFT
    elif direction in ['right', 'cw']:
        result = RIGHT
    elif direction in ['flip', 'inverted', 'half']:
        result = INVERTED
    else:
        raise UnknownDirectionException(
            'Direction “{}” cannot be understood.'.format(direction))

    logger.debug('Converted “{}” to “{}”.'.format(direction, result))

    return result
