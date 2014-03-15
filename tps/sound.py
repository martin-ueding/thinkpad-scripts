#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic for sound.
'''

import logging
import subprocess

import tps

logger = logging.getLogger(__name__)

def unmute(loudness):
    '''
    Unmutes the speakers and sets them to the given loudness.
    '''
    if not tps.has_program('pactl'):
        logger.warning('pactl is not installed')
        return

    command = ['pactl', 'set-sink-volume', '0', loudness]
    logger.debug(' '.join(command))
    subprocess.check_call(command)

    command = ['pactl', 'set-sink-mute', '0', '0']
    logger.debug(' '.join(command))
    subprocess.check_call(command)

def set_volume(loudness):
    '''
    Sets the volume to the given loudness.
    '''
    logger.error('set_volume() not implemented')
