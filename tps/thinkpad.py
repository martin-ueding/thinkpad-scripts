#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

import argparse
import sys
import logging
import os.path

from daemon import DaemonContext
from lockfile.pidlockfile import PIDLockFile

from tps import check_call
from tps.config import get_config, migrate_shell_config, \
                       print_config, set_up_logging
from tps.dock import dock, get_docking_state
from tps.input import toggle_xinput_state
from tps.rotate import rotate_cmdline, rotate_daemon, xrandr_bug_fail_early

logger = logging.getLogger(__name__)


def main():
    '''Entry point (/usr/bin/thinkpad)'''
    options = _parse_cmdline()
    config = get_config()

    set_up_logging(options.verbose)

    if options.command == 'config':
        print_config(get_config())
    elif options.command == 'dock':
        # Quickly abort if the call is by the hook and the user disabled the trigger.
        if options.via_hook and \
            not config['trigger'].getboolean('enable_dock'):
            sys.exit(0)
        dock(get_docking_state(options.state), config)
    elif options.command == 'input':
        device_name = config['input'][options.input + '_device']
        input_state = parse_input_state(options.state)
        toggle_xinput_state(device_name, input_state)
    elif options.command == 'mutemic':
        check_call(['amixer', 'sset', "'Capture',0", 'toggle'], logger)
    elif options.command == 'rotate':
        rotate(options, config)
    elif options.command == 'scripts-config-migration':
        migrate_shell_config()
    
    sys.exit(0)
    
def main_legacy():
    '''Entry point for legacy entry points (/usr/bin/thinkpad-<name>)'''
    
    # swap progname
    entrypoint_name = os.path.basename(sys.argv[0])
    sys.argv[0] = sys.argv[0].replace(entrypoint_name, "thinkpad")
    
    # translate entrypoint name into command and insert onto argv
    # in the correct position
    i = 1
    while i < len(sys.argv):
        if sys.argv[i].startswith('-v'):
            i += 1
        elif sys.argv[i].startswith('--via-hook'):
            i += 1
            if not sys.argv[i].startswith('-'):
                i += 1
        break
    
    command = entrypoint_name.replace('thinkpad-', '')
    input_device = None
    if command.startswith('touch') or command == 'trackpoint':
        input_device = command
        command = 'input'
    elif command.endswith('-hook'):
        command.replace('-hook', '')
        sys.argv.insert(i, "--via-hook")
        i += 1
        # positional argument to --via-hook
        if command == 'rotate' and not sys.argv[i].startswith('-'):
            i += 1
        
    sys.argv.insert(i, command)
    i += 1
    # positional argument to input command
    if input_device is not None:
        if input_device == 'touch':
            input_device = 'touchscreen'
        sys.argv.insert(i, input_device)
        
    main()
    
def parse_input_state(state):
    if state == 'on':
        return True
    elif state == 'off':
        return False
    else:
        return None
        
def rotate(options, config):
    if options.via_hook is not None:
        xrandr_bug_fail_early(config)
    
    # acpi hook values
    if options.via_hook in ('00000001', '00005009'):
        options.direction = None
    elif options.via_hook in ('00000000', '0000500a'):
        options.direction = 'normal'
        
    if not options.daemonize:
        # Quickly abort if the call is by the hook and the user disabled the trigger.
        if options.via_hook is not None and \
            not config['trigger'].getboolean('enable_rotate'):
            sys.exit(0)
            
        rotate_cmdline(options, config)
    else:
        with DaemonContext(pidfile = PIDLockFile(options.pidfile), \
            stdout = sys.stdout, stderr = sys.stderr):
            rotate_daemon(options, config)
            
def _parse_cmdline():
    """
    Parses the command line arguments.

    If the logging module is imported, set the level according to the number of
    ``-v`` given on the command line.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description='ThinkPad Scripts',
                        epilog='Collection of thinkpad utilility commands')
                        #, version='x.y')
    
    parser.add_argument('-v', dest='verbose', action='count',
                        help='Enable verbose output. Can be supplied '
                        'multiple times for even more verbosity.')
    parser.add_argument('--via-hook', nargs='?',
                        help='Let the program know that it was called '
                        'using the hook. This will then enable some '
                        'workarounds. You do not need to care about this.')
    
    subparsers = parser.add_subparsers(help='commands', dest='command')
    
    subparsers.add_parser('config', help='Display current configuration')
    
    dock = subparsers.add_parser('dock', help='Toggle Docking station state')
    
    dock.add_argument('state', nargs='?', choices=('on', 'off'),
                      help='Desired docking station state. '
                      'Toggle if not specified')
                      
    inputs = subparsers.add_parser('input', help='Input devices')
    
    inputs.add_argument('input',
                        choices=('touchpad', 'touchscreen', 'trackpoint'),
                        help='Input device')
    inputs.add_argument('state', nargs='?', choices=('on', 'off'),
                        help='Desired input device state. '
                        'Toggle if not specified')
                        
    subparsers.add_parser('mutemic', help='Toggle Microphone state')
    
    rotate = subparsers.add_parser('rotate', help='Rotate screen')
    
    rotate.add_argument('--force-direction', action='store_true', 
                        help='Do not try to be smart. Actually rotate '
                        'in the direction given even it already is the '
                        'case')
    rotate.add_argument('direction', nargs='?',
                        choices=('normal', 'none', 'left', 'ccw', 
                        'right', 'cw', 'flip', 'inverted', 'half', 
                        'tablet-normal'),
                        help='Desired screen orientation')
    rotate.add_argument('state', nargs='?', choices=('on', 'off'),
                        help='Forced input devices state after change')
                        
    rotate.add_argument('--daemonize', '-d', action='store_true',
                        help='Daemonize screen rotation to take use of '
                        'HDAPS accelerometer for automatic rotation.')
    rotate.add_argument('--pidfile', '-p', action='store', 
                        default='/var/run/thinkpad-rotated.pid',
                        help='Pid File location for daemon mode')
                        
    subparsers.add_parser('scripts-config-migration', 
                          help='Migrate configuration')
                          
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()
    
if __name__ == '__main__':
    main()
