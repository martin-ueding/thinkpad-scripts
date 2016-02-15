# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

import glob
import logging
import os
import sys

from tps.utils import fileExists, fileRead, fileReadLines, \
                      fileReadLineValue, fileGetLineValue, \
                      fileReadBoolean, fileReadHex, fileReadInt, \
                      fileWrite, fileWriteBoolean, fileWriteHex, \
                      fileWriteInt

'''Interface to thinkpad_acpi kernel module via sysfs under:
/proc/acpi/ibm/
/sys/devices/platform/thinkpad_acpi/
/sys/devices/platform/thinkpad_hwmon/
and additionally:
/sys/devices/platform/dock.*

Info and docs:
https://www.kernel.org/doc/Documentation/laptops/thinkpad-acpi.txt
http://www.thinkwiki.org/wiki/Tablet_Hardware_Buttons
http://www.thinkwiki.org/wiki/Table_of_thinkpad-acpi_LEDs
'''

logger = logging.getLogger(__name__)

class ThinkpadAcpi(object):
    '''Class for interacting with Thinkpad ACPI Extras kernel module.
    '''
    
    THINKPAD_ACPI_PROC_BASE = '/proc/acpi/ibm/'
    
    THINKPAD_ACPI_PROC_BEEP = THINKPAD_ACPI_PROC_BASE + 'beep'
    
    THINKPAD_ACPI_PROC_FAN = THINKPAD_ACPI_PROC_BASE + 'fan'
    
    THINKPAD_ACPI_PROC_LED = THINKPAD_ACPI_PROC_BASE + 'led'
    
    THINKPAD_ACPI_PROC_LIGHT = THINKPAD_ACPI_PROC_BASE + 'light'
    
    THINKPAD_ACPI_PROC_VIDEO = THINKPAD_ACPI_PROC_BASE + 'video'
    
    THINKPAD_ACPI_PROC_VOLUME = THINKPAD_ACPI_PROC_BASE + 'volume'
    
    THINKPAD_ACPI_PROC_THERMAL = THINKPAD_ACPI_PROC_BASE + 'thermal'
    
    THINKPAD_ACPI_SYSFS_BASE = '/sys/devices/platform/thinkpad_acpi/'
    
    # Send CMOS command (rw)
    CMOS_COMMAND = THINKPAD_ACPI_SYSFS_BASE + 'cmos_command'
    
    # Whether Bluetooth is enabled (rw)
    BLUETOOTH_ENABLED = THINKPAD_ACPI_SYSFS_BASE + 'bluetooth_enable'
    # Whether Radio is On (ro)
    RADIO_SWITCH = THINKPAD_ACPI_SYSFS_BASE + 'hotkey_radio_sw'
    # Is Tablet sievel down (ro)
    TABLET_MODE = THINKPAD_ACPI_SYSFS_BASE + 'hotkey_tablet_mode'
    
    # All hotkeys enabled mask (ro)
    ALL_MASK = THINKPAD_ACPI_SYSFS_BASE + 'hotkey_all_mask'
    # Current hotkeys enabled (rw)
    MASK = THINKPAD_ACPI_SYSFS_BASE + 'hotkey_mask'
    # Polling frequency (rw)
    POLL_FREQ = THINKPAD_ACPI_SYSFS_BASE + 'hotkey_poll_freq'
    # Recommended hotkeys enabled mask (ro)
    RECOMMENDED_MASK = THINKPAD_ACPI_SYSFS_BASE + 'hotkey_recommended_mask'
    # (ro)
    SOURCE_MASK = THINKPAD_ACPI_SYSFS_BASE + 'hotkey_source_mask'
    
    LEDS_BASE = THINKPAD_ACPI_SYSFS_BASE + 'leds/'
    
    LEDS_GLOB = LEDS_BASE + 'tpacpi*'
    
    DOCK_STATIONS = '/sys/devices/platform/dock.*'
    
    GPU_BBSWITCH = '/proc/acpi/bbswitch'
    
    LEDS = [ 'power', 'orange:batt', 'green:batt',
        'dock_active', 'bay_active', 'dock_batt',
        'unknown_led', 'standby', 'dock_status1',
        'dock_status2', 'unknown_led2', 'unknown_led3',
        'thinkvantage' ]
    
    @staticmethod
    def beep(sound):
        fileWriteInt(ThinkpadAcpi.THINKPAD_ACPI_PROC_BEEP, \
            'Unable to emit sound!', sound)
        
    @staticmethod
    def hasFan():
        return fileExists(ThinkpadAcpi.THINKPAD_ACPI_PROC_FAN)
    
    @staticmethod
    def getFanState():
        status = speed = level = None
        for line in fileReadLines(ThinkpadAcpi.THINKPAD_ACPI_PROC_FAN, \
            'Unable to read Fan State'):
            if line.startswith('status:'):
                status = fileGetLineValue(line)
            if line.startswith('speed:'):
                speed = int(fileGetLineValue(line))
            if line.startswith('level:'):
                level = ThinkpadAcpi.getFanLevelInt(fileGetLineValue(line))
        return {'status': status,
                'level': level,
                'rpm': speed}
        
    @staticmethod
    def setFanSpeed(speed):
        '''Set fan to specified level:
        0=off, 1-7=normal, 254=disengaged, 255=auto, 256=full-speed
        '''
        fanState = ThinkpadAcpi.getFanState()
        
        if speed == fanState['level']:
            logger.debug(_('Keeping the current fan level unchanged'))
        else:
            logger.debug(_('Setting fan level to ') + str(speed))
            if speed == 0:
                fileWrite(ThinkpadAcpi.THINKPAD_ACPI_PROC_FAN, \
                    _('Unable to set Fan Speed'), 'disable')
            else:
                fileWrite(ThinkpadAcpi.THINKPAD_ACPI_PROC_FAN, \
                    _('Unable to set Fan Speed'), 'enable', 
                    'level %s' % ThinkpadAcpi.getFanLevelStr(speed))
    
    @staticmethod
    def getFanLevelInt(speed):
        if speed == 'disengaged':
            return 254
        elif speed == 'auto':
            return 255
        elif speed == 'full-speed':
            return 256
        else:
            return int(speed)
    
    @staticmethod
    def getFanLevelStr(speed):
        if speed == 254:
            return 'disengaged'
        elif speed == 255:
            return 'auto'
        elif speed == 256:
            return 'full-speed'
        else:
            return str(speed)
    
    @staticmethod
    def sendCmosCommand(data):
        return fileWrite(ThinkpadAcpi.CMOS_COMMAND, \
            _('Unable to send CMOS Command!'), data)
    
    @staticmethod
    def hasBluetooth():
        return fileExists(ThinkpadAcpi.BLUETOOTH_ENABLED)
        
    @staticmethod
    def isBluetoothEnabled():
        '''Whether Bluetooth is enabled
        '''
        if not ThinkpadAcpi.hasBluetooth():
            return False
            
        return fileReadBoolean(ThinkpadAcpi.BLUETOOTH_ENABLED, \
            _('Unable to detect Bluetooth status!'))
        
    @staticmethod
    def setBluetoothEnabled(enabled):
        if not ThinkpadAcpi.hasBluetooth():
            return False
        return fileWriteBoolean(ThinkpadAcpi.BLUETOOTH_ENABLED, \
            _('Unable to set Bluetooth status!'), enabled)
    
    @staticmethod
    def hasTabletMode():
        return fileExists(ThinkpadAcpi.TABLET_MODE)

    @staticmethod
    def inTabletMode():
        '''Whether tablet sievel is rotated
        '''
        if not ThinkpadAcpi.hasTabletMode():
            return False            
        return fileReadBoolean(ThinkpadAcpi.TABLET_MODE, \
            _('Unable to detect Tablet Mode!'))
        
    @staticmethod
    def getAllMask():
        return fileReadHex(ThinkpadAcpi.ALL_MASK, \
            _('Unable to obtain Hotkey All Mask!'))
            
    @staticmethod
    def getMask():
        return fileReadHex(ThinkpadAcpi.MASK, \
            _('Unable to obtain Hotkey Mask!'))
            
    @staticmethod
    def setMask(data):
        return fileWriteHex(ThinkpadAcpi.MASK, \
            _('Unable to obtain Hotkey Mask!'), data)
            
    @staticmethod
    def getPollingFrequency():
        return fileReadHex(ThinkpadAcpi.POLL_FREQ, \
            _('Unable to obtain Polling Frequency!'))
            
    @staticmethod
    def setPollingFrequency(data):
        return fileWriteHex(ThinkpadAcpi.POLL_FREQ, \
            _('Unable to obtain Polling Frequency!'), data)
            
    @staticmethod
    def getRecommendedMask():
        return fileReadHex(ThinkpadAcpi.RECOMMENDED_MASK, \
            _('Unable to obtain Hotkey Recommended Mask!'))
            
    @staticmethod
    def getSourceMask():
        return fileReadHex(ThinkpadAcpi.SOURCE_MASK, \
            _('Unable to obtain Hotkey Source Mask!'))
        
    @staticmethod
    def hasBbSwitch():
        return os.path.exists(ThinkpadAcpi.GPU_BBSWITCH)

    @staticmethod
    def getBbSwitchState():
        state = fileRead(ThinkpadAcpi.GPU_BBSWITCH, \
            _('Unable to obtain BB Switch State!'))
        if state == 'ON':
            return True
        elif state == 'OFF':
            return False
        else:
            raise NameError(_('Unknown bbswitch state'))
            
    @staticmethod
    def isDocked():
        '''
        Determines whether the laptop is on a docking station.

        This checks for ``/sys/devices/platform/dock.*/docked``.

        :returns: True if laptop is docked
        :rtype: bool
        '''
        dockfiles = glob.glob(ThinkpadAcpi.DOCK_STATIONS)
        for dockfile in dockfiles:
            with open(dockfile) as handle:
                contents = handle.read()
                dock_state = int(contents) == 1
                if dock_state:
                    logger.info(_('Docking station found.'))
                    return True
        logger.info(_('No docking station found.'))
        return False

    @staticmethod
    def hasThinkLight():
        return fileExists(ThinkpadAcpi.THINKPAD_ACPI_PROC_LIGHT)

    @staticmethod
    def getThinkLightState():
        return 'on' == fileReadLineValue(
            ThinkpadAcpi.THINKPAD_ACPI_PROC_LIGHT, 'status', \
            _('Unable to read ThinkLight State'))

    @staticmethod
    def setThinkLightState(state):
        fileWrite(ThinkpadAcpi.THINKPAD_ACPI_PROC_LIGHT, \
            _('Unable to read ThinkLight State'), \
            'on' if state == True else 'off')

    @staticmethod
    def getAvailableLeds():
        ledFiles = glob.glob(ThinkpadAcpi.LEDS_GLOB)
        leds = [ ThinkpadAcpi._getLedNameFromFileName(ledFile) for ledFile in ledFiles ]
        if 'thinklight' not in leds and ThinkpadAcpi.hasThinkLight():
            leds.append('thinklight')
        return leds

    @staticmethod
    def hasLed(ledName):
        '''Check if led file exists in sysfs'''
        return fileExists(ThinkpadAcpi._getLedFileName(ledName))

    @staticmethod
    def getLedState(led):
        if isinstance(led, int):
            # translate LED ID to LED name to read state via sysfs
            if led < 0 and led > 15:
                raise ValueError(_('Invalid LED ID'))
            if led > len(ThinkpadAcpi.LEDS) - 1:
                raise ValueError(_('LED ID to name mapping is unknown. '
                    'Unable to read LED State'))
            ledName = ThinkpadAcpi.LEDS[led]
        else:
            ledName = led

        if ledName == 'thinklight' and not ThinkpadAcpi.hasLed(ledName):
            return ThinkpadAcpi.hasThinkLight() \
                and ThinkpadAcpi.getThinkLightState()

        brightness = fileReadInt(ThinkpadAcpi._getLedFileName(ledName) \
            + '/brightness', _('Unable to read LED State!'))
        return brightness != 0

    @staticmethod
    def setLedState(led, state):
        if isinstance(led, int):
            if led < 0 and led > 15:
                raise ValueError(_('Invalid LED ID'))

            logger.warn(_('Setting LED state via procfs will render sysfs '
                          'LED state information inaccurate (reading and toggling '
                          'state will not work reliably)! '
                          'Access LEDs by name to avoid this problem.'))

            ledState = str(led) + ' ' + \
                ThinkpadAcpi._getProcLedState(led, state)
    
            fileWrite(ThinkpadAcpi.THINKPAD_ACPI_PROC_LED, \
                _('Unable to set LED State!'), str(led) + ' ' + ledState)
        else:
            ledState = ThinkpadAcpi._getSysLedState(led, state)
            if led == 'thinklight' and not ThinkpadAcpi.hasLed(led):
                ThinkpadAcpi.setThinkLightState(ledState)
            else:
                fileWriteBoolean(ThinkpadAcpi._getLedFileName(led) \
                    + '/brightness', _('Unable to set LED State!'), ledState)

    @staticmethod
    def _getLedNameFromFileName(fileName):
        ledName = os.path.basename(fileName)
        ledName = ledName.replace('tpacpi:', '')
        return ledName.lstrip(':')

    @staticmethod
    def _getLedFileName(ledName):
        ledFileName = ThinkpadAcpi.LEDS_BASE + 'tpacpi:'
        if ':' not in ledName:
            ledFileName += ':'
        return ledFileName + ledName

    @staticmethod
    def _getProcLedState(led, state):
        if isinstance(state, bool):
            return 'on' if state else 'off'
        elif state == 'blink':
            return 'blink'
        elif state == None or state == 'toggle':
            logger.warn(_('LED toggle does not work reliably when '
                          'setting value via procfs but reading via sysfs! '
                          'Access LEDs by name to avoid this problem.'))
            return 'on' if not ThinkpadAcpi.getLedState(led) else 'off'
        else:
            raise ValueError(_('Invalid target LED State'))

    @staticmethod
    def _getSysLedState(led, state):
        if isinstance(state, bool):
            return state
        elif state == 'blink':
            raise ValueError(_('Blink Led State not supported via sysfs'))
        elif state == None or state == 'toggle':
            return not ThinkpadAcpi.getLedState(led)
        else:
            raise ValueError(_('Invalid target LED State'))
