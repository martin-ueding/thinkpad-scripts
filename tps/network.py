#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Network support.
'''

import logging

import tps

logger = logging.getLogger(__name__)

def set_wifi(on):
    '''
    Sets the wifi hardware to the given state.

    :param bool on: Desired state
    :returns: None
    '''
    if not tps.has_program('nmcli'):
        logger.warning('nmcli is not installed')
        return

    tps.check_call(['nmcli', 'nm', 'wifi', 'on' if on else 'off'], logger)

def restart(connection):
    '''
    Disables and enables the given connection if it exists.

    :param str connection: Name of the connection
    :returns: None
    '''
    logger.error('restart() not implemented')
