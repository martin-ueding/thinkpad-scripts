# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

'''Definitions shared among different compositors.
'''

import collections
import logging

from tps.acpi.thinkpad_acpi import ThinkpadAcpi


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
            _('Direction “{}” cannot be understood.').format(direction))

    logger.debug(_('Converted “{}” to “{}”.').format(direction, result))

    return result
    
def cycle_rotation(current, clockwise):
    '''Cycle clockwise or counter clockwise between screen rotations'''
    if current == NORMAL:
        return RIGHT if clockwise else LEFT
    elif current == RIGHT:
        return INVERTED if clockwise else NORMAL
    elif current == INVERTED:
        return LEFT if clockwise else RIGHT
    elif current == LEFT:
        return NORMAL if clockwise else INVERTED
    else:
        raise UnknownDirectionException(
            _('Direction “{}” is invalid.').format(current))

def new_rotation(current, desired_str, config, force=False):
    '''
    Determines the new rotation based on desired and current one.

    :param bool force: If set the function does not try to be too clever but
    just uses the rotation given. If no rotation is given in ``desired_str``,
    it still uses the default from the configuration.
    '''
    if desired_str is None:
        if not ThinkpadAcpi.inTabletMode():
            new = translate_direction(config['rotate']['default_rotation'])
            logger.info(_('Using default, setting to {}').format(new))
        else:
            new = NORMAL
            logger.info(_('Using default, setting to {}').format(new))
    elif desired_str.startswith('cycle'):
        new = cycle_rotation(current, desired_str != 'cycle-ccw')
        logger.info(_('User chose to set to {}').format(new))
    else:
        desired = translate_direction(desired_str)
        if desired == current and not force:
            new = NORMAL
            logger.info(_('You try to rotate into the direction it is, '
                          'reverting to normal.'))
        else:
            new = desired
            logger.info(_('User chose to set to {}').format(new))
    return new
