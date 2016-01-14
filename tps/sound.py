#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic for sound.
'''

import logging
import re

import tps
import tps.config

logger = logging.getLogger(__name__)


def get_pulseaudio_sinks():
    '''
    Retrieves the available PulseAudio sinks on the current system
    and returns them in a set of strings

    :returns: List of sinks. If ``pactl`` is not installed, an empty list is
    returned instead.
    :rtype: list of str
    '''
    if not tps.has_program('pactl'):
        logger.warning('pactl is not installed')
        return []

    output = tps.check_output(['pactl', 'list', 'sinks'], logger).decode()
    sinks = re.findall('^Sink #(\d+)$', output, flags=re.MULTILINE)
    return sinks


def unmute(loudness):
    '''
    Unmutes the speakers and sets them to the given loudness.

    :param str loudness: Loudness value as string with percent
    '''
    sinks = get_pulseaudio_sinks()
    for sink in sinks:
        tps.check_call(['pactl', 'set-sink-mute', sink, '0'], logger)

    set_volume(loudness)


def set_volume(loudness):
    '''
    Sets the volume to the given loudness.

    :param str loudness: Loudness value as string with percent
    '''
    sinks = get_pulseaudio_sinks()
    for sink in sinks:
        tps.check_call(['pactl', 'set-sink-volume', sink, loudness], logger)

if __name__ == '__main__':
    print(get_pulseaudio_sinks())
