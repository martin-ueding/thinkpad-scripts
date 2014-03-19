#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

import argparse
import logging

import tps
import tps.config
import tps.hooks
import tps.input
import tps.screen
import tps.unity
import tps.vkeyboard

logger = logging.getLogger(__name__)

def main():
    options = _parse_args()

    config = tps.config.get_config()

    new_direction = new_rotation(
        tps.screen.get_rotation(config['screen']['internal']),
        options.direction, config)

    rotate_to(new_direction, config)

def rotate_to(direction, config):
    '''
    Performs all steps needed for a screen rotation.
    '''
    tps.hooks.prerotate(direction, config)

    tps.screen.rotate(config['screen']['internal'], direction)
    tps.input.rotate_all_wacom_devices(direction)
    tps.input.map_all_wacom_devices_to_output(config['screen']['internal'])

    if config['screen'].getboolean('rotate_subpixels'):
        if config['screen'].getboolean('rotate_subpixels_with_external') \
           or tps.screen.get_external(config['screen']['internal']) is None:
            tps.screen.set_subpixel_order(direction)

    if config['unity'].getboolean('toggle_launcher'):
        tps.unity.set_launcher(direction == tps.NORMAL)

    tps.vkeyboard.toggle(config['vkeyboard']['program'],
                         direction != tps.NORMAL)

    tps.input.set_xinput_state(
        tps.input.get_xinput_id('TrackPoint'),
        direction == tps.NORMAL,
    )
    tps.input.set_xinput_state(
        tps.input.get_xinput_id('TouchPad'),
        direction == tps.NORMAL,
    )

    tps.hooks.postrotate(direction, config)

def new_rotation(current, desired_str, config):
    '''
    Determines the new rotation based on desired and current one.
    '''
    if desired_str is None:
        if current == tps.NORMAL:
            new = tps.translate_direction(config['rotate']['default_rotation'])
            logger.info('Using default, setting to {}'.format(new))
        else:
            new = tps.NORMAL
            logger.info('Using default, setting to {}'.format(new))
    else:
        desired = tps.translate_direction(desired_str)
        if desired == current:
            logger.info('You try to rotate into the direction it is, reverting to normal.')
            new = tps.NORMAL
        else:
            logger.info('User chose to set to {}'.format(new))
            new = desired
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
    #parser.add_argument("", dest="", type="", default=, help=)
    #parser.add_argument("--version", action="version", version="<the version>")
    parser.add_argument("-v", dest='verbose', action="count", help='Enable verbose output. Can be supplied multiple times for even more verbosity.')

    options = parser.parse_args()

    if options.verbose == 1:
        tps.config.set_up_logging(logging.INFO)
    elif options.verbose == 2:
        tps.config.set_up_logging(logging.DEBUG)
    else:
        tps.config.set_up_logging(logging.WARN)

    return options

if __name__ == "__main__":
    main()
