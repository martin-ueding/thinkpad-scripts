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
    #subprocess.check_output(['xrandr', '-q', '--verbose'])

def rotate(screen, direction):
    logger.error('rotate() not implemented')
