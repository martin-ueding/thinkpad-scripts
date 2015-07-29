#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2014 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic for virtual keyboard
'''

import logging
import subprocess

import tps

logger = logging.getLogger(__name__)


def toggle(program, state):
    '''
    Toggles the running state of the given progam.

    If state is true, the program will be spawned.

    :param str program: Name of the program
    :param bool state: Desired state
    :returns: None
    '''
    if state:
        try:
            tps.check_output(['pgrep', program], logger)
        except subprocess.CalledProcessError:
            if tps.has_program(program):
                logger.debug(program)
                subprocess.Popen([program])
            else:
                logger.warning('{} is not installed'.format(program))
    else:
        try:
            tps.check_output(['pgrep', program], logger)
            tps.check_call(['killall', program], logger)
        except subprocess.CalledProcessError:
            pass
