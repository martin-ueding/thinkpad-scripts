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
    '''
    command = ['xrandr', '--output', screen, '--rotate', direction.xrandr]
    logger.debug(' '.join(command))
    subprocess.check_call(command)

def set_subpixel_order(direction):
    '''
    Sets the text subpixel anti-alias order.

    :type direction: tps.Direction
    '''
    command = ['gsettings', 'set',
               'org.gnome.settings-daemon.plugins.xsettings', 'rgba-order',
               direction.subpixel]
    logger.debug(' '.join(command))
    subprocess.check_call(command)

def set_brightness(brightness):
    if not tps.has_program('xbacklight'):
        logger.warning('xbacklight is not installed')
        return

    command = ['xbacklight', '-set', brightness]
    logger.debug(' '.join(command))
    subprocess.check_call(command)

def disable(screen):
    '''
    Disables the given screen using ``xrandr``.

    :rype: None
    '''
    command = ['xrandr', '--output', screen, '--off']
    logger.debug(' '.join(command))
    subprocess.check_call(command)

def enable(screen, primary=False, position=None):
    command = ['xrandr', '--output', screen, '--auto']

    if position is not None:
        command += ['--{}'.format(position[0]), position[1]]

    if primary:
        command += ['--primary']

    logger.debug(' '.join(command))
    subprocess.check_call(command)
