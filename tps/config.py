#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Martin Ueding <dev@martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

'''
Config module.

Takes care of the INI style config file for global and user configuration.
'''

import configparser
import os.path

import pkg_resources

import termcolor

CONFIGFILE = os.path.expanduser('~/.config/thinkpad-scripts/config.ini')
'Path of global config file'

def get_config():
    '''
    Loads the config from the config files.

    The global config file is read first, then the user config file is read.
    That way, options can be overwritten in the user config file.

    :returns: Config
    :rtype: configparser.ConfigParser
    '''
    config = configparser.ConfigParser()

    default_filename = pkg_resources.resource_filename(__name__, "default.ini")

    config.read(default_filename)
    if os.path.isfile(CONFIGFILE):
        config.read(CONFIGFILE)

    return config

def print_config(config):
    '''
    Pretty prints config with colors.

    :param configparser.ConfigParser config: Config to print
    :returns: None
    '''
    for section in sorted(config.sections()):
        termcolor.cprint(section, attrs=('bold',))

        for key in sorted(config[section]):
            print(termcolor.colored(key, 'yellow'), config[section][key])

def main():
    '''
    Command line entry point.

    :returns: None
    '''
    print_config(get_config())

if __name__ == '__main__':
    main()
