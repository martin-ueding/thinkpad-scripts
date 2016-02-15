# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic related to input devices.
'''

import logging
import re

from tps.compositor.common import InputDeviceNotFoundException
from tps.compositor.x11.screen import get_resolution_and_shift
from tps.utils import check_call, check_output

logger = logging.getLogger(__name__)


def get_device_ids(regex):
    '''
    Gets the IDs of the built-in Wacom touch devices.

    This calls ``xinput`` to get the list and parses that with a regular
    expression. Only device names starting with ``Wacom ISD`` (default regex)
    are taken into account. If you have an external device, this will not be
    picked up.

    :rtype: list
    '''
    logger.debug(_('Using “%s” as regex to find devices.'), regex)
    pattern = re.compile(regex.encode())
    output = check_output(['xinput'], logger)
    lines = output.split(b'\n')
    ids = []
    for line in lines:
        matcher = pattern.search(line)
        if matcher:
            ids.append(int(matcher.group(1)))

    return ids

def rotate_input_device(device, matrix):
    '''
    Rotates an input device.

    :type device: int
    :type direction: tps.Direction
    '''
    check_call(
        ['xinput', 'set-prop', str(device), 'Coordinate Transformation Matrix']
        + list(map(str, matrix)), logger
    )

def rotate_input_devices(regex, output, orientation):
    '''
    Rotates all touch (Wacom®) devices by regex.
    '''
    matrix = generate_xinput_coordinate_transformation_matrix(output,
                                                              orientation)
    for device in get_device_ids(regex):
        rotate_input_device(device, matrix)

def get_xinput_id(name):
    '''
    Gets the ``xinput`` ID for given device.

    The first parts of the name may be omitted. To get “TPPS/2 IBM TrackPoint”,
    it is sufficient to use “TrackPoint”.

    :raises InputDeviceNotFoundException: Device not found in ``xinput`` output
    :rtype: int
    '''
    output = check_output(['xinput', 'list'], logger).decode()
    matcher = re.search(name + r'\s*id=(\d+)', output)
    if matcher:
        return int(matcher.group(1))

    raise InputDeviceNotFoundException(
        _('Input device “{}” could not be found').format(name))

def set_xinput_state(device, state):
    '''
    Sets the device state.

    :param device: ``xinput`` ID of devicwe
    :type device: int
    :param state: Whether device should be enabled
    :type state: bool
    '''
    set_to = '1' if state else '0'
    check_call(['xinput', 'set-prop', str(device), 'Device Enabled',
                    set_to], logger)

def get_xinput_state(device):
    '''
    Gets the device state.

    :param device: ``xinput`` ID of devicwe
    :type device: int
    :returns: Whether device is enabled
    :rtype: bool
    '''
    output = check_output(['xinput', '--list', str(device)], logger)
    return b'disabled' not in output
    
def toggle_xinput_state(device_name, state):
    '''
    Change the state of the given device.
    :returns: None
    '''
    device = get_xinput_id(device_name)
    if state is None:
        state = not get_xinput_state(device)
    set_xinput_state(device, state)

    if has_xinput_prop(device, b'Wacom Enable Touch'):
        set_wacom_touch(device, state)

def set_wacom_touch(device_id, state):
    '''
    Changes the Wacom Touch property of the given device.
    '''
    check_call(['xinput', 'set-prop', str(device_id), 'Wacom Enable Touch',
                    '1' if state else '0'], logger)

def has_xinput_prop(device, prop):
    '''
    Checks whether the device has the given xinput propery.
    '''
    output = check_output(['xinput', 'list-props', str(device)], logger)
    return prop in output

def generate_xinput_coordinate_transformation_matrix(output, orientation):
    '''
    Generates the coordinate transformation matrix that is needed for xinput to
    confine the input to one screen and rotate it properly.

    0.415703, 0.000000, 0.584297,
    0.000000, -0.711111, 0.711111,
    0.000000, 0.000000, 1.000000
    '''
    rs = get_resolution_and_shift(output)

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
    logger.debug(_('Translation and scaling matrix: %s'),
                   _matrix_to_str(m_shift_scale))

    m_total = _matrix_mul(m_shift_scale, orientation.rot_mat)
    logger.debug(_('Complete transformation matrix: %s'),
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
