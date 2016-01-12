#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

import argparse
import logging
import sys
import time

from daemon import DaemonContext
from lockfile.pidlockfile import PIDLockFile

import tps
from tps.acpi import Acpi
import tps.config
from tps.hdaps import Hdaps
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

    if options.via_hook:
        xrandr_bug_fail_early(config)
        
    if not options.daemonize:
        # Quickly abort if the call is by the hook and the user disabled the trigger.
        if options.via_hook and not config['trigger'].getboolean('enable_rotate'):
            sys.exit(0)
            
        main_cmdline(options, config)
    else:
        with DaemonContext(pidfile = PIDLockFile(options.pidfile), \
		    stdout = sys.stdout, stderr = sys.stderr):
            main_daemon(options, config)
    
    sys.exit(0)
        
def main_cmdline(options, config):
    try:
        new_direction = new_rotation(
            tps.screen.get_rotation(config['screen']['internal']),
            options.direction, config, options.force_direction)
    except tps.UnknownDirectionException:
        logger.error('Direction cannot be understood.')
        sys.exit(1)
    except tps.screen.ScreenNotFoundException as e:
        logger.error('Unable to determine rotation of "{}": {}'.format(
            config['screen']['internal'], e))
        sys.exit(1)

    rotate_to(new_direction, config, Acpi.inTabletMode())

def main_daemon(options, config):
    if not Hdaps.hasHDAPS():
        sys.exit(1)
    
    try:
        current_rotation = tps.screen.get_rotation(config['screen']['internal'])
    except tps.screen.ScreenNotFoundException as e:
        logger.error('Unable to determine rotation of "{}": {}'.format(
            config['screen']['internal'], e))
        sys.exit(1)
       
    hdaps_resting_x = config['rotate'].getint('hdaps_resting_x')
    hdaps_resting_y = config['rotate'].getint('hdaps_resting_y')
    hdaps_resolution_x = config['rotate'].getint('hdaps_resolution_x')
    hdaps_resolution_y = config['rotate'].getint('hdaps_resolution_y')
    hdaps_invert = config['rotate'].getint('hdaps_invert')
    
    hdaps = Hdaps((hdaps_resting_x, hdaps_resting_y), 
        (hdaps_resolution_x, hdaps_resolution_y))
    if hdaps_invert > 0:
        hdaps.setInvertion(hdaps_invert)
    
    hadps_autorotate_tablet_mode = config['rotate'].\
        getboolean('hadps_autorotate_tablet_mode')
    hadps_autorotate_laptop_mode = config['rotate'].\
        getboolean('hadps_autorotate_laptop_mode')
    hadps_poll_interval = config['rotate'].\
        getfloat('hadps_poll_interval')
        
    tablet_mode = Acpi.inTabletMode()
    
    while True:
        time.sleep(hadps_poll_interval);
        tablet_mode_prev = tablet_mode
        tablet_mode = Acpi.inTabletMode()
        try:
            if tablet_mode:
                if not hadps_autorotate_tablet_mode:
                    desired_rotation = tps.translate_direction(config['rotate']['default_rotation'])
                else:
                    desired_rotation = hdaps.getOrientation(True)
            elif not hadps_autorotate_laptop_mode:
                desired_rotation = tps.NORMAL
            else:
                desired_rotation = hdaps.getOrientation(False)
                
            if desired_rotation is None or \
                current_rotation == desired_rotation:                    
                if tablet_mode != tablet_mode_prev:
                    # when orientation does not change but table mode
                    # does we're left with disabled controls
                    toggle_tablet_mode(config, tablet_mode)
                continue
        except tps.UnknownDirectionException:
            logger.error('Direction cannot be understood.')
            sys.exit(1)

        rotate_to(desired_rotation, config, tablet_mode)
        current_rotation = desired_rotation

def rotate_to(direction, config, tablet_mode):
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

    toggle_tablet_mode(config, tablet_mode)

    if needs_xrandr_bug_workaround(config) and can_use_chvt():
        toggle_virtual_terminal()

    tps.hooks.postrotate(direction, config)
    
def toggle_tablet_mode(config, tablet_mode):
    '''
    Steps dependant on tablet mode
    '''
    if config['unity'].getboolean('toggle_launcher'):
        tps.unity.set_launcher(not tablet_mode)

    tps.vkeyboard.toggle(config['vkeyboard']['program'], tablet_mode)

    try:
        trackpoint_xinput_id = tps.input.get_xinput_id('TrackPoint')
        tps.input.set_xinput_state(
            trackpoint_xinput_id,
            not tablet_mode,
        )
    except tps.input.InputDeviceNotFoundException as e:
        logger.info('TrackPoint was not found, could not be (de)activated.')
        logger.debug('Exception was: “%s”', str(e))

    try:
        touchpad_xinput_id = tps.input.get_xinput_id('TouchPad')
        tps.input.set_xinput_state(
            touchpad_xinput_id,
            not tablet_mode,
        )
    except tps.input.InputDeviceNotFoundException as e:
        logger.info('TouchPad was not found, could not be (de)activated.')
        logger.debug('Exception was: “%s”', str(e))


def new_rotation(current, desired_str, config, force=False):
    '''
    Determines the new rotation based on desired and current one.

    :param bool force: If set the function does not try to be too clever but
    just uses the rotation given. If no rotation is given in ``desired_str``,
    it still uses the default from the configuration.
    '''
    if desired_str is None:
        if not Acpi.inTabletMode():
            new = tps.translate_direction(config['rotate']['default_rotation'])
            logger.info('Using default, setting to {}'.format(new))
        else:
            new = tps.NORMAL
            logger.info('Using default, setting to {}'.format(new))
    else:
        desired = tps.translate_direction(desired_str)
        if desired == current and not force:
            new = tps.NORMAL
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
    output = tps.check_output(command, logger)

    return b'/bin/chvt' in output


def toggle_virtual_terminal():
    '''
    '''
    assert can_use_chvt()
    tps.check_call(['sudo', '-n', 'chvt', '6'], logger)
    tps.check_call(['sudo', '-n', 'chvt', '7'], logger)


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


def _parse_args():
    """
    Parses the command line arguments.

    If the logging module is imported, set the level according to the number of
    ``-v`` given on the command line.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description='Thinkpad screen rotate')
    parser.add_argument("direction", nargs='?', help="Positional arguments.")
    parser.add_argument("-d", dest='daemonize', action="store_true",
                        help='Daemonize screen rotation to take use of '
                        'HDAPS accelerometer for automatic rotation.')
    parser.add_argument("--pidfile", "-p", dest='pidfile', action='store', 
                        default='/var/run/thinkpad-rotated.pid',
                        help='Pid File location for daemon mode.')
    parser.add_argument("-v", dest='verbose', action="count",
                        help='Enable verbose output. Can be supplied '
                        'multiple times for even more verbosity.')
    parser.add_argument('--via-hook', action='store_true', 
                        help='Let the program know that it was called '
                        'using the hook. This will then enable some '
                        'workarounds. You do not need to care about this.')
    parser.add_argument('--force-direction', action='store_true', 
                        help='Do not try to be smart. Actually rotate '
                        'in the direction given even it already is the '
                        'case.')

    options = parser.parse_args()

    tps.config.set_up_logging(options.verbose)

    return options


if __name__ == "__main__":
    main()
