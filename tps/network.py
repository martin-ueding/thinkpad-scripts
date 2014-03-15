#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Network support.
'''

import glob
import logging

import tps

logger = logging.getLogger(__name__)

def set_wifi(state):
    '''
    Sets the wifi hardware to the given state.

    :param bool state: Desired state
    :returns: None
    '''
    if not tps.has_program('nmcli'):
        logger.warning('nmcli is not installed')
        return

    tps.check_call(['nmcli', 'nm', 'wifi', 'on' if state else 'off'], logger)

def has_ethernet():
    '''
    Checks whether there is an ethernet connection.

    It evalues the files in ``/sys/class/net/e*/carrier`` and checks whether
    one of them contains a ``1``.

    It does not make sense to disable the wireless connection if there is no
    wired connection available.

    :returns: None
    '''
    carrierfiles = glob.glob('/sys/class/net/e*/carrier')
    for carrierfile in carrierfiles:
        with open(carrierfile) as handle:
            contents = handle.read()
            carrier_state = int(contents) == 1
            if carrier_state:
                return True
    return False

def restart(connection):
    '''
    Disables and enables the given connection if it exists.

    :param str connection: Name of the connection
    :returns: None
    '''
    if not tps.has_program('nmcli'):
        logger.warning('nmcli is not installed')

    tps.check_call(['nmcli', 'con', 'down', 'id', connection], logger)
    tps.check_call(['nmcli', 'con', 'up', 'id', connection], logger)
