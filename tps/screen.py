#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Screen related logic.
'''

import subprocess
import re
import logging

import tps

logger = logging.getLogger(__name__)

def get_rotation(screen):
    '''
    Gets the current rotation of the given screen.

    :param str screen: Find rotation of given output
    :returns: Current direction
    :rtype: tps.Direction
    '''
    command = ['xrandr', '-q', '--verbose']
    logger.debug(' '.join(command))
    output = subprocess.check_output(command).decode()
    lines = output.split('\n')
    for line in lines:
        if screen in line:
            matcher = re.search(r'\) (normal|left|inverted|right) \(', line)
            if matcher:
                rotation = tps.translate_direction(matcher.group(1))
                logger.info('Current rotation is “{}”.'.format(rotation))
                return rotation

def get_external(internal):
    '''
    Gets the external screen.

    You have to specify the internal screen to exclude that from the listing.
    This returns the first external screen. Since you could possibly have
    multiple, this might be adjusted. The graphics card in the X220 (Intel HD
    3000) can only use two screens, so this might be okay right here.

    ;param str internal: Name of the internal screen
    :returns: External screen name
    :rtype: str
    '''
    lines = subprocess.check_output(['xrandr']).decode().split('\n')
    for line in lines:
        if not line.startswith(internal):
            matcher = re.search(r'^(\S+) connected', line)
            if matcher:
                return matcher.group(1)

def rotate(screen, direction):
    '''
    Rotates the screen into the direction.

    :param str screen: Name of the output to rotate
    :param tps.Direction direction: New direction
    :returns: None
    '''
    command = ['xrandr', '--output', screen, '--rotate', direction.xrandr]
    logger.debug(' '.join(command))
    subprocess.check_call(command)

def set_subpixel_order(direction):
    '''
    Sets the text subpixel anti-alias order.

    :param tps.Direction direction: New direction
    :returns: None
    '''
    command = ['gsettings', 'set',
               'org.gnome.settings-daemon.plugins.xsettings', 'rgba-order',
               direction.subpixel]
    logger.debug(' '.join(command))
    subprocess.check_call(command)

def set_brightness(brightness):
    '''
    Sets the brightness with ``xbacklight``.

    :param str brightness: Percent value of brightness, e. g. ``60%``
    :returns: None
    '''
    if not tps.has_program('xbacklight'):
        logger.warning('xbacklight is not installed')
        return

    command = ['xbacklight', '-set', brightness]
    logger.debug(' '.join(command))
    subprocess.check_call(command)

def disable(screen):
    '''
    Disables the given screen using ``xrandr``.

    :param str screen: Name of the output to disable
    :returns: None
    '''
    command = ['xrandr', '--output', screen, '--off']
    logger.debug(' '.join(command))
    subprocess.check_call(command)

def enable(screen, primary=False, position=None):
    '''
    Enables given screen using ``xrandr``.

    :param str screen: Name of the output to enable
    :param bool primary: Set output as primary
    :param tuple position: Tuple with (0) relative position and (1) other
        output. This could be ``('right-of', 'LVDS1')``.
    :returns: None
    '''
    command = ['xrandr', '--output', screen, '--auto']

    if position is not None:
        command += ['--{}'.format(position[0]), position[1]]

    if primary:
        command += ['--primary']

    logger.debug(' '.join(command))
    subprocess.check_call(command)
