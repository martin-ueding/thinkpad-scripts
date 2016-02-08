#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2014 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

import unittest

import tps.network

class ParseTerseLineTestCase(unittest.TestCase):

    def test_parse_terse_line_no_escape(self):
        expected = ['foo bar', 'baz goo']
        actual = tps.network.parse_terse_line('foo bar:baz goo')
        self.assertEqual(expected, actual)

    def test_parse_terse_line_escape_colon(self):
        expected = ['foo: bar baz', 'goo']
        actual = tps.network.parse_terse_line(r'foo\: bar baz:goo')
        self.assertEqual(expected, actual)

        expected = ['foo', 'bar:baz']
        actual = tps.network.parse_terse_line(r'foo:bar\:baz')
        self.assertEqual(expected, actual)

    def test_parse_terse_line_escape_backslash(self):
        expected = ['foo\\', 'baz']
        actual = tps.network.parse_terse_line(r'foo\\:baz')
        self.assertEqual(expected, actual)

        expected = [r'foo\\ bar', r'baz\goo']
        actual = tps.network.parse_terse_line(r'foo\\\\ bar:baz\\goo')
        self.assertEqual(expected, actual)

    def test_parse_terse_line_escape_both(self):
        expected = ['foo\:', 'bar']
        actual = tps.network.parse_terse_line(r'foo\\\::bar')
        self.assertEqual(expected, actual)
