# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

import errno
from functools import wraps
import logging
import os
import shlex
import subprocess

logger = logging.getLogger(__name__)


def command_exists(command):
    '''
    Checks whether a given command is installed on this system.

    :param str command: Name of command
    :returns: Whether command is found and executable
    :rtype: bool
    '''
    def is_exe(path):
        return os.path.isfile(path) and os.access(path, os.X_OK)

    # Check if `command` is a path to an executable
    if os.sep in command:
        if is_exe(os.path.expanduser(command)):
            logger.debug(_('Command “{}” found.').format(command))
            return True

    # Check if `command` is an executable on PATH
    else:
        for dir in os.get_exec_path():
            if is_exe(os.path.join(dir, command)):
                logger.debug(_('Command “{}” found.').format(command))
                return True

    logger.debug(_('Command “{}” not found.').format(command))
    return False
    
def command_toggle_state(program, state):
    '''
    Toggles the running state of the given progam.

    If state is true, the program will be spawned.

    :param str program: Name of the program
    :param bool state: Desired state
    :returns: None
    '''
    if state:
        try:
            check_output(['pgrep', program], logger)
        except subprocess.CalledProcessError:
            if command_exists(program):
                logger.debug(program)
                subprocess.Popen([program])
            else:
                logger.warning(_('{} is not installed').format(program))
    else:
        try:
            check_output(['pgrep', program], logger)
            check_call(['killall', program], logger)
        except subprocess.CalledProcessError:
            pass


def print_command_decorate(function):
    '''
    Decorates a func from the subprocess module to log the `command` parameter.

    Note that the wrapper adds an additional `local_logger` parameter following
    the `command` parameter that is used for the logging. All other parameters
    are passed to the wrapped function.

    :param function: Function to wrap
    :returns: Decorated function
    '''
    @wraps(function)
    def wrapper(command, local_logger, *args, **kwargs):
        shell_command = ' '.join(map(shlex.quote,command))
        local_logger.debug('subprocess “{}”'.format(' '.join(shell_command)))
        #kwargs['stderr'] = subprocess.STDOUT
        return function(command, *args, **kwargs)
    return wrapper
    
check_call = print_command_decorate(subprocess.check_call)
call = print_command_decorate(subprocess.call)
check_output = print_command_decorate(subprocess.check_output)

def fileExists(file):
    return os.path.exists(file)

def fileReadBoolean(file, errMsg):
    return fileReadInt(file, errMsg) == 1
    
def fileReadHex(file, errMsg):
    return int(fileRead(file, errMsg), 16)
    
def fileReadInt(file, errMsg):
    return int(fileRead(file, errMsg))

def fileRead(file, errMsg):
    try:
        with open(file, 'r') as f:
            return f.read().strip()
    except (IOError, OSError) as e:
        if e.errno == errno.ENXIO and fileExists(file):
            # sometimes even though file exists we can't read it
            logger.debug(errMsg)
            logger.debug(e)
            return None
        else:
            logger.error(errMsg)
            logger.error(e)
            raise
        
def fileReadLines(file, errMsg):
    try:
        lines = []
        with open(file, 'r') as f:
            for line in f:
                lines.append(line.strip())
        return lines
    except (IOError, OSError) as e:
        if e.errno == errno.ENXIO and fileExists(file):
            # sometimes even though file exists we can't read it
            logger.debug(errMsg)
            logger.debug(e)
            return []
        else:
            logger.error(errMsg)
            logger.error(e)
            raise

def fileReadLineValue(file, valueName, errMsg):
    try:
        with open(file, 'r') as f:
            for line in f:
                if line.startswith(valueName + ":"):
                    return fileGetLineValue(line)
        raise ValueError(_('Unable to read value named: %s') % valueName)
    except (IOError, OSError) as e:
        if e.errno == errno.ENXIO and fileExists(file):
            # sometimes even though file exists we can't read it
            logger.debug(errMsg)
            logger.debug(e)
            return None
        else:
            logger.error(errMsg)
            logger.error(e)
            raise

def fileGetLineValue(line):
    return line.split(':')[-1].strip()

def fileWriteBoolean(file, errMsg, data):
    return fileWriteInt(file, errMsg, 1 if data else 0)
    
def fileWriteHex(file, errMsg, data):
    return fileWrite(file, errMsg, hex(data))
    
def fileWriteInt(file, errMsg, data):
    return fileWrite(file, errMsg, str(data))

def fileWrite(file, errMsg, *lines):        
    try:
        with open(file, 'w') as f:
            for line in lines:
                f.write(str(line))
            f.flush()
        return True
    except IOError as e:
        logger.error(errMsg)
        logger.error(e)
        return False

class DictInitialised(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
