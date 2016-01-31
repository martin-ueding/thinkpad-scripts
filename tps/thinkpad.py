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

from tps.config import get_config, migrate_shell_config, \
                       print_config, set_up_logging
from tps.acpi.battery import ThinkpadAcpiBatteryController
from tps.dock import dock, get_docking_state
from tps.compositor import toggle_input_state
from tps.compositor.x11.screen import xrandr_bug_fail_early
from tps.rotate import rotate_cmdline, rotate_daemon
from tps.utils import check_call

logger = logging.getLogger(__name__)


def main():
    '''Entry point (/usr/bin/thinkpad)'''
    options = _parse_cmdline()
    config = get_config()

    set_up_logging(options.verbose)

    if options.command == 'config':
        print_config(get_config())
    elif options.command == 'battery':
        battery(options, config)
    elif options.command == 'dock':
        # Quickly abort if the call is by the hook and the user disabled the trigger.
        if options.via_hook and \
            not config['trigger'].getboolean('enable_dock'):
            sys.exit(0)
        dock(get_docking_state(options.state), config)
    elif options.command == 'input':
        device_name = config['input'][options.input + '_device']
        input_state = parse_input_state(options.state)
        toggle_input_state(device_name, input_state)
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
            if i < len(sys.argv) and not sys.argv[i].startswith('-'):
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
        
def displayThreshhold(level):
    if level == 0:
        print(str(level) + " (default)")
    elif level > 0 and level < 100:
        print(str(level) + " (relative percent)")
    else:
        print(str(level) + " (unknown)")
        
def displayInhibit(result):
    if result.inhibit_charge_status == 1:
        result_str = "yes";
        timer = result.inhibit_charge_effective_timer
        if timer == 0:
            result_str += " (unspecified min)"
        elif timer == 65535:
            result_str += " (forever)"
        else:
            result_str += " (%d min)" % timer
        print(result_str)
    else:
        print('no')
  
def displayForceDischarge(result):
    result_str = 'yes' if result.discharge_status == 1 else 'no'
    if result.break_by_ac_detaching == 1:
        result_str += ' (break on AC detach)'
    print(result_str)
    
def timerType(forInhibitCharge):
    def getInhibitCharge(string):
        timer = 0 if string == '' else int(string)
        ############################################################
        #they are shifting a bit somewhere; the limit should be 1440
        #the same range in peak-shift-state is used, except shifted to the left
        #the value returned by peak-shift-state is the REAL duration, though
        if forInhibitCharge and timer != 65535:
            timer *= 2
        ############################################################

        if timer > 1440 and timer != 65535:
            raise argparse.ArgumentTypeError('Invalid value for <min>: number '
                                             'of minutes, or 0 for never, or '
                                             '65535 for forever')
        return timer
    return getInhibitCharge
        
def battery(options, config):
    batteryController = ThinkpadAcpiBatteryController()
    if options.battery_command in ['ST', 'st', 'start', 'startThreshold']:
        if options.level is not None:
            result = batteryController.setStartThreshold(options.battery, options.level)
        else:
            result = batteryController.getStartThreshold(options.battery)
            displayThreshhold(result)
    elif options.battery_command in ['SP', 'sp', 'stop', 'stopThreshold']:
        if options.level is not None:
            result = batteryController.setStopThreshold(options.battery, options.level)
        else:
            result = batteryController.getStopThreshold(options.battery)
            displayThreshhold(result)
    elif options.battery_command in ['IC', 'ic', 'inhibit', 'inhibitCharge']:
        if options.inhibit is not None:
            result = batteryController.setInhibitCharge(options.battery, options.inhibit, options.min)
        else:
            result = batteryController.getInhibitCharge(options.battery)
            displayInhibit(result)
    elif options.battery_command in ['FD', 'fd', 'forceDischarge']:
        print(options)
        if options.discharge is not None:
            result = batteryController.setForceDischarge(options.battery, options.discharge, options.acbreak)
        else:
            result = batteryController.getForceDischarge(options.battery)
            displayForceDischarge(result)
    elif options.battery_command in ['PS', 'ps', 'peakShiftState']:
        result = batteryController.setPeakShiftState(options.inhibit, options.min)
    elif options.battery_command == 'list':
        raise NotImplemented('Feature not yet implemented')
        
def rotate(options, config):
    if options.via_hook is not None:
        # TODO: get rid of this if possible to remain compositor agnostic
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
            
def _tpacpi_bat_cmdline_compat():
    '''Modify argv to make the cmdline api compatibile with tpacpi-bat'''
    if len(sys.argv) > 2 and 'battery' in sys.argv:
        i = 1
        args = ','.join(['--st', '--start', '--startThreshold'
                '--sp', '--stop', '--stopThreshold'
                '--ic', '--inhibit', '--inhibitCharge'
                '--fd', '--forceDischarge'
                '--ps', '--peakShiftState'])
        while i < len(sys.argv):
            if sys.argv[i] in args:
                sys.argv[i] = sys.argv[i].replace('--', '')
            i += 1
            
