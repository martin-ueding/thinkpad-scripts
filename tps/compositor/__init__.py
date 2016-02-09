# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

'''This module exposes methods for screen/input interaction unified 
among different compositors. Currently only X11 server is supported
until Wayland/Mir implementations in DEs mature to expose xinput/xrandr
counterparts.
'''

import logging

from tps.acpi.thinkpad_acpi import ThinkpadAcpi
from tps.compositor.common import LEFT, RIGHT, NORMAL, INVERTED, \
                                  InputDeviceNotFoundException, \
                                  ScreenNotFoundException, \
                                  UnknownDirectionException, \
                                  translate_direction, \
                                  new_rotation
from tps.compositor.x11.input import rotate_input_devices, \
                                     get_xinput_id, set_xinput_state, \
                                     toggle_xinput_state as \
                                     toggle_input_state
from tps.compositor.x11.screen import rotate as screen_rotate, \
                                      get_externals, get_rotation, \
                                      set_brightness, set_subpixel_order, \
                                      enable as screen_enable, \
                                      disable as screen_disable, \
                                      xrandr_bug_workaround
from tps.compositor.unity import set_launcher as unity_set_launcher
from tps.hooks import prerotate as prerotate_hook, \
                      postrotate as postrotate_hook
from tps.utils import check_call, check_output, command_toggle_state

logger = logging.getLogger(__name__)

__all__ = [ 'LEFT', 'RIGHT', 'NORMAL', 'INVERTED', 
    'InputDeviceNotFoundException', 'ScreenNotFoundException', 
    'UnknownDirectionException', 'rotate_input_devices', 'rotate', 
    'get_externals', 'get_rotation', 'set_brightness', 'screen_enable',
    'screen_disable', 'translate_direction', 'new_rotation', 'rotate',
    'get_input_state', 'set_inputs_state', 'toggle_xinput_state'
]

def rotate(direction, config, input_state):
    '''
    Performs all steps needed for a screen rotation.
    '''
    prerotate_hook(direction, config)

    screen_rotate(config['screen']['internal'], direction)
    rotate_input_devices(config['touch']['regex'], \
                         config['screen']['internal'], direction)

    if config['rotate'].getboolean('subpixels'):
        if config['rotate'].getboolean('subpixels_with_external') \
           or not get_externals(config['screen']['internal']):
            set_subpixel_order(direction)

    set_inputs_state(config, input_state)

    xrandr_bug_workaround(config)

    postrotate_hook(direction, config)


def get_input_state(state, direction):
    if state == 'on':
        return True
    elif state == 'off' or direction == 'tablet-normal':
        return False
    elif state is None:
        return not ThinkpadAcpi.inTabletMode()


def set_inputs_state(config, state):
    '''
    Change input devices to desired state
    '''
    if config['unity'].getboolean('toggle_launcher'):
        unity_set_launcher(state)

    command_toggle_state(config['vkeyboard']['program'], not state)

    try:
        trackpoint_xinput_id = get_xinput_id('TrackPoint')
        set_xinput_state(trackpoint_xinput_id, state)
    except InputDeviceNotFoundException as e:
        logger.info('TrackPoint was not found, could not be (de)activated.')
        logger.debug('Exception was: “%s”', str(e))

    try:
        touchpad_xinput_id = get_xinput_id('TouchPad')
        set_xinput_state(touchpad_xinput_id, state)
    except InputDeviceNotFoundException as e:
        logger.info('TouchPad was not found, could not be (de)activated.')
        logger.debug('Exception was: “%s”', str(e))
