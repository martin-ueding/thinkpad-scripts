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
    options = parser.parse_args()

    key = options.key

    if key in ('00000001', '00005009'):
        set_to = ''

    elif key in ('00000000', '0000500a'):
        set_to = 'normal'

    command = 'su -c "env DISPLAY=:0.0 /usr/bin/thinkpad-rotate {set_to}" --login "{user}" & disown'.format(user=get_graphicsl_user(), set_to=set_to)
    logger.debug('subprocess “{}”'.format(command))
    subprocess.call(command, shell=True)