def _parse_cmdline():
    """
    Parses the command line arguments.

    If the logging module is imported, set the level according to the number of
    ``-v`` given on the command line.

    :return: Namespace with arguments.
    :rtype: Namespace
    """
    
    _tpacpi_bat_cmdline_compat()
    
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
                        
    parser.add_argument('--version', action='version', version='%(prog)s 4.7.1')
    
    commands = parser.add_subparsers(title='Available commands',
                                     description='Valid subcommands', 
                                     help='commands', dest='command')
    
    commands.add_parser('config', help='Display current configuration')
    
    battery = commands.add_parser('battery', help='Battery management')
    
    # only to achieve compatibility with tpacpi-bat utility - NO OP
    battery_ops = battery.add_mutually_exclusive_group(required=True)
    battery_ops.add_argument('--get', '-g', action='store_const', 
                             dest='batop', const='get', 
                             help='Get value. No action argument - for '
                             'CLI compatibility with tpacpi-bat')
    battery_ops.add_argument('--set', '-s', action='store_const', 
                             dest='batop', const='set', 
                             help='Set value. No action argument - for '
                             'CLI compatibility with tpacpi-bat')
    
    battery_cmds = battery.add_subparsers(title='Available battery commands',
                                          description='Exposes ACPI interface '
                                          'for battery controls to change: '
                                          'force discharge, inhibit charge, '
                                          'start/stop charge threshold and '
                                          'peak shift state.',
                                       help='Battery commands with aliases',
                                       dest='battery_command')
    
    battery_st = battery_cmds.add_parser('ST', aliases=['st', 'start', 
                                        'startThreshold'], 
                                         help='Start charge threshold')
    
    battery_st.add_argument('battery', type=int, choices=range(0,3),
                            help='Battery selection: 1 for main, 2 for '
                            'secondary, 0 for either/both')
                            
    battery_st.add_argument('level', nargs='?', type=int, 
                            choices=range(0, 100), default=None,
                            help='Charge level: 0 for default, 1-99 for '
                            'percentage')
    
    battery_sp = battery_cmds.add_parser('SP', aliases=['sp', 'stop', 
                                         'stopThreshold'], 
                                         help='Stop charge threshold')
                                         
    battery_sp.add_argument('battery', type=int, choices=range(0,3),
                            help='Battery selection: 1 for main, 2 for '
                            'secondary, 0 for either/both')
                            
    battery_sp.add_argument('level', nargs='?', type=int, 
                            choices=range(0, 100), default=None,
                            help='Charge level: 0 for default, 1-99 for '
                            'percentage')
    
    battery_ic = battery_cmds.add_parser('IC', aliases=['ic', 'inhibit',
                                         'inhibitCharge'], 
                                         help='Inhibit Charge')
                                         
    battery_ic.add_argument('battery', type=int, choices=range(0,3),
                            help='Battery selection: 1 for main, 2 for '
                            'secondary, 0 for either/both')
                            
    battery_ic.add_argument('inhibit', nargs='?', type=int, 
                            choices=range(0, 2), default=None,
                            help='Charging inhibition: 1 to inhibit '
                            'charge, 0 for stop inhibiting charge')
                            
    battery_ic.add_argument('min', nargs='?', type=timerType(True), default=0,
                            help='Time in minutes: 1-720 or 0 for never, '
                            'or 65535 for forever.')
                                         
    battery_fd = battery_cmds.add_parser('FD', aliases=['fd', 
                                         'forceDischarge'], 
                                         help='Force discharge')
                                         
    battery_fd.add_argument('battery', type=int, choices=range(0,3),
                            help='Battery selection: 1 for main, 2 for '
                            'secondary, 0 for either/both')
                            
    battery_fd.add_argument('discharge', nargs='?', type=int, choices=range(0, 2),
                            default=None, help='Force Discharge: 1 for force '
                            'discharge, 0 for stop forcing discharge')
                            
    battery_fd.add_argument('acbreak', nargs='?', type=int, choices=range(0,2),
                            default=0, help='AC Detached stop: 1 to '
                            'stop forcing when AC is detached, 0 '
                            'to continue')
                                         
    battery_ps = battery_cmds.add_parser('PS', aliases=['ps', 
                                         'peakShiftState'], 
                                         help='Peak shift state')
                                         
    battery_ps.add_argument('inhibit', type=int, choices=range(0, 2),
                            help='Charging inhibition: 1 to inhibit '
                            'charge, 0 for stop inhibiting charge')
                            
    battery_ps.add_argument('min', nargs='?', type=timerType(False), default=0,
                            help='Time in minutes: 1-1440 or 0 for '
                            'never, or 65535 for forever.')
                            
    battery_cmds.add_parser('list', help='List known power devices')

    
    dock = commands.add_parser('dock', help='Toggle Docking station state')
    
    dock.add_argument('state', nargs='?', choices=('on', 'off'),
                      help='Desired docking station state. '
                      'Toggle if not specified')
                      
    inputs = commands.add_parser('input', help='Input devices')
    
    inputs.add_argument('input',
                        choices=('touchpad', 'touchscreen', 'trackpoint'),
                        help='Input device')
    inputs.add_argument('state', nargs='?', choices=('on', 'off'),
                        help='Desired input device state. '
                        'Toggle if not specified')
                        
    commands.add_parser('mutemic', help='Toggle Microphone state')
    
    rotate = commands.add_parser('rotate', help='Rotate screen')
    
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
                        
    commands.add_parser('scripts-config-migration', 
                        help='Migrate configuration')
                          
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()
    
if __name__ == '__main__':
    main()
