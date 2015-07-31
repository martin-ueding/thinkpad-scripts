#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2014-2015 Martin Ueding <dev@martin-ueding.de>
# Copyright © 2015 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

'''
Attempts to find the currently logged in user using the graphical session.
'''

import configparser
import logging
import os.path
import re
import subprocess
import sys

import tps
import tps.config

logger = logging.getLogger(__name__)

def get():
    '''
    Get the currently logged in user.

    This uses the various methods implemented in this module automatically
    until a sensible result is found.
    '''
    methods = [
        _get_loginctl,
        _get_who,
        _get_pgrep,
    ]

    for method in methods:
        result = method()
        if result is not None:
            logger.info('Found a sensible user with %s.', method.__name__)
            return result

    return None


def _get_who():
    '''
    Get the currently logged in user via ``who -u``.
    '''
    pattern = re.compile(r'\(:0(\.0)?\)')

    lines = tps.check_output(['who', '-u'], logger).decode().split('\n')
    for line in lines:
        m = pattern.search(line)
        if m:
            words = line.split()
            return words[0]

    logger.warning('Could not determine user with `who -u`.')
    return None


def _get_pgrep():
    '''
    Get the currently logged in user by searching for X.org user.

    Since ``who -u`` does not give a result in every case (see GH-107__), we
    also use ``pgrep`` to search for the user of the currently running instance
    of X.org.

    __ https://github.com/martin-ueding/thinkpad-scripts/issues/107
    '''
    pgrep_output = tps.check_output([
        'pgrep', '-f',
        r'^/usr/(local/)?(bin|lib)/([^[:blank:]]+/)?(Xorg|X)([[:blank:]]+|$)'],
        logger)
    pids = pgrep_output.decode().strip().split()

    logger.debug('pgrep gave PIDs: %s', ', '.join(pids))

    if len(pids) > 1:
        logger.warning('There are two instances of X.org running. I cannot '
                       'decide which is the user which should have the script '
                       'executed on behalf. PIDs are %s', ', '.join(pids))
        return None

    if len(pids) == 0:
        logger.warning('No X.org seems to be running.')
        return None

    ps_output = tps.check_output(['ps', '--no-headers', '--format=euser',
                                 pids[0]], logger)
    uid_str = ps_output.decode().strip()

    if uid_str == 'root':
        logger.warning('X server is running as root. User cannot be determined this way.')
        return None

    return uid_str


def _try_get_graphical_user(session):
    '''
    Returns username for graphical sessions, ``None`` otherwise.

    :param str session: Session ID
    :rtype: str or None
    '''
    def prop_getter(prop):
        output = tps.check_output(['loginctl', 'show-session', session, '--property='+prop], logger)
        line = output.decode().strip()
        return line[len(prop) + 1:]

    user = prop_getter('Name')
    active = prop_getter('Active')
    class_ = prop_getter('Class')
    type_ = prop_getter('Type')

    logger.debug(
        'Session %s has user `%s`, active `%s`, class `%s`, type `%s`.',
        session, user, active, class_, type_)

    if active == 'yes' and class_ == 'user' and type_ == 'x11':
        return user
    else:
        return None



def _loginctl_sessions():
    '''
    Retrieves list of sessions.

    :rtype: list of str
    '''
    output = tps.check_output(['loginctl', 'list-sessions', '--no-legend'], logger)
    lines = output.decode().split('\n')

    pattern = re.compile(r'(?P<session>\d+)\s*(?P<uid>\d+)\s*(?P<user>\S+)\s*(?P<seat>\S+)')

    sessions = []

    for line in lines:
        matcher = pattern.search(line)
        if matcher:
            group_dict = matcher.groupdict()
            sessions.append(group_dict['session'])

    unique = list(set(sessions))
    logger.debug('Unique session ids: %s', repr(unique))
    return unique


def _get_loginctl():
    '''
    Get the currently logged in user by asking ``loginctl``.
    '''
    sessions = _loginctl_sessions()
    try_users = [_try_get_graphical_user(session) for session in sessions]
    users = [user for user in try_users if user is not None]

    if len(users) == 1:
        return users[0]
    else:
        logging.debug('Users determined active by loginctl are: %s', repr(users))
        return None


if __name__ == '__main__':
    tps.config.set_up_logging(2)
    print('Active user:', get())
