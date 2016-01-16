#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

import collections
import logging
import sys
import time

import tps
from tps.acpi.thinkpad_acpi import ThinkpadAcpi
import tps.config
from tps.hdaps import Hdaps
import tps.hooks
import tps.input
import tps.screen
import tps.unity
from tps.utils import check_call, check_output

logger = logging.getLogger(__name__)


Direction = collections.namedtuple(
    'Direction', ['xrandr', 'subpixel', 'rot_mat']
)
'''
Holds the direction names of different tools.

``xrandr`` and other programs use different names for the rotations. To avoid
proliferation of various names, this class holds the differing names. The
module provides constants which have to be used within :mod:`tps`.
'''

LEFT = Direction('left', 'vrgb', [0,-1, 1,
                                  1, 0, 0,
                                  0, 0, 1])

RIGHT = Direction('right', 'vbgr', [0, 1, 0,
                                   -1, 0, 1,
                                    0, 0, 1])

NORMAL = Direction('normal', 'rgb', [1, 0, 0,
                                     0, 1, 0,
                                     0, 0, 1])

INVERTED = Direction('inverted', 'bgr', [-1, 0, 1,
                                          0,-1, 1,
                                          0, 0, 1])

TABLET_NORMAL = NORMAL

class UnknownDirectionException(Exception):
    '''
    Unknown direction given at the command line.
    '''
        
def rotate_cmdline(options, config):
    try:
        new_direction = new_rotation(
            tps.screen.get_rotation(config['screen']['internal']),
            options.direction, config, options.force_direction)
    except UnknownDirectionException:
        logger.error('Direction cannot be understood.')
        sys.exit(1)
    except tps.screen.ScreenNotFoundException as e:
        logger.error('Unable to determine rotation of "{}": {}'.format(
            config['screen']['internal'], e))
        sys.exit(1)
        
    input_state = get_input_state(options.state, options.direction)

    rotate_to(new_direction, config, input_state)

def rotate_daemon(options, config):
    if not Hdaps.hasHDAPS():
        sys.exit(1)
    
    try:
        current_rotation = tps.screen.get_rotation(config['screen']['internal'])
    except tps.screen.ScreenNotFoundException as e:
        logger.error('Unable to determine rotation of "{}": {}'.format(
            config['screen']['internal'], e))
        sys.exit(1)
       
    hdaps_resting_x = config['hdaps'].getint('resting_x')
    hdaps_resting_y = config['hdaps'].getint('resting_y')
    hdaps_resolution_x = config['hdaps'].getint('resolution_x')
    hdaps_resolution_y = config['hdaps'].getint('resolution_y')
    hdaps_invert = config['hdaps'].getint('invert')
    hadps_poll_interval = config['hdaps'].getfloat('poll_interval')
    
    hdaps = Hdaps((hdaps_resting_x, hdaps_resting_y), 
        (hdaps_resolution_x, hdaps_resolution_y))
    if hdaps_invert > 0:
        hdaps.setInvertion(hdaps_invert)
    
    autorotate_tablet_mode = config['rotate'].\
        getboolean('autorotate_tablet_mode')
    autorotate_laptop_mode = config['rotate'].\
        getboolean('autorotate_laptop_mode')
        
    tablet_mode = ThinkpadAcpi.inTabletMode()
    
    while True:
        time.sleep(hadps_poll_interval);
        tablet_mode_prev = tablet_mode
        tablet_mode = ThinkpadAcpi.inTabletMode()
        try:
            if tablet_mode:
                if not autorotate_tablet_mode:
                    desired_rotation = translate_direction(config['rotate']['default_rotation'])
                else:
                    desired_rotation = hdaps.getOrientation(True)
            elif not autorotate_laptop_mode:
                desired_rotation = NORMAL
            else:
                desired_rotation = hdaps.getOrientation(False)
                
            if desired_rotation is None or \
                current_rotation == desired_rotation:                    
                if tablet_mode != tablet_mode_prev:
                    # when orientation does not change but table mode
                    # does we're left with disabled controls
                    set_inputs_state(config, not tablet_mode)
                continue
        except UnknownDirectionException:
            logger.error('Direction cannot be understood.')
            sys.exit(1)

        rotate_to(desired_rotation, config, not tablet_mode)
        current_rotation = desired_rotation
        
def get_input_state(state, direction):
    if state == 'on':
        return True
    elif state == 'off' or direction == 'tablet-normal':
        return False
    elif state is None:
        return not ThinkpadAcpi.inTabletMode()
    
def set_inputs_state(config, state):
    '''
    Change input devices enabled state
    '''
    if config['unity'].getboolean('toggle_launcher'):
        tps.unity.set_launcher(state)

    command_toggle_state(config['vkeyboard']['program'], not state)

    try:
        trackpoint_xinput_id = tps.input.get_xinput_id('TrackPoint')
        tps.input.set_xinput_state(
            trackpoint_xinput_id,
            state
        )
    except tps.input.InputDeviceNotFoundException as e:
        logger.info('TrackPoint was not found, could not be (de)activated.')
        logger.debug('Exception was: “%s”', str(e))

    try:
        touchpad_xinput_id = tps.input.get_xinput_id('TouchPad')
        tps.input.set_xinput_state(
            touchpad_xinput_id,
            state
        )
    except tps.input.InputDeviceNotFoundException as e:
        logger.info('TouchPad was not found, could not be (de)activated.')
        logger.debug('Exception was: “%s”', str(e))

