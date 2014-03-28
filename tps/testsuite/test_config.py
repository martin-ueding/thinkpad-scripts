#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

import unittest
from configparser import ConfigParser

import tps.config

class ConfigTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ConfigTestCase, self).__init__(*args, **kwargs)
        self.addTypeEqualityFunc(ConfigParser, self.assertConfigEqual)

    def assertConfigEqual(self, first, second, msg=None):
        '''
        Compare configurations in ConfigParser objects.

        :param first: First configuration
        :param second: Second configuration
        :raises self.failureException(msg):
        '''
        self.assertEqual({sect:dict(first[sect]) for sect in first.sections()},
                         {sect:dict(second[sect]) for sect in second.sections()})

    def test_interpret_shell_line(self):
        ref = ConfigParser()
        ref['network'] = {}
        ref['network']['disable_wifi'] = 'foo bar'
        ref['gui'] = {}
        ref['gui']['kdialog'] = 'true'
        act = ConfigParser()
        tps.config.interpret_shell_line('disable_wifi="foo bar"', act)
        tps.config.interpret_shell_line('kdialog=true', act)
        self.assertEqual(ref, act)

        act = ConfigParser()
        with self.assertRaises(tps.config.ShellParseException) as cm:
            tps.config.interpret_shell_line('foo=5', act)
        self.assertEqual('Cannot parse “foo=5”: Not a known option',
                         str(cm.exception))

        act = ConfigParser()
        with self.assertRaises(tps.config.ShellParseException) as cm:
            tps.config.interpret_shell_line('unmute=(1 2)', act)
        self.assertEqual('Cannot parse “unmute=(1 2)”: Not a single value',
                         str(cm.exception))

        act = ConfigParser()
        with self.assertRaises(tps.config.ShellParseException) as cm:
            tps.config.interpret_shell_line('unmute=$bar', act)
        self.assertEqual('Cannot parse “unmute=$bar”: Contains “$”, indicates '
                         'complex value', str(cm.exception))
