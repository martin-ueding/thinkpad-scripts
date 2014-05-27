#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2014 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

'''
Main module for thinkpad-scripts.
'''

import collections
import functools
import subprocess
import logging
import os

Direction = collections.namedtuple('Direction', ['xrandr', 'xsetwacom',
                                                 'subpixel'])
'''
Holds the direction names of different tools.

``xrandr`` and ``xsetwacom`` use different names for the rotations. To avoid
proliferation of various names, this class holds the differing names. The
module provides four constants which have to be used within :mod:`tps`.
'''

Direction.__repr__ = lambda d: d.xrandr

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
    def is_exe(path):
        return os.path.isfile(path) and os.access(path, os.X_OK)

    # Check if `command` is a path to an executable
    if os.sep in command:
        if is_exe(os.path.expanduser(command)):
            logger.debug('Command “{}” found.'.format(command))
            return True

    # Check if `command` is an executable on PATH
    else:
        for dir in os.get_exec_path():
            if is_exe(os.path.join(dir, command)):
                logger.debug('Command “{}” found.'.format(command))
                return True

    logger.debug('Command “{}” not found.'.format(command))
    return False

def print_command_decorate(function):
    '''
    Decorates a func from the subprocess module to log the `command` parameter.

    Note that the wrapper adds an additional `local_logger` parameter following
    the `command` parameter that is used for the logging. All other parameters
    are passed to the wrapped function.

    :param function: Function to wrap
    :returns: Decorated function
    '''
    @functools.wraps(function)
    def wrapper(command, local_logger, *args, **kwargs):
        local_logger.debug('subprocess “{}”'.format(' '.join(command)))
        return function(command, *args, **kwargs)
    return wrapper

check_call = print_command_decorate(subprocess.check_call)
call = print_command_decorate(subprocess.call)
check_output = print_command_decorate(subprocess.check_output)
