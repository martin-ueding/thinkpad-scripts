#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014-2017 Martin Ueding <dev@martin-ueding.de>
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

    # Quickly abort if the call is by the hook and the user disabled the
    # trigger.
    if options.via_hook is not None:
        if 'enable_rotate' in config['trigger']:
            # The user has this key in his configuration. The default does not
            # have it anymore, so this must be manual.
            if config['trigger'].getboolean('enable_rotate'):
                logger.warning('You have specified the deprecated trigger.enable_rotate option in your configuration file. The new config option is trigger.rotate_triggers, which is a list of enabled triggers. This program will use your existing trigger.enable_rotate value, but please update your config. To update your config while keeping the behavior of your current config, simply remove trigger.enable_rotate from your config file.')
            else:
                logger.warning('You have specified the deprecated trigger.enable_rotate option in your configuration file. The new config option is trigger.rotate_triggers, which is a list of enabled triggers. This program will use your existing trigger.enable_rotate value, but please update your config. To update your config while keeping the behavior of your current config, remove trigger.enable_rotate from your config file and set trigger.rotate_triggers to an empty value.')
                sys.exit(0)
        elif options.via_hook not in config['trigger']['rotate_triggers'].split():
            sys.exit(0)

    if options.via_hook is not None:
        xrandr_bug_fail_early(config)

    try:
        new_direction = new_rotation(
            tps.screen.get_rotation(tps.screen.get_internal(config)),
            options.direction, config, options.force_direction)
    except tps.UnknownDirectionException:
        logger.error('Direction cannot be understood.')
        sys.exit(1)
    except tps.screen.ScreenNotFoundException as e:
        logger.error('Unable to determine rotation of "{}": {}'.format(
            tps.screen.get_internal(config), e))
        sys.exit(1)

    rotate_to(new_direction, config)


def rotate_to(direction, config):
    '''
    Performs all steps needed for a screen rotation.
    '''
    tps.hooks.prerotate(direction, config)

    tps.screen.rotate(tps.screen.get_internal(config), direction)
    tps.input.map_rotate_all_input_devices(tps.screen.get_internal(config),
                                           direction)

    if config['rotate'].getboolean('subpixels'):
        if config['rotate'].getboolean('subpixels_with_external') \
           or not tps.screen.get_externals(tps.screen.get_internal(config)):
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
        logger.info('TrackPoint was not found, could not be (de)activated.')
        logger.debug('Exception was: “%s”', str(e))

    try:
        touchpad_xinput_id = tps.input.get_xinput_id('TouchPad')
        tps.input.set_xinput_state(
            touchpad_xinput_id,
            not direction.physically_closed,
        )
    except tps.input.InputDeviceNotFoundException as e:
        logger.info('TouchPad was not found, could not be (de)activated.')
        logger.debug('Exception was: “%s”', str(e))

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
        if not current.physically_closed:
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
    externals = tps.screen.get_externals(tps.screen.get_internal(config))
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
    parser = argparse.ArgumentParser()
    parser.add_argument("direction", nargs='?', help="Positional arguments.")
    parser.add_argument("-v", dest='verbose', action="count",
                        help='Enable verbose output. Can be supplied multiple '
                             'times for even more verbosity.')
    parser.add_argument('--via-hook', help='Let the program know that it was called using the specified hook. You do not need to care about this.')
    parser.add_argument('--force-direction', action='store_true', help='Do not try to be smart. Actually rotate in the direction given even it already is the case.')

    options = parser.parse_args()

    tps.config.set_up_logging(options.verbose)

    return options


if __name__ == "__main__":
    main()
