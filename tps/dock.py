# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2015 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

'''
Logic related to the UltraBase® docks.
'''

import glob
import logging

from tps.compositor import get_rotation, get_externals, set_brightness, \
                           screen_enable, screen_disable, \
                           rotate_input_devices, ScreenNotFoundException
from tps.hooks import predock as predock_hook, postdock as postdock_hook
import tps.network
import tps.sound

logger = logging.getLogger(__name__)


def get_docking_state(state):
    if state == 'on':
        return True
    elif state == 'off':
        return False
    elif state is None:
        return not is_docked()

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
                logger.info('Docking station found.')
                return True
    logger.info('No docking station found.')
    return False


def select_docking_screens(internal, primary='', secondary=''):
    '''
    Selects the primary, secondary, and remaining screens when docking.

    If `primary` or `secondary` is not the name of a connected screen, then
    select an appropriate screen from the connected screens. External screens
    are prioritized over the `internal` screen, and `primary` is prioritized
    over `secondary`. Warn the user if `primary` or `secondary` is a non-empty
    string and the screen is not connected.

    If no external screens are connected, then set `primary` to the `internal`
    screen, and set `secondary` to `None`.

    :param str internal: Name of the internal screen
    :param str primary: Name of primary screen, or an empty string
    :param str secondary: Name of secondary screen, or an empty string
    :returns: (`primary`, `secondary`, [`other1`, ...])
    :rtype: tuple

    For example, when only ``LVDS1`` is connected:

    >>> select_docking_screens('LVDS1', '', '')
    ('LVDS1', None, [])

    When ``LVDS1`` and ``VGA1`` are connected:

    >>> select_docking_screens('LVDS1', '', '')
    ('VGA1', 'LVDS1', [])
    >>> select_docking_screens('LVDS1', 'LVDS1', '')
    ('LVDS1', 'VGA1', [])

    When ``LVDS1``, ``VGA1``, and ``HDMI1`` are connected:

    >>> select_docking_screens('LVDS1', '', '')
    ('HDMI1', 'VGA1', ['LVDS1'])
    >>> select_docking_screens('LVDS1', 'VGA1', '')
    ('VGA1', 'HDMI1', ['LVDS1'])
    >>> select_docking_screens('LVDS1', '', 'LVDS1')
    ('HDMI1', 'LVDS1', ['VGA1'])

    Note that the default order of ``VGA1`` versus ``HDMI1`` depends on the
    output of ``xrandr``. See
    :py:class:`tps.testsuite.test_dock.SelectDockingScreensTestCase` for more
    examples.

    '''
    screens = get_externals(internal) + [internal]
    for index, screen in enumerate([primary, secondary]):
        if screen in screens:
            screens.remove(screen)
            screens.insert(index, screen)
        elif screen != '':
            logger.warning('Configured screen "{}" does not exist or is not '
                           'connected.'.format(screen))
    return screens[0], screens[1] if len(screens) > 1 else None, screens[2:]


def dock(on, config):
    '''
    Performs the makroscopic docking action.

    :param bool on: Desired state
    :param configparser.ConfigParser config: Global config
    :returns: None
    '''
    logger.info('dock({})'.format(on))
    predock_hook(on, config)

    if on:
        if config['sound'].getboolean('unmute'):
            tps.sound.unmute(config['sound']['dock_loudness'])

        if config['screen'].getboolean('set_brightness'):
            set_brightness(config['screen']['brightness'])

        primary, secondary, others = select_docking_screens(
            config['screen']['internal'], config['screen']['primary'],
            config['screen']['secondary'])

        logger.debug('primary: %s, secondary: %s, others: %s', str(primary),
                     str(secondary), str(others))
        if secondary is None:
            # This is the only screen.
            screen_enable(primary, primary=True)
        else:
            # Disable all but one screen (xrandr complains otherwise).
            for screen in others[:-1]:
                screen_disable(screen)
            # Enable one screen.
            screen_enable(secondary)
            # It's now safe to disable the last other screen.
            if others:
                screen_disable(others[-1])
            # Enable the primary screen.
            screen_enable(primary)
            # Need to call this separately to work around bugs in xrandr/X11.
            screen_enable(
                primary, primary=True,
                position=(config['screen']['relative_position'], secondary))

            if not config['screen'].getboolean('internal_docked_on'):
                logger.info('Internal screen is supposed to be off when '
                            'docked, turning it off.')
                screen_disable(config['screen']['internal'])

        if config['network'].getboolean('disable_wifi') \
           and tps.network.has_ethernet():
            tps.network.set_wifi(False)

        if config['network'].getboolean('restart_connection'):
            try:
                # Try to get connection name from the configuration. If there
                # is none, use the one that was found automatically.
                connection_to_restart = config['network'].get(
                    'connection_name', tps.network.get_ethernet_con_name())
                tps.network.restart(connection_to_restart)
            except tps.network.MissingEthernetException:
                logger.warning('unable to find ethernet connection')

        if primary == config['screen']['internal'] or \
           secondary == config['screen']['internal']:
            try:
                rotate_input_devices(config['touch']['regex'],
                    config['screen']['internal'],
                    get_rotation(config['screen']['internal']))
            except ScreenNotFoundException as e:
                logger.error('Unable to map input devices to "{}": {}'.format(
                    config['screen']['internal'], e))

    else:
        externals = get_externals(config['screen']['internal'])
        # Disable all but one screen (xrandr complains otherwise).
        for external in externals[:-1]:
            screen_disable(external)
        # Enable the internal screen.
        screen_enable(config['screen']['internal'], primary=True)
        # It's now safe to disable the last external screen.
        if externals:
            screen_disable(externals[-1])

        if config['sound'].getboolean('unmute'):
            tps.sound.set_volume(config['sound']['undock_loudness'])

        if config['network'].getboolean('disable_wifi'):
            tps.network.set_wifi(True)

        try:
            rotate_input_devices(config['touch']['regex'],
                config['screen']['internal'],
                get_rotation(config['screen']['internal']))
        except ScreenNotFoundException as e:
            logger.error('Unable to map input devices to "{}": {}'.format(
                config['screen']['internal'], e))

    postdock_hook(on, config)
