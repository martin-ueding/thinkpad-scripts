# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)
#

import os

from tps.sysfs.device import SysDevice


class TpSmapi(SysDevice, dict):

    TP_SMAPI_SYS_BASE = '/sys/devices/platform/smapi/'

    def __init__(self):
        super(TpSmapi, self).__init__(self.TP_SMAPI_SYS_BASE)
        self['BAT0'] = TpSmapiBattery(self._join('BAT0'))
        self['BAT1'] = TpSmapiBattery(self._join('BAT1'))
    
    @property
    def ac_connected(self):
        return self.read_bool('ac_connected')
        
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
            
class TpSmapiBattery(SysDevice):

    @property
    def barcoding(self): return self.read('barcoding')
    
    @property
    def charging_max_current(self): return self.read_int('charging_max_current')
    
    @property
    def charging_max_voltage(self): return self.read_int('charging_max_voltage')
    
    @property
    def chemistry(self): return self.read('chemistry')
    
    @property
    def current_avg(self): return self.read_int('current_avg')
    
    @property
    def current_now(self): return self.read_int('current_now')
    
    @property
    def cycle_count(self): return self.read_int('cycle_count')
    
    @property
    def design_capacity(self): return self.read_int('design_capacity')
    
    @property
    def design_voltage(self): return self.read_int('design_voltage')
    
    #@property
    #def dump(self): return self.read('dump')
    
    @property
    def first_use_date(self): return self.read('first_use_date')
    
    @property
    def force_discharge(self): return self.read('force_discharge')
    
    @force_discharge.setter
    def force_discharge(self, discharge): self.write('force_discharge', discharge)
    
    @property
    def group0_voltage(self): return self.read_int('group0_voltage')
    
    @property
    def group1_voltage(self): return self.read_int('group1_voltage')
    
    @property
    def group2_voltage(self): return self.read_int('group2_voltage')
    
    @property
    def group3_voltage(self): return self.read_int('group3_voltage')
    
    @property
    def inhibit_charge_minutes(self): return self.read_int('inhibit_charge_minutes')
    
    @inhibit_charge_minutes.setter
    def inhibit_charge_minutes(self, min): self.write('inhibit_charge_minutes', min)
    
    @property
    def installed(self): return self.read_bool('installed')
    
    @property
    def last_full_capacity(self): return self.read_int('last_full_capacity')
    
    @property
    def manufacture_date(self): return self.read('manufacture_date')
    
    @property
    def manufacturer(self): return self.read('manufacturer')
    
    @property
    def model(self): return self.read('model')
    
    @property
    def power_avg(self): return self.read_int('power_avg')
    
    @property
    def power_now(self): return self.read_int('power_now')
    
    @property
    def remaining_capacity(self): return self.read_int('remaining_capacity')
    
    @property
    def remaining_charging_time(self): return self.read('remaining_charging_time')
    
    @property
    def remaining_percent(self): return self.read_int('remaining_percent')
    
    @property
    def remaining_percent_error(self): return self.read_int('remaining_percent_error')
    
    @property
    def remaining_running_time(self): return self.read('remaining_running_time')
    
    @property
    def remaining_running_time_now(self): return self.read('remaining_running_time_now')
    
    @property
    def serial(self): return self.read('serial')
    
    @property
    def start_charge_thresh(self): return self.read('start_charge_thresh')
    
    @start_charge_thresh.setter
    def start_charge_thresh(self, level): self.write('start_charge_thresh', level)
    
    @property
    def state(self): return self.read('state')
    
    @property
    def stop_charge_thresh(self): return self.read('stop_charge_thresh')
    
    @stop_charge_thresh.setter
    def stop_charge_thresh(self, level): self.write('stop_charge_thresh', level)

    @property
    def temperature(self): return self.read('temperature')
    
    @property
    def voltage(self): return self.read('voltage')
