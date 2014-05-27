#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic for sound.
'''

import argparse
import logging

import tps
import tps.config

logger = logging.getLogger(__name__)

def unmute(loudness):
    '''
    Unmutes the speakers and sets them to the given loudness.

    :param str loudness: Loudness value as string with percent
    '''
    if not tps.has_program('pactl'):
        logger.warning('pactl is not installed')
        return

    tps.check_call(['pactl', 'set-sink-volume', '0', loudness], logger)
    tps.check_call(['pactl', 'set-sink-mute', '0', '0'], logger)

def set_volume(loudness):
    '''
    Sets the volume to the given loudness.

    :param str loudness: Loudness value as string with percent
    '''
    if not tps.has_program('pactl'):
        logger.warning('pactl is not installed')
        return

    tps.check_call(['pactl', 'set-sink-volume', '0', loudness], logger)

def main_mutemic():
    '''
    Entry point for ``thinkpad-mutemic``.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", dest='verbose', action="count",
                        help='Enable verbose output. Can be supplied multiple '
                             'times for even more verbosity.')
    options = parser.parse_args()
    tps.config.set_up_logging(options.verbose)

    tps.check_call(['amixer', 'sset', "'Capture',0", 'toggle'], logger)
