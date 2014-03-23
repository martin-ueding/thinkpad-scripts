#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

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
    if os.path.isfile(hook):
        tps.call([hook, direction.xrandr], logger)

def postrotate(direction, config):
    '''
    Executes postrotate hook if it exists.

    :param tps.Direction direction: Desired direction
    :param configparser.ConfigParser config: Global config
    :returns: None
    '''
    hook = os.path.expanduser(config['hooks']['postrotate'])
    if os.path.isfile(hook):
        tps.call([hook, direction.xrandr], logger)

def predock(state, config):
    '''
    Executes predock hook if it exists.

    :param bool state: Whether new state is on
    :param configparser.ConfigParser config: Global config
    :returns: None
    '''
    hook = os.path.expanduser(config['hooks']['predock'])
    if os.path.isfile(hook):
        tps.call([hook, 'on' if state else 'off'], logger)

def postdock(state, config):
    '''
    Executes postdock hook if it exists.

    :param bool state: Whether new state is on
    :param configparser.ConfigParser config: Global config
    :returns: None
    '''
    hook = os.path.expanduser(config['hooks']['postdock'])
    if os.path.isfile(hook):
        tps.call([hook, 'on' if state else 'off'], logger)

def get_graphicsl_user():
    pattern = re.compile(r'\(:0(\.0)?\)')

    lines = tps.check_output(['who', '-u'], logger).decode().split('\n')
    for line in lines:
        m = pattern.search(line)
        if m:
            words = line.split()
            return words[0]

def main_rotate_hook():
    parser = argparse.ArgumentParser()
    parser.add_argument('key', help='Keycode')
    parser.add_argument("-v", dest='verbose', action="count", help='Enable verbose output. Can be supplied multiple times for even more verbosity.')
    options = parser.parse_args()
    tps.config.set_up_logging(options.verbose)

    key = options.key

    if key in ('00000001', '00005009'):
        set_to = ''

    elif key in ('00000000', '0000500a'):
        set_to = 'normal'

    tps.check_call([
        'sudo', '-u', get_graphicsl_user(), '-i',
        'env', 'DISPLAY=:0.0',
        '/usr/bin/thinkpad-rotate', set_to
    ], logger)
