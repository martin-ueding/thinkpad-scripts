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

class Acpi(object):
    '''
    Utility class for interacting with Thinkpad ACPI Extras kernel module.
    '''
    
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
    
    @staticmethod
    def sendCmosCommand():
        return filewrite(Acpi.CMOS_COMMAND, \
            'Unable to send CMOS Command', data)
    
    @staticmethod
    def hasBluetooth():
        return fileexists(Acpi.BLUETOOTH_ENABLED)
        
    @staticmethod
    def isBluetoothEnabled():
        '''Whether Bluetooth is enabled
        '''
        if not Acpi.hasBluetooth():
            return False
            
        return fileReadBoolean(Acpi.BLUETOOTH_ENABLED, \
            'Unable to detect Bluetooth status!')
        
    @staticmethod
    def setBluetoothEnabled(enabled):
        if not Acpi.hasBluetooth():
            return False
        return fileWriteBoolean(Acpi.BLUETOOTH_ENABLED, \
            'Unable to set Bluetooth status!', enabled)
    
    @staticmethod
    def hasTabletMode():
        return fileExists(Acpi.TABLET_MODE)

    @staticmethod
    def inTabletMode():
        '''Whether tablet sievel is rotated
        '''
        if not Acpi.hasTabletMode():
            return False            
        return fileReadBoolean(Acpi.TABLET_MODE, \
            'Unable to detect Tablet Mode!')
        
    @staticmethod
    def getAllMask():
        return fileReadHex(Acpi.ALL_MASK, \
            'Unable to obtain Hotkey All Mask!')
            
    @staticmethod
    def getMask():
        return fileReadHex(Acpi.MASK, \
            'Unable to obtain Hotkey Mask!')
            
    @staticmethod
    def setMask(data):
        return fileWriteHex(Acpi.MASK, \
            'Unable to obtain Hotkey Mask!', data)
            
    @staticmethod
    def getPollingFrequency():
        return fileReadHex(Acpi.POLL_FREQ, \
            'Unable to obtain Polling Frequency!')
            
    @staticmethod
    def setPollingFrequency(data):
        return fileWriteHex(Acpi.POLL_FREQ, \
            'Unable to obtain Polling Frequency!', data)
            
    @staticmethod
    def getRecommendedMask():
        return fileReadHex(Acpi.RECOMMENDED_MASK, \
            'Unable to obtain Hotkey Recommended Mask!')
            
    @staticmethod
    def getSourceMask():
        return fileReadHex(Acpi.SOURCE_MASK, \
            'Unable to obtain Hotkey Source Mask!')
        

