# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)
#
# Initial implementation comes from:
#     LaptopControlPanel - A Laptop Control Panel 
#     Copyright (C) 2014 Fabrice Salvaire
# The original author has given conscent to use this code within this project.
#

import re

from tps.battery import AcAdapterBase, BatteryBase, PowerSourceInfoBase
from tps.cache import cached_property
from tps.sysfs.device import SysDevice
from tps.utils import fileExists


class PowerSource(SysDevice):

    def __init__(self, path):
        super(PowerSource, self).__init__(path)
        self._type = self.read('type')
        self._device_path = self.read('device/path')

    @cached_property
    def type(self): return self._type

    @cached_property
    def device_path(self): return self._device_path

class AcAdapter(PowerSource, AcAdapterBase):

    @cached_property(ttl=1)
    def state(self): return self.readBool('online')
    
    def isPowerConnected(self):
        return self.state

class Battery(PowerSource, BatteryBase):
    
    @cached_property
    def id(self): return int(self.name.replace('BAT', '')) + 1
    
    @cached_property(ttl=1)
    def installed(self): return self.readBool('present')
    
    @cached_property(ttl=1)
    def state(self): return self.read('status')

    @cached_property
    def technology(self): return self.read('technology')

    @cached_property(ttl=1)
    def cycle_count(self): return self.readInt('cycle_count')

    @cached_property
    def voltage_min_design(self): 
        return self.readFloat('voltage_min_design', 6)

    @cached_property(ttl=1)
    def voltage_now(self): 
        return self.readFloat('voltage_now', 6)
    
    @cached_property(ttl=1)
    def remaining_percent(self):
        return int(100.0 * self.remaining_capacity / self.last_full_capacity)
        
    @cached_property(ttl=1)
    def power_avg(self):
        if self.power_now is not None and self.voltage_now is not None:
            rate = self.power_now
            if self.isDischarging() and rate > 0:
                rate *= -1
            return int(self.voltage_now * rate)
        return None
    
    @cached_property(ttl=1)
    def power_now(self):
        return self.readCharge('current_now', 'power_now')
    
    @cached_property(ttl=1)
    def remaining_capacity(self):
        return self.readCharge('charge_now', 'energy_now')
    
    @cached_property(ttl=1)
    def last_full_capacity(self):
        return self.readCharge('charge_full', 'energy_full')
        
    @cached_property
    def design_capacity(self):
        return self.readCharge('charge_full_design', 'energy_full_design')
    
    @cached_property(ttl=1)
    def capacity(self): return self.readInt('capacity')

    @cached_property
    def model_name(self): return self.read('model_name')

    @cached_property
    def manufacturer(self): return self.read('manufacturer')

    @cached_property
    def serial_number(self): return self.read('serial_number')
        
    @property
    def force_discharge(self): return NotImplemented
    
    @property
    def inhibit_charge_minutes(self): return NotImplemented

    def readCharge(self, chargeField, energyField):
        '''
        Contains a workaround for lenovo's firmware which names files 
        energy_* when booted from battery, and charge_* when booted 
        with AC power connected.
        '''
        if self.exists(chargeField):
            return self.readFloat(chargeField, 6)
        return self.readFloat(energyField, 6)# / self.voltage_now

class PowerSourceInfo(SysDevice, PowerSourceInfoBase, dict):

    POWER_SUPPLY_SYS_BASE = '/sys/class/power_supply'
    
    def __init__(self):
        super(PowerSourceInfo, self).__init__(PowerSourceInfo.POWER_SUPPLY_SYS_BASE)
        PowerSourceInfoBase.__init__(self)
    
    @staticmethod
    def isAvailable():
        return fileExists(PowerSourceInfo.POWER_SUPPLY_SYS_BASE)
        
    def getAcAdapter(self):
        for ps in self.values():
            if isinstance(ps, AcAdaper):
                return ps
        return None
        
    def getBatteries(self):
        return [ ps for ps in self.values() if isinstance(ps, Battery) ]
        
    def getPowerSources(self):
        return self.values()
        
    def initPowerSources(self):
        for fileName in self.list():
            path = self._join(fileName)
            if fileName == 'AC' or fileName.startswith('ADP'):
                power_source = AcAdapter(path)
            else:
                power_source = Battery(path)
            self[power_source.name] = power_source

class AcAdapterLegacy(SysDevice, AcAdapterBase):

    @cached_property(ttl=1)
    def state(self): return self.read('status')
    
    def isPowerConnected(self):
        return 'on-line' in self.state
        
