#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic related to the UltraBase® docks.
'''

import glob

import tps
import tps.config
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
    '''

    if on:
        if config['sound'].getboolean('unmute'):
            tps.sound.unmute(config['sound']['dock_loundness'])

        if config['screen'].getboolean('set_brightness'):
            tps.screen.set_brightness(config['screen']['brightness'])

        if config['network'].getboolean('disable_wifi'):
            tps.network.set_wifi(False)

        if config['network'].getboolean('restart_connection'):
            tps.restart(config['network']['connection'])
    else:
        tps.screen.set_primary(config['screen']['internal'])
        tps.screen.disable_external()

        if config['sound'].getboolean('unmute'):
            tps.sound.set_volume(config['sound']['undock_loundness'])

        if config['network'].getboolean('disable_wifi'):
            tps.network.set_wifi(True)
