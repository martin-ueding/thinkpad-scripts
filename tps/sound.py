#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic for sound.
'''

import logging

import tps

logger = logging.getLogger(__name__)

def unmute(loudness):
    '''
    Unmutes the speakers and sets them to the given loudness.
    '''
    if not tps.has_program('pactl'):
        logger.warning('pactl is not installed')
        return

    tps.check_call(['pactl', 'set-sink-volume', '0', loudness], logger)
    tps.check_call(['pactl', 'set-sink-mute', '0', '0'], logger)

def set_volume(loudness):
    '''
    Sets the volume to the given loudness.
    '''
    if not tps.has_program('pactl'):
        logger.warning('pactl is not installed')
        return

    tps.check_call(['pactl', 'set-sink-volume', '0', loudness], logger)
