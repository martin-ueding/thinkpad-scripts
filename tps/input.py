#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic related to input devices.
'''

import logging
import re

import tps

logger = logging.getLogger(__name__)

class InputDeviceNotFoundException(Exception):
    '''
    ``xinput`` device could not be found.
    '''
    pass

def get_wacom_device_ids():
    '''
    Gets the IDs of the built-in Wacom® touch devices.

    This calls ``xsetwacom list devices`` to get the list and parses that with
    a regular expression. Only device names starting with ``Wacom ISD`` are
    taken into account. If you have an external device, this will not be picked
    up.

    :rtype: list
    '''
    pattern = re.compile(br'Wacom ISD.*id: (\d+).*')
    output = tps.check_output(['xsetwacom', 'list', 'devices'], logger)
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
    tps.check_call(['xsetwacom', 'set', str(device), 'rotate',
                    direction.xsetwacom], logger)

def map_wacom_device_to_output(device, output):
    '''
    Maps a Wacom® device to a specific output.

    :type device: int
    :type output: str
    '''
    tps.check_call(['xsetwacom', 'set', str(device), 'MapToOutput', output],
                   logger)

def rotate_all_wacom_devices(direction):
    '''
    Rotates all Wacom® devices.
    '''
    for device in get_wacom_device_ids():
        rotate_wacom_device(device, direction)

def map_all_wacom_devices_to_output(output):
    '''
    Maps all Wacom® devices.
    '''
    for device in get_wacom_device_ids():
        map_wacom_device_to_output(device, output)

def get_xinput_id(name):
    '''
    Gets the ``xinput`` ID for given device.

    The first parts of the name may be omitted. To get “TPPS/2 IBM TrackPoint”,
    it is sufficient to use “TrackPoint”.

    :raises InputDeviceNotFoundException: Device not found in ``xinput`` output
    :rtype: int
    '''
    output = tps.check_output(['xinput', 'list'], logger).decode()
    matcher = re.search(name + r'\s*id=(\d+)', output)
    if matcher:
        return int(matcher.group(1))

    raise InputDeviceNotFoundException(
        'Input device “{}” could not found'.format(name))

def set_xinput_state(device, state):
    '''
    :param device: ``xinput`` ID of devicwe
    :type device: int
    :param state: Whether device should be enabled
    :type state: bool
    '''
    set_to = '1' if state else '0'
    tps.check_call(['xinput', 'set-prop', str(device), 'Device Enabled',
                    set_to], logger)

if __name__ == '__main__':
    print(get_xinput_id('TrackPoint'))
