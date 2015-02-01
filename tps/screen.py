#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2015 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

'''
Screen related logic.
'''

import logging
import re
import subprocess

import tps

logger = logging.getLogger(__name__)

def get_rotation(screen):
    '''
    Gets the current rotation of the given screen.

    :param str screen: Find rotation of given output
    :returns: Current direction
    :rtype: tps.Direction
    '''
    output = tps.check_output(['xrandr', '-q', '--verbose'], logger).decode()
    lines = output.split('\n')
    for line in lines:
        if screen in line:
            matcher = re.search(r'\) (normal|left|inverted|right) \(', line)
            if matcher:
                rotation = tps.translate_direction(matcher.group(1))
                logger.info('Current rotation is “{}”.'.format(rotation))
                return rotation

    # At this point, nothing was found in the xrandr output.
    logger.error('Rotation of screen "%s" could not be determined. Do you have a screen like that in the output of "xrandr"? Maybe you have to adjust the option of screen.internal in the configuration.', screen)

def get_externals(internal):
    '''
    Gets the external screens.

    You have to specify the internal screen to exclude that from the listing.

    ;param str internal: Name of the internal screen
    :returns: List of external screen names
    :rtype: str
    '''
    externals = []
    lines = tps.check_output(['xrandr'], logger).decode().split('\n')
    for line in lines:
        if not line.startswith(internal):
            matcher = re.search(r'^(\S+) connected', line)
            if matcher:
                externals.append(matcher.group(1))
    return externals

def rotate(screen, direction):
    '''
    Rotates the screen into the direction.

    :param str screen: Name of the output to rotate
    :param tps.Direction direction: New direction
    :returns: None
    '''
    tps.check_call(['xrandr', '--output', screen, '--rotate',
                    direction.xrandr], logger)

def set_subpixel_order(direction):
    '''
    Sets the text subpixel anti-alias order.

    :param tps.Direction direction: New direction
    :returns: None
    '''
    if tps.has_program('xfconf-query'):
        try:
            tps.check_call(['xfconf-query', '-c', 'xsettings', '-p', '/Xft/RGBA',
                        '-s', direction.subpixel], logger)
        except subprocess.CalledProcessError as e:
            logger.error(e)

    elif tps.has_program('gsettings'):
        try:
            schemas = tps.check_output(
                ['gsettings', 'list-schemas']).decode().split('\n')
            schema = 'org.gnome.settings-daemon.plugins.xsettings'
            if schema in schemas:
                tps.check_call(['gsettings', 'set', schema, 'rgba-order',
                                direction.subpixel], logger)
            else:
                logger.warning('gsettings is installed, but the "{}" schema '
                               'is not available'.format(schema))
        except subprocess.CalledProcessError as e:
            logger.error(e)
    else:
        logger.warning('neither xfconf-query nor gsettings is installed')

def set_brightness(brightness):
    '''
    Sets the brightness with ``xbacklight``.

    :param str brightness: Percent value of brightness, e. g. ``60%``
    :returns: None
    '''
    if not tps.has_program('xbacklight'):
        logger.warning('xbacklight is not installed')
        return

    tps.check_call(['xbacklight', '-set', brightness], logger)

def disable(screen):
    '''
    Disables the given screen using ``xrandr``.

    :param str screen: Name of the output to disable
    :returns: None
    '''
    tps.check_call(['xrandr', '--output', screen, '--off'], logger)

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

    tps.check_call(command, logger)
