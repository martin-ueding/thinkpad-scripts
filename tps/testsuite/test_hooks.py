#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2017 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

import unittest

import tps.input

class ParseGraphicalUserTestCase(unittest.TestCase):

    def test_parse_graphical_user_single(self):
        lines = [
            'foo      tty1         2017-03-14 16:14 21:11         683',
        ]
        user = tps.hooks.parse_graphical_user(lines)
        self.assertEqual(user, 'foo')

    def test_parse_graphical_user_display_zero(self):
        lines = [
            'bar     tty1         2017-03-14 12:02 23:25        683',
            'foo     tty1         2017-03-14 12:02 23:25        683 (:0)',
            'baz     tty1         2017-03-14 12:02 23:25        683',
        ]
        user = tps.hooks.parse_graphical_user(lines)
        self.assertEqual(user, 'foo')

    def test_parse_graphical_user_display_zero_point_zero(self):
        lines = [
            'bar     tty1         2017-03-14 12:02 23:25        683',
            'foo     tty1         2017-03-14 12:02 23:25        683 (:0.0)',
            'baz     tty1         2017-03-14 12:02 23:25        683',
        ]
        user = tps.hooks.parse_graphical_user(lines)
        self.assertEqual(user, 'foo')

    def test_parse_graphical_user_display_one(self):
        lines = [
            'bar     tty1         2017-03-14 12:02 23:25        683',
            'foo     tty1         2017-03-14 12:02 23:25        683 (:1)',
            'baz     tty1         2017-03-14 12:02 23:25        683',
        ]
        user = tps.hooks.parse_graphical_user(lines)
        self.assertEqual(user, 'foo')

    def test_parse_graphical_user_display_zero_with_one(self):
        lines = [
            'bar     tty1         2017-03-14 12:02 23:25        683 (:1)',
            'foo     tty1         2017-03-14 12:02 23:25        683 (:0)',
            'baz     tty1         2017-03-14 12:02 23:25        683',
        ]
        user = tps.hooks.parse_graphical_user(lines)
        self.assertEqual(user, 'foo')
