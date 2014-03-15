#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic for Ubuntu Unity.
'''

import logging

import tps

logger = logging.getLogger(__name__)

def set_launcher(autohide):
    if not tps.has_program('dconf'):
        logger.warning('dconf is not installed')
        return

    set_to = '1' if autohide else '0'
    tos.check_call(['dconf', 'write',
                    '/org/compiz/profiles/unity/plugins/unityshell/launcher-hide-mode',
                    set_to], logger)

