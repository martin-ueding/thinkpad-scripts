# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

import logging
import os
import sys

logger = logging.getLogger(__name__)

class Acpi(object):
    '''
    Utility class for interacting with Thinkpad ACPI Extras kernel module.
    '''
    
    THINKPAD_ACPI_SYSFS_BASE = '/sys/devices/platform/thinkpad_acpi/'
    
    # Send CMOS command (rw)
    CMOS_COMMAND = 'cmos_command'
    
    # Whether Bluetooth is enabled (rw)
    BLUETOOTH_ENABLED = 'bluetooth_enable'
    # Whether Radio is On (ro)
    RADIO_SWITCH = 'hotkey_radio_sw'
    # Is Tablet sievel down (ro)
    TABLET_MODE = 'hotkey_tablet_mode'
    
    # All hotkeys enabled mask (ro)
    ALL_MASK = 'hotkey_all_mask'
    # Current hotkeys enabled (rw)
    MASK = 'hotkey_mask'
    # Polling frequency (rw)
    POLL_FREQ = 'hotkey_poll_freq'
    # Recommended hotkeys enabled mask (ro)
    RECOMMENDED_MASK = 'hotkey_recommended_mask'
    # (ro)
    SOURCE_MASK = 'hotkey_source_mask'
    
    @staticmethod
    def sendCmosCommand():
        return Acpi._write(Acpi.CMOS_COMMAND, \
            'Unable to send CMOS Command', data)
    
    @staticmethod
    def hasBluetooth():
        return Acpi._exists(Acpi.BLUETOOTH_ENABLED)
        
    @staticmethod
    def isBluetoothEnabled():
        '''Whether Bluetooth is enabled
        '''
        if not Acpi.hasBluetooth():
            return False
            
        return Acpi._readBoolean(Acpi.BLUETOOTH_ENABLED, \
            'Unable to detect Bluetooth status!')
        
    @staticmethod
    def setBluetoothEnabled(enabled):
        if not Acpi.hasBluetooth():
            return False
        return Acpi._writeBoolean(Acpi.BLUETOOTH_ENABLED, \
            'Unable to set Bluetooth status!', enabled)
    
    @staticmethod
    def hasTabletMode():
        return Acpi._exists(Acpi.TABLET_MODE)

    @staticmethod
    def inTabletMode():
        '''Whether tablet sievel is rotated
        '''
        if not Acpi.hasTabletMode():
            return False            
        return Acpi._readBoolean(Acpi.TABLET_MODE, \
            'Unable to detect Tablet Mode!')
        
    @staticmethod
    def getAllMask():
        return Acpi._readHex(Acpi.ALL_MASK, \
            'Unable to obtain Hotkey All Mask!')
            
    @staticmethod
    def getMask():
        return Acpi._readHex(Acpi.MASK, \
            'Unable to obtain Hotkey Mask!')
            
    @staticmethod
    def setMask(data):
        return Acpi._writeHex(Acpi.MASK, \
            'Unable to obtain Hotkey Mask!', data)
            
    @staticmethod
    def getPollingFrequency():
        return Acpi._readHex(Acpi.POLL_FREQ, \
            'Unable to obtain Polling Frequency!')
            
    @staticmethod
    def setPollingFrequency(data):
        return Acpi._writeHex(Acpi.POLL_FREQ, \
            'Unable to obtain Polling Frequency!', data)
            
    @staticmethod
    def getRecommendedMask():
        return Acpi._readHex(Acpi.RECOMMENDED_MASK, \
            'Unable to obtain Hotkey Recommended Mask!')
            
    @staticmethod
    def getSourceMask():
        return Acpi._readHex(Acpi.SOURCE_MASK, \
            'Unable to obtain Hotkey Source Mask!')
        
    @staticmethod
    def _exists(sysfsFile):
        return os.path.exists(Acpi.THINKPAD_ACPI_SYSFS_BASE + sysfsFile)

    @staticmethod
    def _readBoolean(sysfsFile, errMsg):
        return Acpi._readInt(sysfsFile, errMsg) == 1
        
    @staticmethod
    def _readHex(sysfsFile, errMsg):
        return int(Acpi._read(sysfsFile, errMsg), 16)
        
    @staticmethod
    def _readInt(sysfsFile, errMsg):
        return int(Acpi._read(sysfsFile, errMsg))

    @staticmethod
    def _read(sysfsFile, errMsg):
        try:
            with open(Acpi.THINKPAD_ACPI_SYSFS_BASE + sysfsFile, 'r') as f:
                return f.read().strip()
        except IOError:
            logger.error(errMsg)
            raise
    
    @staticmethod
    def _writeBoolean(sysfsFile, errMsg, data):
        return Acpi._writeInt(sysfsFile, errMsg, 1 if data else 0)
        
    @staticmethod
    def _writeHex(sysfsFile, errMsg, data):
        return Acpi._write(sysfsFile, errMsg, hex(data))
        
    @staticmethod
    def _writeInt(sysfsFile, errMsg, data):
        return Acpi._write(sysfsFile, errMsg, str(data))
    
    @staticmethod
    def _write(sysfsFile, errMsg, data):        
        try:
            with open(Hdaps.HDAPS_SYSFS_BASE + sysfsFile, 'w') as f:
                f.write(str(data))
            return True
        except IOError:
            logger.error(errMsg)
            return False