class BatteryLegacy(SysDevice, BatteryBase):
    
    @cached_property
    def id(self): return int(self.name.replace('BAT', '')) + 1
    
    @cached_property(ttl=1)
    def installed(self):
        return self.info('present') == 'yes'
    
    @cached_property(ttl=1)
    def state(self): return self.info('charging state')
    
    @cached_property(ttl=1)
    def voltage_now(self):
        voltValUnit = self._extractValueAndUnit(self.info('present voltage'))
        if voltValUnit == None or voltValUnit[1] != 'mV':
            return None
        return self.roundFloat(voltValUnit[0], 3)
        
    @cached_property(ttl=1)
    def remaining_percent(self):
        if self.remaining_capacity > 0 and self.last_full_capacity > 0:
            return int(self.remaining_capacity / self.last_full_capacity * 100.0)
        else:
            return 0 if self.remaining_capacity is not None else None
        
    @cached_property(ttl=1)
    def power_avg(self):
        if self.voltage_now is not None and self.power_now is not None:
            rate = self.power_now
            if self.isDischarging() and rate > 0:
                rate *= -1
            return int(self.voltage_now * rate)
        return None
    
    @cached_property(ttl=1)
    def power_now(self):
        return self._extractCurrent(self.info('present rate'))
    
    @cached_property(ttl=1)
    def remaining_capacity(self): 
        return self._extractCurrent(self.info('remaining capacity'))
    
    @cached_property(ttl=1)
    def last_full_capacity(self):
        return self._extractCurrent(self.info('last full capacity'))
        
    @cached_property
    def design_capacity(self):
        return self._extractCurrent(self.info('design capacity'))
    
    @cached_property
    def technology(self): return self.info('battery type')
    
    @cached_property
    def model_name(self): return self.info('model number')

    @cached_property
    def manufacturer(self): return self.info('OEM info')

    @cached_property
    def serial_number(self): return self.info('serial number')
        
    @property
    def force_discharge(self): return NotImplemented
    
    @property
    def inhibit_charge_minutes(self): return NotImplemented
        
    @cached_property(ttl=1)
    def _info(self):
        info = dict()
        info.update(self.read('state'))
        info.update(self.read('info'))
        return info
        
    def info(self, name, default=None):
        return self._info.get(name, default)
        
    def read(self, fileName):
        '''Returns a dictionary of key->value pairs.
        Processing output similar to:        
        state:
        present:                 yes
        capacity state:          ok
        charging state:          discharging
        present rate:            unknown
        remaining capacity:      3920 mAh
        present voltage:         14800 mV
        
        info:
        present:                 yes
        design capacity:         3920 mAh
        last full capacity:      3920 mAh
        battery technology:      rechargeable
        design voltage:          14800 mV
        design capacity warning: 30 mAh
        design capacity low:     20 mAh
        capacity granularity 1:  10 mAh
        capacity granularity 2:  3470 mAh
        model number:            Bat0
        serial number:              
        battery type:            Lion
        OEM info:                Acer
        '''
        d = dict()
        keyValRe = re.compile('([a-zA-Z0-9 ]+):\s*([a-zA-Z0-9 ]+)')
        for line in super(fileName).splitlines():
            m = keyValRe.match(line)
            if m != None:
                d[m.group(1)] = m.group(2)
        return d
      
    def _extractCurrent(self, value):
        valUnit = self._extractValueAndUnit(value)
        if valUnit == None:
            return None
        (val, unit) = valUnit
        if unit == 'mAh' or unit == 'mA':
            return val
        elif unit == 'mWh' or unit == 'mW':
            if self.voltage_now is not None:
                return int(val / self.voltage_now)
        return None
    
    def _extractValueAndUnit(self, s):
        m = re.compile('(\d+)\s*([a-zA-Z]*)').match(s)
        if m != None:
            return [int(m.group(1)), m.group(2)]
        return None

class PowerSourceInfoLegacy(SysDevice, PowerSourceInfoBase, dict):
    
    POWER_SUPPLY_PROC_BASE = '/proc/acpi/'
    
    POWER_SUPPLY_BATTERY_PROC_BASE = POWER_SUPPLY_PROC_BASE + 'battery/'
    
    def __init__(self):
        super(PowerSourceInfoLegacy, self).__init__(PowerSourceInfo.POWER_SUPPLY_BATTERY_PROC_BASE)
        PowerSourceInfoBase.__init__(self)
    
    @staticmethod
    def isAvailable():
        return fileExists(PowerSourceInfoLegacy.POWER_SUPPLY_BATTERY_PROC_BASE)
        
    def getAcAdapter(self):
        return self['AC']
        
    def getBatteries(self):
        return [ ps for ps in self.values() if isinstance(ps, BatteryLegacy) ]
        
    def getPowerSources(self):
        return self.values()

    def initPowerSources(self):
        self['AC'] = AcAdapterLegacy(self._join(POWER_SUPPLY_PROC_BASE, \
            'ac_adapter', 'AC'))
        for fileName in self.list():
            battery = BatteryLegacy(self._join(fileName))
            self[battery.name] = battery
