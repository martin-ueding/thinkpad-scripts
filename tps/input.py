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
    Gets the IDs of the Wacom® touch devices.

    This calls ``xsetwacom list devices`` to get the list and parses that with regular expressions 

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

def rotate_wacom_device(device, direction):
    '''
    Rotates a Wacom® device.

    :type device: int
    :type direction: tps.Direction
    '''
    subprocess.check_call(['xsetwacom', 'set', str(device), 'rotate',
                           direction.xsetwacom])

def map_wacom_device_to_output(device, output):
    '''
    Maps a Wacom® device to a specific output.

    :type device: int
    :type output: str
    '''
    subprocess.check_call(['xsetwacom', 'set', str(device), 'MapToOutput', output])

def rotate_all_wacom_devices(direction):
    for device in get_wacom_device_ids():
        rotate_wacom_device(device, direction)

def map_all_wacom_devices_to_output(output):
    for device in get_wacom_device_ids():
        map_wacom_device_to_output(device, output)

if __name__ == '__main__':
    print(get_wacom_device_ids())
