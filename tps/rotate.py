#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

import argparse
import logging
import sys

import tps
import tps.config
import tps.hooks
import tps.input
import tps.screen
import tps.unity
import tps.vkeyboard

logger = logging.getLogger(__name__)

def main():
    '''
    Entry point for ``thinkpad-rotate``.
    '''
    options = _parse_args()

    config = tps.config.get_config()

    try:
        new_direction = new_rotation(
            tps.screen.get_rotation(config['screen']['internal']),
            options.direction, config)
    except tps.UnknownDirectionException:
        logger.error('Direction cannot be understood.')
        sys.exit(1)

    rotate_to(new_direction, config)

def rotate_to(direction, config):
    '''
    Performs all steps needed for a screen rotation.
    '''
    tps.hooks.prerotate(direction, config)

    tps.screen.rotate(config['screen']['internal'], direction)
    tps.input.rotate_all_wacom_devices(direction)
    tps.input.map_all_wacom_devices_to_output(config['screen']['internal'])

    if config['rotate'].getboolean('subpixels'):
        if config['rotate'].getboolean('subpixels_with_external') \
           or tps.screen.get_external(config['screen']['internal']) is None:
            tps.screen.set_subpixel_order(direction)

    if config['unity'].getboolean('toggle_launcher'):
        tps.unity.set_launcher(not direction.physically_closed)

    tps.vkeyboard.toggle(config['vkeyboard']['program'],
                         direction.physically_closed)

    try:
        trackpoint_xinput_id = tps.input.get_xinput_id('TrackPoint')
        tps.input.set_xinput_state(
            trackpoint_xinput_id,
            not direction.physically_closed,
        )
    except tps.input.InputDeviceNotFoundException as e:
        logger.warning('TrackPoint was not found, could not be deactivated.')
        logger.warning(e)

    try:
        touchpad_xinput_id = tps.input.get_xinput_id('TouchPad')
        tps.input.set_xinput_state(
            touchpad_xinput_id,
            not direction.physically_closed,
        )
    except tps.input.InputDeviceNotFoundException as e:
        logger.warning('TouchPad was not found, could not be deactivated.')
        logger.warning(e)

    tps.hooks.postrotate(direction, config)

def new_rotation(current, desired_str, config):
    '''
    Determines the new rotation based on desired and current one.
    '''
    if desired_str is None:
        if not current.physically_closed:
            new = tps.translate_direction(config['rotate']['default_rotation'])
            logger.info('Using default, setting to {}'.format(new))
        else:
            new = tps.NORMAL
            logger.info('Using default, setting to {}'.format(new))
    else:
        desired = tps.translate_direction(desired_str)
        if desired == current:
            new = tps.NORMAL
            logger.info('You try to rotate into the direction it is, reverting to normal.')
        else:
            new = desired
            logger.info('User chose to set to {}'.format(new))
    return new


def _parse_args():
    """
    Parses the command line arguments.

    If the logging module is imported, set the level according to the number of
    ``-v`` given on the command line.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("direction", nargs='?', help="Positional arguments.")
    parser.add_argument("-v", dest='verbose', action="count",
                        help='Enable verbose output. Can be supplied multiple '
                             'times for even more verbosity.')

    options = parser.parse_args()

    tps.config.set_up_logging(options.verbose)

    return options

if __name__ == "__main__":
    main()
