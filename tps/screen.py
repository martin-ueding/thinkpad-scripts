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
    output = subprocess.check_output(['xrandr', '-q', '--verbose']).decode()
    lines = output.split('\n')
    for line in lines:
        if screen in line:
            matcher = re.search(r'\) (normal|left|inverted|right) \(', line)
            if matcher:
                rotation = tps.translate_direction(matcher.group(1))
                logger.info('Current rotation is “{}”.'.format(rotation))
                return rotation

def get_external():
    '''
    Gets the external screen.
    '''
    logger.error('get_external() not implemented')

def rotate(screen, direction):
    '''
    Rotates the screen into the direction.
    '''
    subprocess.check_call(['xrandr', '--output', screen, '--rotate',
                           direction.xrandr])

def set_subpixel_order(direction):
    '''
    Sets the text subpixel anti-alias order.
    '''
    subprocess.check_call(['gsettings', 'set',
                           'org.gnome.settings-daemon.plugins.xsettings',
                           'rgba-order', direction.subpixel])

def set_brightness(brightness):
    logger.error('set_brightness() not implemented')

def set_primary(screen):
    logger.error('set_primary() not implemented')

def disable_external():
    logger.error('disable_external() not implemented')

