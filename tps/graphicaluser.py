#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2015 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

'''
Attempts to find the currently logged in user using the graphical session.
'''

import argparse
import logging
import os.path
import re
import subprocess
import sys

import tps
import tps.config

logger = logging.getLogger(__name__)

def get():
    '''
    Get the currently logged in user.

    This uses the various methods implemented in this module automatically
    until a sensible result is found.
    '''
    methods = [
        _get_who,
        _get_pgrep,
    ]

    for method in methods:
        result = method()
        if result is not None:
            return result

    return None


def _get_who():
    '''
    Get the currently logged in user via ``who -u``.
    '''
    pattern = re.compile(r'\(:0(\.0)?\)')

    lines = tps.check_output(['who', '-u'], logger).decode().split('\n')
    for line in lines:
        m = pattern.search(line)
        if m:
            words = line.split()
            return words[0]

    logger.warning('Could not determine user with `who -u`.')
    return None


def _get_pgrep():
    '''
    Get the currently logged in user by searching for X.org user.

    Since ``who -u`` does not give a result in every case (see GH-107__), we
    also use ``pgrep`` to search for the user of the currently running instance
    of X.org.

    __ https://github.com/martin-ueding/thinkpad-scripts/issues/107
    '''
    pgrep_output = tps.check_output([
        'pgrep', '-f',
        r'^/usr/(local/)?(bin|lib)/([^[:blank:]]+/)?(Xorg|X)([[:blank:]]+|$)'],
        logger)
    pids = pgrep_output.decode().strip().split()

    logger.debug('pgrep gave PIDs: %s', ', '.join(pids))

    if len(pids) > 1:
        logger.warning('There are two instances of X.org running. I cannot '
                       'decide which is the user which should have the script '
                       'executed on behalf. PIDs are %s', ', '.join(pids))
        return None

    if len(pids) == 0:
        logger.warning('No X.org seems to be running.')
        return None

    ps_output = tps.check_output(['ps', '--no-headers', '--format=euser',
                                 pids[0]], logger)
    uid_str = ps_output.decode().strip()

    if uid_str == 'root':
        logger.warning('X server is running as root. User cannot be determined this way.')
        return None

    return uid_str

if __name__ == '__main__':
    print(get())
