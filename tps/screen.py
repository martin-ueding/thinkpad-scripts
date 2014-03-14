#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Screen related logic.
'''

import subprocess
import logging

logger = logging.getLogger(__name__)

def get_rotation(screen):
    '''
    Gets the current rotation of the given screen.
    '''
    logger.error('get_rotation() not implemented')

def get_external():
    '''
    Gets the external screen.
    '''
    logger.error('get_external() not implemented')

def rotate(screen, direction):
    '''
    Rotates the screen into the direction.
    '''
    logger.error('rotate() not implemented')

def set_subpixel_order(direction):
    '''
    Sets the text subpixel anti-alias order.
    '''
    logger.error('set_subpixel_order() not implemented')

def set_brightness(brightness):
    logger.error('set_brightness() not implemented')

def set_primary(screen):
    logger.error('set_primary() not implemented')

def disable_external():
    logger.error('disable_external() not implemented')

