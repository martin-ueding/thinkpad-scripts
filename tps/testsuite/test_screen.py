# Copyright © 2017 Martin Ueding <martin-ueding.de>
# Licensed under The GNU Public License Version 2 (or later)

import unittest

import tps.screen


class XrandrParserTestCase(unittest.TestCase):
    def test_xrandr_parsing(self):
        output = '''Screen 0: minimum 320 x 200, current 3286 x 1080, maximum 8192 x 8192
LVDS-1 connected 1366x768+1920+0 (normal left inverted right x axis y axis) 277mm x 156mm
   1366x768      60.02*+
   1024x768      60.04    60.00  
   960x720       60.00  
   928x696       60.05  
   896x672       60.01  
   800x600       60.00    60.32    56.25  
   700x525       59.98  
   640x512       60.02  
   640x480       60.00    59.94  
   512x384       60.00  
   400x300       60.32    56.34  
   320x240       60.05  
VGA-1 disconnected (normal left inverted right x axis y axis)
HDMI-1 disconnected (normal left inverted right x axis y axis)
DP-1 disconnected (normal left inverted right x axis y axis)
HDMI-2 disconnected (normal left inverted right x axis y axis)
HDMI-3 disconnected (normal left inverted right x axis y axis)
DP-2 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 509mm x 286mm
   1920x1080     60.00*+
   1600x900      60.00  
   1280x1024     75.02    60.02  
   1152x864      75.00  
   1024x768      75.03    60.00  
   800x600       75.00    60.32  
   640x480       75.00    59.94  
   720x400       70.08  
DP-3 disconnected (normal left inverted right x axis y axis)'''

        self.assertEqual(tps.screen.get_available_screens(output), ['DP-2', 'LVDS-1'])

    def test_filter_outputs(self):
        outputs = ['DP-2', 'LVDS-1']
        regex = r'LVDS-?1|eDP-?1'
        self.assertEqual(tps.screen.filter_outputs(outputs, regex), 'LVDS-1')

    def test_filter_outputs_assert(self):
        outputs = ['eDP1', 'LVDS-1']
        regex = r'LVDS-?1|eDP-?1'
        with self.assertRaises(AssertionError):
            tps.screen.filter_outputs(outputs, regex)
