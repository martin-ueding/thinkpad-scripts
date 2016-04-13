#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014-2016 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic related to input devices.
'''

import argparse
import logging
import re

import tps
import tps.config
import tps.screen

logger = logging.getLogger(__name__)


class InputDeviceNotFoundException(Exception):
    '''
    ``xinput`` device could not be found.
    '''
    pass


def get_wacom_device_ids():
    '''
    Gets the IDs of the built-in Wacom touch devices.

    This calls ``xinput`` to get the list and parses that with a regular
    expression. Only device names starting with ``Wacom ISD`` (default regex)
    are taken into account. If you have an external device, this will not be
    picked up.

    :rtype: list
    '''
    config = tps.config.get_config()

    regex = config['touch']['regex']
    logger.debug('Using “%s” as regex to find Wacom devices.', regex)
    pattern = re.compile(regex.encode())
    output = tps.check_output(['xinput'], logger)
    lines = output.split(b'\n')
    ids = []
    for line in lines:
        matcher = pattern.search(line)
        if matcher:
            ids.append(int(matcher.group(1)))

    return ids


def map_rotate_input_device(device, matrix):
    '''
    Rotates an input device.

    :type device: int
    :type direction: tps.Direction
    '''
    tps.check_call(
        ['xinput', 'set-prop', str(device), 'Coordinate Transformation Matrix']
        + list(map(str, matrix)), logger
    )


def map_rotate_all_input_devices(output, orientation):
    '''
    Maps all Wacom® devices.
    '''
    matrix = generate_xinput_coordinate_transformation_matrix(output,
                                                              orientation)
    wacom_device_ids = get_wacom_device_ids()
    for device in wacom_device_ids:
        map_rotate_input_device(device, matrix)
    for device in wacom_device_ids:
        wacom_rotate_reset(device)


def wacom_rotate_reset(device):
    '''
    Resets the “Wacom Rotation” property of devices.

    In GH-117__ we noticed that in Ubuntu the ``xrandr`` rotation command will
    also rotate some input devices. This is probably meant in a good way but
    interferes with out rotation here. Therefore we reset the “Wacom Rotation”
    after setting the transformation matrix.

    __ https://github.com/martin-ueding/thinkpad-scripts/issues/117
    '''
    command = ['xinput', 'set-prop', 'device', 'Wacom Rotation', '0']
    tps.check_call(command, logger)


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
        'Input device “{}” could not be found'.format(name))


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
    return b'disabled' not in output


def set_wacom_touch(device_id, state):
    '''
    Changes the Wacom Touch property of the given device.
    '''
    tps.check_call(['xinput', 'set-prop', str(device_id), 'Wacom Enable Touch',
                    '1' if state else '0'], logger)


def state_change_ui(config_name):
    '''
    Change the state of the given device depending on command line options.

    It parses the command line options. If no state is given there, it will be
    the opposite of the current state.

    :param bool set_touch: Whether to also toggle the ``Touch`` property on
        this device.
    :returns: None
    '''
    config = tps.config.get_config()
    device_name = config['input'][config_name]
    state = _parse_args_to_state()
    device = get_xinput_id(device_name)
    if state is None:
        state = not get_xinput_state(device)
    set_xinput_state(device, state)

    if has_xinput_prop(device, b'Wacom Enable Touch'):
        set_wacom_touch(device, state)


def has_xinput_prop(device, prop):
    '''
    Checks whether the device has the given xinput propery.
    '''
    output = tps.check_output(['xinput', 'list-props', str(device)], logger)
    return prop in output


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
    parser.add_argument("-v", dest='verbose', action="count",
                        help='Enable verbose output. Can be supplied multiple '
                             'times for even more verbosity.')

    options = parser.parse_args()

    tps.config.set_up_logging(options.verbose)

    if options.state == 'on':
        return True
    elif options.state == 'off':
        return False
    else:
        return None


def generate_xinput_coordinate_transformation_matrix(output, orientation):
    '''
    Generates the coordinate transformation matrix that is needed for xinput to
    confine the input to one screen and rotate it properly.

    0.415703, 0.000000, 0.584297,
    0.000000, -0.711111, 0.711111,
    0.000000, 0.000000, 1.000000
    '''
    rs = tps.screen.get_resolution_and_shift(output)

    x_scale = rs['output_width'] / rs['screen_width']
    y_scale = rs['output_height'] / rs['screen_height']

    m_scale = [
        x_scale, 0, 0,
        0, y_scale, 0,
        0, 0, 1,
    ]

    x_shift = rs['output_x'] / rs['screen_width']
    y_shift = rs['output_y'] / rs['screen_height']

    m_shift = [
        1, 0, x_shift,
        0, 1, y_shift,
        0, 0, 1,
    ]

    m_shift_scale = _matrix_mul(m_shift, m_scale)
    logger.debug("Translation and scaling matrix: %s",
                 _matrix_to_str(m_shift_scale))

    m_total = _matrix_mul(m_shift_scale, orientation.rot_mat)
    logger.debug("Complete transformation matrix: %s",
                 _matrix_to_str(m_total))

    return m_total


def _matrix_to_str(matrix):
    msg = '['
    for row in range(3):
        msg += '['
        for column in range(3):
            msg += '{:9.5f} '.format(matrix[row*3 + column])
        msg += ']'
    msg += ']'
    return msg


def _matrix_mul(m1, m2):
    output = [0]*9

    for o_row in range(3):
        for o_col in range(3):
            for i in range(3):
                output[o_row*3 + o_col] += m1[o_row*3 + i] * m2[i*3 + o_col]

    return output


if __name__ == '__main__':
    generate_xinput_coordinate_transformation_matrix('LVDS1', tps.INVERTED)
