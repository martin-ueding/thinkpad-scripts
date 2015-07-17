#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Network support.
'''

import glob
import logging
import re

import tps

logger = logging.getLogger(__name__)


class MissingEthernetException(Exception):
    '''
    This exception is raised when NetworkManager has no configured Ethernet
    connections as reported by ``nmcli con list``.
    '''


def parse_terse_line(output):
    '''
    Split output line from nmcli called with the --terse option into a list and
    remove backslashes that escape ':' and '\\'.

    :param str output: Output from nmcli
    :returns: The split output with backslash escapes removed
    '''
    # Split string on non-escaped ':'; regular expression based on
    # http://stackoverflow.com/a/8435588
    split = re.findall(r'((?:[^:\\]|\\.)+):?', output)
    # Remove '\' used to escape ':' or '\'
    for i in range(len(split)):
        split[i] = re.sub(r'\\([\\:])', r'\1', split[i])
    return split


def get_nmcli_version():
    '''
    Gets the version of nmcli, removing trailing zeroes.

    :returns: tuple, e.g. (0, 9, 10) for version 0.9.10.0
    '''
    if not tps.has_program('nmcli'):
        logger.warning('nmcli is not installed')
        return

    response = tps.check_output(['nmcli', '--version'], logger).decode()
    version_str = re.search(r'\d+(\.\d+)*', response).group(0)
    version_list = [int(n) for n in version_str.split('.')]
    while version_list[-1] == 0:
        version_list.pop()
    return tuple(version_list)


def set_wifi(state):
    '''
    Sets the wifi hardware to the given state.

    :param bool state: Desired state
    :returns: None
    '''
    if not tps.has_program('nmcli'):
        logger.warning('nmcli is not installed')
        return

    if get_nmcli_version() >= (0, 9, 10):
        command = ['nmcli', 'radio', 'wifi', 'on' if state else 'off']
    else:
        command = ['nmcli', 'nm', 'wifi', 'on' if state else 'off']
    tps.check_call(command, logger)


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


def get_ethernet_con_name():
    '''
    Gets the lexicographically first ethernet connection name from nmcli.

    :returns: str
    :raises tps.network.MissingEthernetException:
    '''
    if not tps.has_program('nmcli'):
        logger.warning('nmcli is not installed')
        return

    if get_nmcli_version() >= (0, 9, 10):
        command = ['nmcli', '--terse', '--fields', 'NAME,TYPE', 'con', 'show']
    else:
        command = ['nmcli', '--terse', '--fields', 'NAME,TYPE', 'con', 'list']
    lines = tps.check_output(command, logger).decode()
    ethernet_cons = []
    for line in lines.split('\n'):
        if line.strip():
            name, type = parse_terse_line(line)
            if 'ethernet' in type.lower():
                ethernet_cons.append(name)
    if ethernet_cons:
        return sorted(ethernet_cons)[0]
    else:
        raise MissingEthernetException('No configured Ethernet connections.')


def restart(connection):
    '''
    Disables and enables the given connection if it exists.

    :param str connection: Name of the connection
    :returns: None
    '''
    if not tps.has_program('nmcli'):
        logger.warning('nmcli is not installed')
        return

    tps.check_call(['nmcli', 'con', 'up', 'id', connection], logger)
