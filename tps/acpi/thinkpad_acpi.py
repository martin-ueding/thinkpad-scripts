# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

import glob
import logging
import os
import sys

from tps.utils import fileExists, fileRead, fileReadBoolean, \
                      fileReadHex, fileReadInt, fileWrite, \
                      fileWriteBoolean, fileWriteHex, fileWriteInt

'''Interface to thinkpad_acpi kernel module via sysfs under:
/proc/acpi/ibm/
/sys/devices/platform/thinkpad_acpi/
/sys/devices/platform/thinkpad_hwmon/
and additionally:
/sys/devices/platform/dock.*
/sys/class/power_supply/
/sys/class/dmi/id

Info and docs:
https://www.kernel.org/doc/Documentation/laptops/thinkpad-acpi.txt
http://www.thinkwiki.org/wiki/Tablet_Hardware_Buttons
http://www.thinkwiki.org/wiki/Table_of_thinkpad-acpi_LEDs
'''

logger = logging.getLogger(__name__)

class ThinkpadAcpi(object):
    '''Class for interacting with Thinkpad ACPI Extras kernel module.
    '''
    
    POWER_SUPPLY_SYS_GLOB = "/sys/class/power_supply/{BAT0,BAT1,AC,ADP0,ADP1}/device/path"
    
    THINKPAD_ACPI_PROC_BASE = '/proc/acpi/ibm/'
    # beep  bluetooth  cmos  driver  fan  hotkey  led  light  video  volume
    # thermal
    
    THINKPAD_ACPI_PROC_FAN = THINKPAD_ACPI_PROC_BASE + 'fan'
    
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
    
    DOCK_STATIONS = '/sys/devices/platform/dock.*'
    
    GPU_BBSWITCH = '/proc/acpi/bbswitch'
        
    @staticmethod
    def hasFan():
        return fileExists(ThinkpadAcpi.THINKPAD_ACPI_PROC_FAN)
    
    @staticmethod
    def getFanState():
        def getValue(line):
            return line.split(':')[-1].strip()

        status = speed = level = None
        with open(ThinkpadAcpi.THINKPAD_ACPI_PROC_FAN, 'r') as f:
            for line in f:
                if line.startswith('status:'):
                    status = getValue(line)
                if line.startswith('speed:'):
                    speed = int(getValue(line))
                if line.startswith('level:'):
                    level = ThinkpadAcpi.getFanLevelInt(getValue(line))
        return {'status': status,
                'level': level,
                'rpm': speed}
        
    @staticmethod
    def setFanSpeed(speed):
        '''Set fan to specified level:
        0=off, 1-7=normal, 254=disengaged, 255=auto, 256=full-speed
        '''
        fan_state = ThinkpadAcpi.getFanState()
        
        if speed == fan_state['level']:
            logger.debug('Keeping the current fan level unchanged')
        else:
            logger.debug('Setting fan level to ' + str(speed))
            with open(ThinkpadAcpi.THINKPAD_ACPI_PROC_FAN, 'w') as f:
                if speed == 0:
                    f.write('disable')
                else:
                    f.write('enable')
                    f.write('level %s' % \
                        ThinkpadAcpi.getFanLevelStr(speed))
                f.flush()
    
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
            'Unable to send CMOS Command', data)
    
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
            'Unable to detect Bluetooth status!')
        
    @staticmethod
    def setBluetoothEnabled(enabled):
        if not ThinkpadAcpi.hasBluetooth():
            return False
        return fileWriteBoolean(ThinkpadAcpi.BLUETOOTH_ENABLED, \
            'Unable to set Bluetooth status!', enabled)
    
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
            'Unable to detect Tablet Mode!')
        
    @staticmethod
    def getAllMask():
        return fileReadHex(ThinkpadAcpi.ALL_MASK, \
            'Unable to obtain Hotkey All Mask!')
            
    @staticmethod
    def getMask():
        return fileReadHex(ThinkpadAcpi.MASK, \
            'Unable to obtain Hotkey Mask!')
            
    @staticmethod
    def setMask(data):
        return fileWriteHex(ThinkpadAcpi.MASK, \
            'Unable to obtain Hotkey Mask!', data)
            
    @staticmethod
    def getPollingFrequency():
        return fileReadHex(ThinkpadAcpi.POLL_FREQ, \
            'Unable to obtain Polling Frequency!')
            
    @staticmethod
    def setPollingFrequency(data):
        return fileWriteHex(ThinkpadAcpi.POLL_FREQ, \
            'Unable to obtain Polling Frequency!', data)
            
    @staticmethod
    def getRecommendedMask():
        return fileReadHex(ThinkpadAcpi.RECOMMENDED_MASK, \
            'Unable to obtain Hotkey Recommended Mask!')
            
    @staticmethod
    def getSourceMask():
        return fileReadHex(ThinkpadAcpi.SOURCE_MASK, \
            'Unable to obtain Hotkey Source Mask!')
        
    @staticmethod
    def hasBbSwitch():
        return os.path.exists(ThinkpadAcpi.GPU_BBSWITCH)

    @staticmethod
    def getBbSwitchState():
        state = fileRead(ThinkpadAcpi.GPU_BBSWITCH, \
            'Unable to obtain BB Switch State!')
        if state == 'ON':
            return True
        elif state == 'OFF':
            return False
        else:
            raise NameError('Unknown bbswitch state')
            
    @staticmethod
    def isDocked():
        '''
        Determines whether the laptop is on a docking station.

        This checks for ``/sys/devices/platform/dock.*/docked``.

        :returns: True if laptop is docked
        :rtype: bool
        '''
        dockfiles = glob.glob(DOCK_STATIONS)
        for dockfile in dockfiles:
            with open(dockfile) as handle:
                contents = handle.read()
                dock_state = int(contents) == 1
                if dock_state:
                    logger.info('Docking station found.')
                    return True
        logger.info('No docking station found.')
        return False
