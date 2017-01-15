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
        self.maxDiff = None

    def assertConfigEqual(self, first, second, msg=None):
        '''
        Compare configurations in ConfigParser objects.

        Ignores any differences in ordering and pretty-prints differences.

        :param first: First configuration
        :param second: Second configuration
        :raises self.failureException(msg):
        '''
        self.assertEqual({sect:dict(first[sect]) for sect in first.sections()},
                         {sect:dict(second[sect]) for sect in second.sections()})


class InterpretShellLineTestCase(ConfigTestCase):
    def test_interpret_shell_line_normal(self):
        '''
        `interpret_shell_line` should work properly with normal input.
        '''
        expected = ConfigParser(interpolation=None)
        expected.read_dict({'network': {'disable_wifi': 'true'},
                            'screen': {'internal_regex': 'LVDS1',
                                       'set_brightness': 'true',
                                       'brightness': '100%',
                                       'relative_position': 'right'},
                            'sound': {'unmute': 'false',
                                      'dock_loudness': '50%',
                                      'undock_loudness': '10%'},
                            'gui': {'kdialog': 'true'},
                            'rotate': {'default_rotation': 'left'},
                            'unity': {'toggle_unity_launcher': 'false'},
                            'vkeyboard': {'program': 'kvkbd'}})

        str_input = ['disable_wifi=true',
                     'internal=LVDS1',
                     'set_brightness=true',
                     'brightness=100%',
                     'relative_position=right',
                     'unmute=false',
                     'dock_loudness=50%',
                     'undock_loudness=10%',
                     'kdialog=true',
                     'default_rotation=left',
                     'toggle_unity_launcher=false',
                     'virtual_kbd=kvkbd']
        actual = ConfigParser(interpolation=None)
        for input in str_input:
            tps.config.interpret_shell_line(input, actual)

        self.assertEqual(expected, actual)

    def test_interpret_shell_line_white_space(self):
        expected = ConfigParser(interpolation=None)
        expected.read_dict({'screen': {'brightness': ' 50%',
                                       'set_brightness': 'true ',
                                       'internal_regex': 'LVDS1',
                                       'relative_position': 'foo bar'},
                            'gui': {'kdialog': 'true'}})

        actual = ConfigParser(interpolation=None)
        tps.config.interpret_shell_line('brightness=" 50%"', actual)
        tps.config.interpret_shell_line("set_brightness='true '", actual)
        tps.config.interpret_shell_line('internal=LVDS1  ', actual)
        tps.config.interpret_shell_line('relative_position="foo bar"', actual)
        tps.config.interpret_shell_line(' kdialog=true', actual)

        self.assertEqual(expected, actual)

    def test_interpret_shell_line_empty_str(self):
        '''
        `interpret_shell_line` should do nothing with an empty string.
        '''
        expected = ConfigParser(interpolation=None)
        actual = ConfigParser(interpolation=None)
        tps.config.interpret_shell_line('', actual)
        self.assertEqual(expected, actual)

    def test_interpret_shell_line_comment(self):
        '''
        `interpret_shell_line` should do nothing with a comment.
        '''
        expected = ConfigParser(interpolation=None)

        actual = ConfigParser(interpolation=None)
        tps.config.interpret_shell_line('#unmute=5', actual)
        self.assertEqual(expected, actual)

        actual = ConfigParser(interpolation=None)
        tps.config.interpret_shell_line(' #unmute=5', actual)
        self.assertEqual(expected, actual)

    def test_interpret_shell_line_unknown_option(self):
        '''
        `interpret_shell_line` should fail with an unknown option.
        '''
        actual = ConfigParser(interpolation=None)
        with self.assertRaises(tps.config.ShellParseException) as cm:
            tps.config.interpret_shell_line('foo=5', actual)
        self.assertEqual('Cannot parse “foo=5”: Not a known option',
                         str(cm.exception))

    def test_interpret_shell_line_multiple_values(self):
        '''
        `interpret_shell_line` should fail with an array value.
        '''
        actual = ConfigParser(interpolation=None)
        with self.assertRaises(tps.config.ShellParseException) as cm:
            tps.config.interpret_shell_line('unmute=(1 2)', actual)
        self.assertEqual('Cannot parse “unmute=(1 2)”: Not a single value',
                         str(cm.exception))

    def test_interpret_shell_line_dollar_sign(self):
        '''
        `interpret_shell_line` should fail with a dollar sign in the value.
        '''
        actual = ConfigParser(interpolation=None)
        with self.assertRaises(tps.config.ShellParseException) as cm:
            tps.config.interpret_shell_line('unmute=$bar', actual)
        self.assertEqual('Cannot parse “unmute=$bar”: Contains “$”, indicates '
                         'complex value', str(cm.exception))

    def test_interpret_shell_line_unclosed_quotes(self):
        '''
        `interpret_shell_line` should fail with unclosed quotes in the value.
        '''
        actual = ConfigParser(interpolation=None)
        with self.assertRaises(tps.config.ShellParseException) as cm:
            tps.config.interpret_shell_line('unmute="bar', actual)
        self.assertEqual('Cannot parse “unmute="bar”: No closing quotation',
                         str(cm.exception))
