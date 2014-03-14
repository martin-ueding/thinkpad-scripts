#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

import logging
import os.path
import subprocess

logger = logging.getLogger(__name__)

def prerotate(direction, config):
    hook = os.path.expanduser(config['hooks']['prerotate'])
    if os.path.isfile(hook):
        subprocess.call([hook, direction.xrandr])

def postrotate(direction, config):
    hook = os.path.expanduser(config['hooks']['postrotate'])
    if os.path.isfile(hook):
        subprocess.call([hook, direction.xrandr])

def predock(on, config):
    hook = os.path.expanduser(config['hooks']['predock'])
    if os.path.isfile(hook):
        subprocess.call([hook, 'on' if on else 'off'])

def postdock(on, config):
    hook = os.path.expanduser(config['hooks']['postdock'])
    if os.path.isfile(hook):
        subprocess.call([hook, 'on' if on else 'off'])
