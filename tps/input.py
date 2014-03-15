#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic related to input devices.
'''

import argparse
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
    Sets the device state.

    :param device: ``xinput`` ID of devicwe
    :type device: int
    :param state: Whether device should be enabled
    :type state: bool
    '''
    set_to = '1' if state else '0'
    tps.check_call(['xinput', 'set-prop', str(device), 'Device Enabled',
                    set_to], logger)

def get_xinput_state(device):
    '''
    Gets the device state.

    :param device: ``xinput`` ID of devicwe
    :type device: int
    :returns: Whether device is enabled
    :rtype: bool
    '''
    output = tps.check_output(['xinput', '--list', str(device)], logger)
    return not b'disabled' in output

def main_trackpoint():
    '''
    Command line entry point for toggling the trackpoint.

    :returns: None
    '''
    state_change_ui('TrackPoint')

def main_touchpad():
    '''
    Command line entry point for toggling the touchpad.

    :returns: None
    '''
    state_change_ui('TouchPad')

def main_touchscreen():
    '''
    Command line entry point for toggling the touch screen.

    :returns: None
    '''
    state_change_ui('Wacom ISDv4 E6 Finger touch')

def state_change_ui(device_name):
    '''
    Change the state of the given device depending on command line options.

    It parses the command line options. If no state is given there, it will be
    the opposite of the current state.

    :returns: None
    '''
    state = _parse_args_to_state()
    device = get_xinput_id(device_name)
    if state is None:
        state = not get_xinput_state(device)
    set_xinput_state(device, state)

def _parse_args_to_state():
    """
    Parses the command line arguments.

    If the logging module is imported, set the level according to the number of
    ``-v`` given on the command line.

    :return: State
    :rtype: bool or None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("state", nargs='?', help="Positional arguments.")
    parser.add_argument("-v", dest='verbose', action="count", help='Enable verbose output. Can be supplied multiple times for even more verbosity.')

    options = parser.parse_args()

    # Try to set the logging level in case the logging module is imported.
    try:
        if options.verbose == 1:
            logging.basicConfig(level=logging.INFO)
        elif options.verbose == 2:
            logging.basicConfig(level=logging.DEBUG)
    except NameError as e:
        pass

    if options.state == 'on':
        return True
    elif options.state == 'off':
        return False
    else:
        return None
