#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic related to the UltraBase® docks.
'''

import argparse
import glob
import logging

import tps
import tps.config
import tps.hooks
import tps.input
import tps.network
import tps.screen
import tps.sound

def is_docked():
    '''
    Determines whether the laptop is on a docking station.

    This checks for ``/sys/devices/platform/dock.*/docked``.

    :returns: True if laptop is docked
    :rtype: bool
    '''
    dockfiles = glob.glob('/sys/devices/platform/dock.*/docked')
    for dockfile in dockfiles:
        with open(dockfile) as handle:
            contents = handle.read()
            dock_state = int(contents) == 1
            if dock_state:
                return True
    return False

def dock(on, config):
    '''
    Performs the makroscopic docking action.

    :param on: Desired state
    :param configparser.ConfigParser config: Global config
    :returns: None
    '''
    tps.hooks.predock(on, config)

    if on:
        if config['sound'].getboolean('unmute'):
            tps.sound.unmute(config['sound']['dock_loudness'])

        if config['screen'].getboolean('set_brightness'):
            tps.screen.set_brightness(config['screen']['brightness'])


        tps.screen.enable(config['screen']['internal'])
        tps.screen.enable(tps.screen.get_external(config['screen']['internal']), primary=True,
                          position=(config['screen']['relative_position'],
                                    config['screen']['internal']))

        if config['network'].getboolean('disable_wifi') \
           and tps.network.has_ethernet():
            tps.network.set_wifi(False)

        if config['network'].getboolean('restart_connection'):
            tps.network.restart(config['network']['connection'])
    else:
        tps.screen.enable(config['screen']['internal'], primary=True)
        tps.screen.disable(tps.screen.get_external(config['screen']['internal']))

        if config['sound'].getboolean('unmute'):
            tps.sound.set_volume(config['sound']['undock_loudness'])

        if config['network'].getboolean('disable_wifi'):
            tps.network.set_wifi(True)

    tps.input.map_all_wacom_devices_to_output(config['screen']['internal'])

    tps.hooks.postdock(on, config)

def main():
    '''
    Command line entry point.

    :returns: None
    '''
    options = _parse_args()
    config = tps.config.get_config()
    dock(options.state == 'on', config)

def _parse_args():
    """
    Parses the command line arguments.

    If the logging module is imported, set the level according to the number of
    ``-v`` given on the command line.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("state", nargs='?', help="Positional arguments.")
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

if __name__ == '__main__':
    main()
