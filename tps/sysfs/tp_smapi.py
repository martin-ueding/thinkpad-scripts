# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

from tps.battery import AcAdapterBase, BatteryBase, PowerSourceControllerBase
from tps.cache import cached_property
from tps.sysfs.device import SysDevice
from tps.utils import fileExists


class TpSmapi(SysDevice, PowerSourceControllerBase, dict):

    TP_SMAPI_SYS_BASE = '/sys/devices/platform/smapi'

    def __init__(self):
        super(TpSmapi, self).__init__(self.TP_SMAPI_SYS_BASE)
        PowerSourceControllerBase.__init__(self)
        
    @staticmethod
    def isAvailable():
        return fileExists(TpSmapi.TP_SMAPI_SYS_BASE)
        
    def getAcAdapter(self):
        return self['AC']
        
    def getBatteries(self):
        return [ ps for ps in self.values() if isinstance(ps, TpSmapiBattery) ]
        
    def getPowerSources(self):
        return self.values()
        
    def initPowerSources(self):
        self['AC'] = TpSmapiAcAdapter(self._path)
        self['BAT0'] = TpSmapiBattery(self._join('BAT0'))
        self['BAT1'] = TpSmapiBattery(self._join('BAT1'))
        
    def getStartThreshold(self, batteryId):
        return self._getBattery(batteryId).start_charge_thresh()
    
    def setStartThreshold(self, batteryId, level):
        self._setBatteryAttr(batteryId, 'start_charge_thresh', level)
        
    def getStopThreshold(self, batteryId):
        return self._getBattery(batteryId).stop_charge_thresh()
        
    def setStopThreshold(self, batteryId, level):
        self._setBatteryAttr(batteryId, 'stop_charge_thresh', level)
        
    def getInhibitCharge(self, batteryId):
        min = self._getBattery(batteryId).inhibit_charge_minutes()
        return (min > 0, min)
    
    def setInhibitCharge(self, batteryId, inhibit, min):
        if inhibit and min is None: min = 1
        elif not inhibit: min = 0
        self._setBatteryAttr(batteryId, 'inhibit_charge_minutes', min)
        
    def getForceDischarge(self, batteryId):
        return (self._getBattery(batteryId).force_discharge(), None)
    
    def setForceDischarge(self, batteryId, discharge, acbreak):
        self._setBatteryAttr(batteryId, 'force_discharge', discharge)
        
    def setPeakShiftState(self, inhibit, min):
        raise NotImplementedError('Setting Peak Shift State is not '
            'implemented in tp_smapi driver!')
        
    def _getBattery(batteryId):
        if batteryId not in [ 1, 2 ]:
            raise ValueError('Battery ID must be 1 or 2!')
        return self['BAT' + (batteryId - 1)]
        
    def _setBatteryAttr(self, batteryId, attr, value):
        if batteryId not in [ 0, 1, 2 ]:
            raise ValueError('Battery ID must be one of 0, 1 or 2!')
        if batteryId in [ 1, 0 ] and self['BAT0'].installed:
            setattr(self['BAT0'], attr, value)
        if batteryId in [ 2, 0 ] and self['BAT1'].installed:
            setattr(self['BAT1'], attr, value)
            
class TpSmapiAcAdapter(SysDevice, AcAdapterBase):
    
    @cached_property(ttl=1)
    def state(self):
        return self.readBool('ac_connected')
        
    def isPowerConnected(self):
        return self.state
            
class TpSmapiBattery(SysDevice, BatteryBase):
    
    @cached_property
    def id(self): return int(self.name.replace('BAT', '')) + 1

    @cached_property
    def barcoding(self): return self.read('barcoding')
    
    @cached_property
    def charging_max_current(self): return self.readFloat('charging_max_current', 3)
    
    @cached_property
    def charging_max_voltage(self): return self.readFloat('charging_max_voltage', 3)
    
    @cached_property
    def chemistry(self): return self.read('chemistry')
    
    @cached_property(ttl=1)
    def current_avg(self): return self.readFloat('current_avg', 3)
    
    @cached_property(ttl=1)
    def current_now(self): return self.readFloat('current_now', 3)
    
    @cached_property(ttl=1)
    def cycle_count(self): return self.readInt('cycle_count')
    
    @cached_property
    def design_capacity(self): return self.readFloat('design_capacity', 3)
    
    @cached_property
    def design_voltage(self): return self.readFloat('design_voltage', 3)
    
    #@property
    #def dump(self): return self.read('dump')
    
    @cached_property
    def first_use_date(self): return self.read('first_use_date')
    
    @cached_property(ttl=1)
    def force_discharge(self): return self.read('force_discharge')
    
    @force_discharge.setter
    def force_discharge(self, discharge): self.write('force_discharge', discharge)
    
    @cached_property(ttl=1)
    def group0_voltage(self): return self.readFloat('group0_voltage', 3)
    
    @cached_property(ttl=1)
    def group1_voltage(self): return self.readFloat('group1_voltage', 3)
    
    @cached_property(ttl=1)
    def group2_voltage(self): return self.readFloat('group2_voltage', 3)
    
    @cached_property(ttl=1)
    def group3_voltage(self): return self.readFloat('group3_voltage', 3)
    
    @cached_property(ttl=1)
    def inhibit_charge_minutes(self): return self.readInt('inhibit_charge_minutes')
    
    @inhibit_charge_minutes.setter
    def inhibit_charge_minutes(self, min): self.write('inhibit_charge_minutes', min)
    
    @cached_property(ttl=1)
    def installed(self): return self.readBool('installed')
    
    @cached_property(ttl=1)
    def last_full_capacity(self): return self.readFloat('last_full_capacity', 3)
    
    @cached_property
    def manufacture_date(self): return self.read('manufacture_date')
    
    @cached_property
    def manufacturer(self): return self.read('manufacturer')
    
    @cached_property
    def model(self): return self.read('model')
    
    @cached_property(ttl=1)
    def power_avg(self): return self.readFloat('power_avg', 3)
    
    @cached_property(ttl=1)
    def power_now(self): return self.readFloat('power_now', 3)
    
    @cached_property(ttl=1)
    def remaining_capacity(self): return self.readFloat('remaining_capacity', 3)
    
    @cached_property(ttl=1)
    def remaining_charging_time(self): return self.read('remaining_charging_time')
    
    @cached_property(ttl=1)
    def remaining_percent(self): return self.readInt('remaining_percent')
    
    @cached_property(ttl=1)
    def remaining_percent_error(self): return self.readInt('remaining_percent_error')
    
    @cached_property(ttl=1)
    def remaining_running_time(self): return self.read('remaining_running_time')
    
    @cached_property(ttl=1)
    def remaining_running_time_now(self): return self.read('remaining_running_time_now')
    
    @cached_property
    def serial(self): return self.read('serial')
    
    @cached_property(ttl=1)
    def start_charge_thresh(self): return self.readInt('start_charge_thresh')
    
    @start_charge_thresh.setter
    def start_charge_thresh(self, level): self.write('start_charge_thresh', level)
    
    @cached_property(ttl=1)
    def state(self): return self.read('state')
    
    @cached_property(ttl=1)
    def stop_charge_thresh(self): return self.readInt('stop_charge_thresh')
    
    @stop_charge_thresh.setter
    def stop_charge_thresh(self, level): self.write('stop_charge_thresh', level)

    @cached_property(ttl=1)
    def temperature(self): return self.readFloat('temperature', 3)
    
    @cached_property(ttl=1)
    def voltage(self): return self.readFloat('voltage', 3)
