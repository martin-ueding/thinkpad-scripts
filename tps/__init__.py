#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import collections
import subprocess
import logging

Direction = collections.namedtuple('Direction', ['xrandr', 'xsetwacom',
                                                 'subpixel'])
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

logger = logging.getLogger(__name__)

class UnknownDirectionException(Exception):
    '''
    Unknown direction given at the command line.
    '''

def translate_direction(direction):
    '''
    :param str direction: Direction string
    :returns: Direction object
    :rtype: tps.Direction
    :raises tps.UnknownDirectionException:
    '''

    if direction == 'normal':
        result = NORMAL

    elif direction == 'left':
        result = LEFT

    elif direction == 'right':
        result = RIGHT

    elif direction == 'flip':
        result = INVERTED
    elif direction == 'inverted':
        result = INVERTED

    else:
        raise UnknownDirectionException('Direction “{}” cannot be understood.'.format(direction))

    logger.debug('Converted “{}” to “{}”.'.format(direction, result))

    return result

def has_program(command):
    '''
    Checks whether given program is installed on this computer.

    :param str command: Name of command
    :returns: Whether program is installed
    :rtype: bool
    '''
    try:
        subprocess.check_output(['which', command])
        logger.debug('Command “{}” found via “which”.'.format(command))
        return True
    except subprocess.CalledProcessError:
        logger.debug('Command “{}” not found via “which”.'.format(command))
        return False

def check_call(command, local_logger):
    '''
    Calls subprocess.check_call, but prints the command first.

    :param list command: Command suitable for subprocess module
    :param logging.Logger local_logger: Logger of the using module
    :returns: None
    '''
    print_command(command, local_logger)
    subprocess.check_call(command)

def call(command, local_logger):
    '''
    Calls subprocess.call, but prints the command first.

    :param list command: Command suitable for subprocess module
    :param logging.Logger local_logger: Logger of the using module
    :returns: Return value of command
    :rtype: int
    '''
    print_command(command, local_logger)
    return subprocess.call(command)

def check_output(command, local_logger):
    '''
    Calls subprocess.check_output, but prints the command first.

    :param list command: Command suitable for subprocess module
    :param logging.Logger local_logger: Logger of the using module
    :returns: Command output
    :rtype: bytes
    '''
    print_command(command, local_logger)
    return subprocess.check_output(command)

def print_command(command, local_logger):
    '''
    Prints the command to the debug output of the logger.

    :param list command: Command suitable for subprocess module
    :param logging.Logger local_logger: Logger of the using module
    :returns: None
    '''
    local_logger.debug('subprocess “{}”'.format(' '.join(command)))