def translate_direction(direction):
    '''
    :param str direction: Direction string
    :returns: Direction object
    :rtype: Direction
    :raises UnknownDirectionException:
    '''

    if direction in ['normal', 'none']:
        result = NORMAL

    elif direction in ['left', 'ccw']:
        result = LEFT

    elif direction in ['right', 'cw']:
        result = RIGHT

    elif direction in ['flip', 'inverted', 'half']:
        result = INVERTED

    elif direction == 'tablet-normal':
        result = TABLET_NORMAL

    else:
        raise UnknownDirectionException(
            'Direction “{}” cannot be understood.'.format(direction))

    logger.debug('Converted “{}” to “{}”.'.format(direction, result))

    return result

def rotate_to(direction, config, input_state):
    '''
    Performs all steps needed for a screen rotation.
    '''
    tps.hooks.prerotate(direction, config)

    tps.screen.rotate(config['screen']['internal'], direction)
    tps.input.map_rotate_all_input_devices(config['screen']['internal'],
                                           direction)

    if config['rotate'].getboolean('subpixels'):
        if config['rotate'].getboolean('subpixels_with_external') \
           or not tps.screen.get_externals(config['screen']['internal']):
            tps.screen.set_subpixel_order(direction)

    set_inputs_state(config, input_state)

    if needs_xrandr_bug_workaround(config) and can_use_chvt():
        toggle_virtual_terminal()

    tps.hooks.postrotate(direction, config)

def new_rotation(current, desired_str, config, force=False):
    '''
    Determines the new rotation based on desired and current one.

    :param bool force: If set the function does not try to be too clever but
    just uses the rotation given. If no rotation is given in ``desired_str``,
    it still uses the default from the configuration.
    '''
    if desired_str is None:
        if not ThinkpadAcpi.inTabletMode():
            new = translate_direction(config['rotate']['default_rotation'])
            logger.info('Using default, setting to {}'.format(new))
        else:
            new = NORMAL
            logger.info('Using default, setting to {}'.format(new))
    else:
        desired = translate_direction(desired_str)
        if desired == current and not force:
            new = NORMAL
            logger.info('You try to rotate into the direction it is, '
                        'reverting to normal.')
        else:
            new = desired
            logger.info('User chose to set to {}'.format(new))

    return new


def can_use_chvt():
    '''
    Checks whether ``chvt`` can be called with ``sudo`` without a password.

    The ``sudo`` command has the ``-n`` option which will just make the command
    fail when the user does not have the appropriate permissions. The problem
    with ``chvt`` is that it does not have any intelligent command line
    argument parsing. If will return code 1 if no argument is given, the same
    code that ``sudo`` gives when no permission is available. Therefore I chose
    to use ``sudo -l` to get the whole list and see whether the full path to
    ``chvt`` is in there. This might break on Fedora where the ``usr``-merge
    has been done now.

    The following line is needed in a file like ``/etc/sudoers.d/chvt``::

        myuser  ALL = NOPASSWD: /bin/chvt

    You have to replace ``myuser`` which your username. Giving too broad
    permissions to every other user account is probably not a good idea.

    :rtype: bool
    '''
    command = ['sudo', '-l']
    output = check_output(command, logger)

    return b'/bin/chvt' in output


def toggle_virtual_terminal():
    '''
    '''
    assert can_use_chvt()
    check_call(['sudo', '-n', 'chvt', '6'], logger)
    check_call(['sudo', '-n', 'chvt', '7'], logger)


def has_external_screens(config):
    '''
    Checks whether any external screens are attached.
    '''
    externals = tps.screen.get_externals(config['screen']['internal'])
    return len(externals) > 0


def needs_xrandr_bug_workaround(config):
    '''
    Determines whether xrandr bug needs to be worked around.

    XRandr has a `bug in Ubuntu`__, maybe even in other distributions. In
    Ubuntu 15.04 a workaround is to change the virtual terminal to a different
    one and back to the seventh, the graphical one. This can be automated using
    the ``chvt`` command which requires superuser privileges. An entry in the
    sudo file can let the normal user execute this program.

    __ https://bugs.launchpad.net/ubuntu/+source/x11-xserver-utils/+bug/1451798
    '''
    # Do nothing if workaround is not requested.
    if not config['rotate'].getboolean('xrandr_bug_workaround'):
        return False

    logger.debug('xrandr bug workaround requested')

    # Do nothing if an external screen is attached. The bug does not appear
    # then.
    if has_external_screens(config):
        return False

    return True


def xrandr_bug_fail_early(config):
    '''
    Quits the program if xrandr bug cannot be coped with.
    '''
    if needs_xrandr_bug_workaround(config) and not can_use_chvt():
        logger.warning('Aborting since there are no external screens attached '
                       'and XRandr bug workaround is enabled.')
        sys.exit(1)
