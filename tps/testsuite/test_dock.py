#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2015 Jim Turner <jturner314@gmail.com>
# Licensed under The GNU Public License Version 2 (or later)

import unittest

import tps.dock

def set_externals(externals):
    def get_externals(internal):
        return externals
    tps.dock.tps.screen.get_externals = get_externals

class SelectDockingScreensTestCase(unittest.TestCase):

    def test_select_docking_screens_internal_only(self):
        set_externals([])
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', '', ''),
            ('LVDS1', None, []))

    def test_select_docking_screens_single_external_infer_both(self):
        set_externals(['VGA1'])
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', '', ''),
            ('VGA1', 'LVDS1', []))

    def test_select_docking_screens_dual_external_infer_both(self):
        set_externals(['VGA1', 'HDMI1'])
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', '', ''),
            ('VGA1', 'HDMI1', ['LVDS1']))

    def test_select_docking_screens_single_external_infer_primary(self):
        set_externals(['VGA1'])
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', '', 'LVDS1'),
            ('VGA1', 'LVDS1', []))
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', '', 'VGA1'),
            ('LVDS1', 'VGA1', []))

    def test_select_docking_screens_dual_external_infer_primary(self):
        set_externals(['VGA1', 'HDMI1'])
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', '', 'LVDS1'),
            ('VGA1', 'LVDS1', ['HDMI1']))
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', '', 'VGA1'),
            ('HDMI1', 'VGA1', ['LVDS1']))
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', '', 'HDMI1'),
            ('VGA1', 'HDMI1', ['LVDS1']))

    def test_select_docking_screens_single_external_infer_secondary(self):
        set_externals(['VGA1'])
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'LVDS1', ''),
            ('LVDS1', 'VGA1', []))
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'VGA1', ''),
            ('VGA1', 'LVDS1', []))

    def test_select_docking_screens_dual_external_infer_secondary(self):
        set_externals(['VGA1', 'HDMI1'])
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'LVDS1', ''),
            ('LVDS1', 'VGA1', ['HDMI1']))
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'VGA1', ''),
            ('VGA1', 'HDMI1', ['LVDS1']))
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'HDMI1', ''),
            ('HDMI1', 'VGA1', ['LVDS1']))

    def test_select_docking_screens_single_external_infer_neither(self):
        set_externals(['VGA1'])
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'LVDS1', 'VGA1'),
            ('LVDS1', 'VGA1', []))
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'VGA1', 'LVDS1'),
            ('VGA1', 'LVDS1', []))

    def test_select_docking_screens_dual_external_infer_neither(self):
        set_externals(['VGA1', 'HDMI1'])
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'LVDS1', 'VGA1'),
            ('LVDS1', 'VGA1', ['HDMI1']))
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'LVDS1', 'HDMI1'),
            ('LVDS1', 'HDMI1', ['VGA1']))
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'VGA1', 'LVDS1'),
            ('VGA1', 'LVDS1', ['HDMI1']))
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'VGA1', 'HDMI1'),
            ('VGA1', 'HDMI1', ['LVDS1']))
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'HDMI1', 'VGA1'),
            ('HDMI1', 'VGA1', ['LVDS1']))
        self.assertEqual(
            tps.dock.select_docking_screens('LVDS1', 'HDMI1', 'LVDS1'),
            ('HDMI1', 'LVDS1', ['VGA1']))

    def test_select_docking_screens_internal_only_bad_config(self):
        set_externals([])
        with self.assertLogs(tps.dock.logger, level='WARNING') as cm:
            self.assertEqual(
                tps.dock.select_docking_screens('LVDS1', 'foo', 'bar'),
                ('LVDS1', None, []))
        self.assertEqual(
            cm.output, ['WARNING:tps.dock:Configured screen "foo" does not '
                        'exist or is not connected.',
                        'WARNING:tps.dock:Configured screen "bar" does not '
                        'exist or is not connected.'])

    def test_select_docking_screens_single_external_bad_config(self):
        set_externals(['VGA1'])
        with self.assertLogs(tps.dock.logger, level='WARNING') as cm:
            self.assertEqual(
                tps.dock.select_docking_screens('LVDS1', 'LVDS1', 'foo'),
                ('LVDS1', 'VGA1', []))
        self.assertEqual(
            cm.output, ['WARNING:tps.dock:Configured screen "foo" does not '
                        'exist or is not connected.'])

    def test_select_docking_screens_dual_external_bad_config(self):
        set_externals(['VGA1', 'HDMI1'])
        with self.assertLogs(tps.dock.logger, level='WARNING') as cm:
            self.assertEqual(
                tps.dock.select_docking_screens('LVDS1', 'LVDS1', 'foo'),
                ('LVDS1', 'VGA1', ['HDMI1']))
        self.assertEqual(
            cm.output, ['WARNING:tps.dock:Configured screen "foo" does not '
                        'exist or is not connected.'])
