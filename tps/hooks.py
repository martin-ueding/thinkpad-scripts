#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2015 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

'''
Functions that execute the appropriate hooks.
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


def prerotate(direction, config):
    '''
    Executes prerotate hook if it exists.

    :param tps.Direction direction: Desired direction
    :param configparser.ConfigParser config: Global config
    :returns: None
    '''
    hook = os.path.expanduser(config['hooks']['prerotate'])
    if tps.has_program(hook):
        tps.call([hook, direction.xrandr], logger)


def postrotate(direction, config):
    '''
    Executes postrotate hook if it exists.

    :param tps.Direction direction: Desired direction
    :param configparser.ConfigParser config: Global config
    :returns: None
    '''
    hook = os.path.expanduser(config['hooks']['postrotate'])
    if tps.has_program(hook):
        tps.call([hook, direction.xrandr], logger)


def predock(state, config):
    '''
    Executes predock hook if it exists.

    :param bool state: Whether new state is on
    :param configparser.ConfigParser config: Global config
    :returns: None
    '''
    hook = os.path.expanduser(config['hooks']['predock'])
    if tps.has_program(hook):
        tps.call([hook, 'on' if state else 'off'], logger)


def postdock(state, config):
    '''
    Executes postdock hook if it exists.

    :param bool state: Whether new state is on
    :param configparser.ConfigParser config: Global config
    :returns: None
    '''
    hook = os.path.expanduser(config['hooks']['postdock'])
    if tps.has_program(hook):
        tps.call([hook, 'on' if state else 'off'], logger)


def get_graphicsl_user():
    '''
    Get the currently logged in user.

    First it will try ``who -u`` and parse the output. Since this does not give
    a result in every case (see GH-107__), we also use ``pgrep`` to search for
    the user of the currently running instance of X.org.

    __ https://github.com/martin-ueding/thinkpad-scripts/issues/107
    '''
    #pattern = re.compile(r'\(:0(\.0)?\)')

    #lines = tps.check_output(['who', '-u'], logger).decode().split('\n')
    #for line in lines:
    #    m = pattern.search(line)
    #    if m:
    #        words = line.split()
    #        return words[0]


    # We reached this point without returning yet. Therefore `who -u` did not
    # yield any usable result. We will have to make another try to guess the
    # currently logged in user. See GH-107 for more details.

    pgrep_output = tps.check_output([
        'pgrep', '-f',
        r'^/usr/(local/)?(bin|lib)/([^[:blank:]]+/)?(Xorg|X)([[:blank:]]+|$)'],
        logger)
    pids = pgrep_output.decode().strip().split()

    logger.debug('pgrep gave PIDs: %s', ', '.join(pids))

    if len(pids) > 1:
        logger.error('There are two instances of X.org running. I cannot '
                     'decide which is the user which should have the script '
                     'executed on behalf. PIDs are %s', ', '.join(pids))
        sys.exit(1)

    if len(pids) == 0:
        logger.error('No X.org seems to be running.')
        sys.exit(1)

    ps_output = tps.check_output(['ps', '--no-headers', '--format=ruser',
                                 pids[0]], logger)
    uid_str = ps_output.decode().strip()

    if uid_str == 'root':
        logger.error('X server is running as root. User cannot be determined this way.')
        sys.exit(1)

    return uid_str



def main_rotate_hook():
    '''
    Entry point for ``thinkpad-rotate-hook``.

    It interprets the key values from the caller and start up another
    interpreter with the actual ``thinkpad-rotate`` script.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('ignored_one')
    parser.add_argument('ignored_two')
    parser.add_argument('ignored_three')
    parser.add_argument('key', help='Keycode')
    parser.add_argument("-v", dest='verbose', action="count",
                        help='Enable verbose output. Can be supplied multiple '
                             'times for even more verbosity.')
    options = parser.parse_args()
    tps.config.set_up_logging(options.verbose)

    key = options.key

    if key in ('00000001', '00005009'):
        set_to = ''

    elif key in ('00000000', '0000500a'):
        set_to = 'normal'

    else:
        logger.error('Unexpected keycode %s given in rotate-hook', key)
        sys.exit(1)

    tps.check_call([
        'sudo', '-u', get_graphicsl_user(), '-i',
        'env', 'DISPLAY=:0.0',
        '/usr/bin/thinkpad-rotate', set_to, '--via-hook',
    ], logger)


def main_dock_hook():
    '''
    Entry point for ``thinkpad-dock-hook``.

    It interprets the key values from the caller and start up another
    interpreter with the actual ``thinkpad-dock`` script.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='`on` or `off`')
    parser.add_argument("-v", dest='verbose', action="count",
                        help='Enable verbose output. Can be supplied multiple '
                             'times for even more verbosity.')
    options = parser.parse_args()
    tps.config.set_up_logging(options.verbose)

    tps.check_call([
        'sudo', '-u', get_graphicsl_user(), '-i',
        'env', 'DISPLAY=:0.0',
        '/usr/bin/thinkpad-dock', options.action
    ], logger)

if __name__ == '__main__':
    print(get_graphicsl_user())
