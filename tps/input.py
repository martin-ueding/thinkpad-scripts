#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic related to input devices.
'''

import logging
import re
import subprocess

logger = logging.getLogger(__name__)

def get_wacom_device_ids():
    '''
    :rtype: list
    '''
    pattern = re.compile(rb'Wacom ISD.*id: (\d+).*')
    output = subprocess.check_output(['xsetwacom', 'list', 'devices'])
    lines = output.split(b'\n')
    ids = []
    for line in lines:
        matcher = pattern.match(line)
        if matcher:
            ids.append(int(matcher.group(1)))
    return ids

if __name__ == '__main__':
    print(get_wacom_device_ids())
