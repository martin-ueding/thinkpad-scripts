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
    if not tps.has_program('pactl'):
        logger.warning('pactl is not installed')
        return

    subprocess.check_call(['pactl', 'set-sink-volume', '0', loudness])
    subprocess.check_call(['pactk', 'set-sink-mute', '0', '0'])
