# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

import logging
import os
import sys

from tps.utils import fileExists, fileRead, fileReadBoolean, \
                      fileReadHex, fileReadInt, fileWrite, \
                      fileWriteBoolean, fileWriteHex, fileWriteInt

'''
http://www.thinkwiki.org/wiki/Tablet_Hardware_Buttons
'''

logger = logging.getLogger(__name__)

class ThinkpadAcpi(object):
    '''
    Utility class for interacting with Thinkpad ACPI Extras kernel module.
    
    #/sys/bus/platform/drivers/thinkpad_hwmon/
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
                    speed = int(getVaue(line))
                if line.startswith('level:'):
                    # level is 0-7, auto, disengaged, full-speed
                    level = getValue(line)
        return (status, speed, level)
    
    @staticmethod
    def sendCmosCommand():
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
