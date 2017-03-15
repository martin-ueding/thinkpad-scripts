#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
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
    lines = tps.check_output(['who', '-u'], logger)\
               .decode().strip().split('\n')
    return parse_graphical_user(lines)


def parse_graphical_user(lines):
    '''Determine the graphical user from the output of ``who -u``.'''
    # If there is a single user, choose them.
    if len(lines) == 1:
        return lines[0].split()[0]
    # Otherwise, search for a user description that matches the regex.
    # 'z' is always greater than any match by the regular expression.
    display = 'z'
    user = None
    for line in lines:
        m = re.search(r'\(:\d+(\.\d+)?\)', line)
        if m and m.group(0) < display:
            display = m.group(0)
            user = line.split()[0]
    return user


def main_rotate_hook():
    '''
    Entry point for ``thinkpad-rotate-hook``.

    It interprets the key values from the caller and start up another
    interpreter with the actual ``thinkpad-rotate`` script.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('direction', nargs='?', help='Direction to rotate to.')
    parser.add_argument('--via-hook', required=True,
                        help='ID of hook that called this program')
    parser.add_argument("-v", dest='verbose', action="count",
                        help='Enable verbose output. Can be supplied multiple '
                             'times for even more verbosity.')
    options = parser.parse_args()
    tps.config.set_up_logging(options.verbose)

    if options.direction is not None:
        direction = [options.direction, '--force-direction']
    else:
        direction = []

    user = get_graphicsl_user()
    if user is None:
        logger.warning('Unable to get graphical user. Ignoring trigger.')
        sys.exit(0)

    tps.check_call(
        ['sudo', '-u', user, '-i',
         'env', 'DISPLAY=:0.0',
         '/usr/bin/thinkpad-rotate'] +
        direction +
        ['--via-hook', options.via_hook],
        logger)


def main_dock_hook():
    '''
    Entry point for ``thinkpad-dock-hook``.

    It interprets the key values from the caller and start up another
    interpreter with the actual ``thinkpad-dock`` script.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs='?', choices=['on', 'off'],
                        help='`on` or `off`')
    parser.add_argument('--via-hook', required=True,
                        help='ID of hook that called this program')
    parser.add_argument("-v", dest='verbose', action="count",
                        help='Enable verbose output. Can be supplied multiple '
                             'times for even more verbosity.')
    options = parser.parse_args()
    tps.config.set_up_logging(options.verbose)

    if options.action is not None:
        action = [options.action]
    else:
        action = []

    user = get_graphicsl_user()
    if user is None:
        logger.warning('Unable to get graphical user. Ignoring trigger.')
        sys.exit(0)

    tps.check_call(
        ['sudo', '-u', user, '-i',
         'env', 'DISPLAY=:0.0',
         '/usr/bin/thinkpad-dock'] +
        action +
        ['--via-hook', options.via_hook],
        logger)
