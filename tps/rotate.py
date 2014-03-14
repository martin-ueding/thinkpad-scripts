#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>

import argparse
import logging

import tps
import tps.config
import tps.hooks

__docformat__ = "restructuredtext en"

class UnknownDirectionException(Exception):
    '''
    Unknown direction given at the command line.
    '''

def main():
    options = _parse_args()

    config = tps.config.get_config()

    rotate_to(translate_direction(options.direction), config)

def translate_direction(direction):
    if direction == 'normal':
        return tps.NORMAL

    if direction == 'left':
        return tps.LEFT

    if direction == 'right':
        return tps.RIGHT

    if direction == 'flip':
        return tps.INVERTED
    if direction == 'inverted':
        return tps.INVERTED

    raise UnknownDirectionException('Direction “{}” cannot be understood.'.format(direction))

def rotate_to(direction, config):
    tps.hooks.prerotate(config)

def _parse_args():
    """
    Parses the command line arguments.

    If the logging module is imported, set the level according to the number of
    ``-v`` given on the command line.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("direction", help="Positional arguments.")
    #parser.add_argument("", dest="", type="", default=, help=)
    #parser.add_argument("--version", action="version", version="<the version>")
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

    return options

if __name__ == "__main__":
    main()
