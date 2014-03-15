#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

import logging
import os.path

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
