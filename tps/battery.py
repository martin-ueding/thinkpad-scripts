# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)

from abc import ABCMeta, abstractmethod as abstract
import logging


logger = logging.getLogger(__name__)

class PowerSourceBase(object):
    pass

class AcAdapterBase(PowerSourceBase):
    
    __metaclass__ = ABCMeta
    
    @abstract
    def isPowerConnected(self): pass

class BatteryBase(PowerSourceBase):
    
    __metaclass__ = ABCMeta
    
    @property
    @abstract
    def id(self): pass
    
    @property
    @abstract
    def installed(self): pass
    
    @property
    @abstract
    def state(self): pass
        
    @property
    @abstract
    def remaining_percent(self): pass
        
    @property
    @abstract
    def power_avg(self): pass
    
    @property
    @abstract
    def power_now(self): pass
    
    @property
    @abstract
    def remaining_capacity(self): pass
    
    @property
    @abstract
    def last_full_capacity(self): pass
        
    @property
    @abstract
    def design_capacity(self): pass
        
    @property
    @abstract
    def force_discharge(self): pass
        
    @property
    @abstract
    def inhibit_charge_minutes(self): pass
    
    @abstract
    def isInstalled(self):
        return self.installed
    
    @abstract
    def isCharging(self):
        return self.state is not None and self.state.lower() == 'charging'

    @abstract
    def isDischarging(self):
        return self.state is not None and self.state.lower() == 'discharging'

class PowerSourceInfoBase(object):
    '''Interface for all system power sources'''
    
    __metaclass__ = ABCMeta
    
    def __init__(self):
        super(PowerSourceInfoBase, self).__init__()
        self.initPowerSources()
        
    @staticmethod
    @abstract
    def isAvailable(self):
        '''Check if Power Source backend is available and operational'''
        pass
    
    @abstract
    def initPowerSources(self):
        '''Initialize power sources'''
        pass
    
    @abstract
    def getAcAdapter(self):
        '''Should return an AcAdapterBase object'''
        pass
    
    @abstract
    def getBatteries(self):
        '''Should return a list of installed BatteryBase objects'''
        pass
        
    @abstract
    def getPowerSources(self):
        '''Should return a list of all installed power sources 
        i.e. AcBase and BatteryBase objects
        '''
        pass
    
    @abstract
    def isAnyBatteryInstalled(self):
        for battery in self.getBatteries():
            if battery.isInstalled():
                return True
        return False

    @abstract
    def isAnyBatteryCharging(self):
        for battery in self.getBatteries():
            if battery.isCharging():
                return True
        return False
    
    @abstract
    def isAnyBatteryDischarging(self):
        for battery in self.getBatteries():
            if battery.isDischarging():
                return True
        return False
    
    @abstract
    def getBatteryCapacityTotalRemaining(self):
        '''Battery capacity total remaining [%]'''
        remaining = 0
        lastFull = 0
        for battery in self.getBatteries():
            remaining += int(float(battery.remaining_capacity))
            lastFull += int(float(battery.last_full_capacity))
        if lastFull == 0:
            return 0
        return int(100 * (float(remaining) / float(lastFull)))
    
    @abstract
    def getSystemAveragePowerConsumption(self):
        '''Only accurate when system is on battery power'''
        for battery in self.getBatteries():
            if battery.isDischarging():
                return battery.power_avg
    
    @abstract
    def getSystemCurrentPowerConsumption(self):
        '''Only accurate when system is on battery power'''
        for battery in self.getBatteries():
            if battery.isDischarging():
                return battery.power_now
    
class BatteryControllerBase(object):
    
    __metaclass__ = ABCMeta
    
    @staticmethod
    @abstract
    def isAvailable(self):
        '''Check if Power Source backend is available and operational'''
        pass
    
    @abstract
    def getStartThreshold(self, batteryId): pass
    
    @abstract
    def setStartThreshold(self, batteryId, level): pass
    
    @abstract
    def getStopThreshold(self, batteryId): pass
    
    @abstract
    def setStopThreshold(self, batteryId, level): pass
    
    @abstract
    def getInhibitCharge(self, batteryId): pass
    
    @abstract
    def setInhibitCharge(self, batteryId, inhibit, min): pass
    
    @abstract
    def getForceDischarge(self, batteryId): pass
    
    @abstract
    def setForceDischarge(self, batteryId, discharge, acBreak): pass
    
    @abstract
    def setPeakShiftState(self, inhibit, min): pass
    
    @abstract
    def isForcedDischarge(self, batteryId):
        (dischargeStatus, acBreak) = self.getForceDischarge(batteryId)
        return dischargeStatus
    
    @abstract
    def isChargeInhibited(self, batteryId):
        (inhibitStatus, min) = self.getInhibitCharge(batteryId)
        return inhibitStatus
    
    @abstract
    def balanceCharge(self, config, batteryStatus, chargeStrategy, dischargeStrategy):
        '''Initial implementation taken from TPBattStat by Eliot Wolk'''
        
        batteries = batteryStatus.getBatteries()
        if len(batteries) != 2:
            logger.error('You need two batteries present in your '
                         'system to balance charge!')
            return False
        
        (bat1, bat2) = batteries
        if not bat1.isInstalled() or not bat2.isInstalled():
            logger.error('You need two batteries present in your '
                         'system to balance charge!')
            return False
        
        ac = batteryStatus.getAcAdapter()
        
        # TODO: incorporate start/stop thresholds into the algorithm
        #bat1Start = self.getStartThreshold(bat1.id)
        #bat1Stop = self.getStopThreshold(bat1.id)
        bat1Charge = bat1.remaining_percent
        
        #bat2Start = self.getStartThreshold(bat2.id)
        #bat2Stop = self.getStopThreshold(bat2.id)
        bat2Charge = bat2.remaining_percent
        
        # charge inhibition
        
        should_not_inhibit = (
            not ac.isACConnected() or
            not bat1.isInstalled() or
            not bat2.isInstalled())
        
        if should_not_inhibit or chargeStrategy == 'system':
            if self.getInhibitCharge(bat1.id):
                self.setInhibitCharge(bat1.id, False)
            if self.getInhibitCharge(bat2.id):
                self.setInhibitCharge(bat2.id, False)
        elif chargeStrategy == 'leapfrog':
            threshold = self._config['battery']['charge_leapfrog_threshold']
            if bat2Charge - bat1Charge > threshold:
                self._ensureCharging(bat1, bat2, bat2.id)
            elif bat1Charge - bat2Charge > threshold:
                self._ensureCharging(bat1, bat2, bat1.id)
        elif chargeStrategy == 'chasing':
            if bat2Charge > bat1Charge:
                self._ensureCharging(bat1, bat2, bat1.id)
            elif bat1Charge > bat2Charge:
                self._ensureCharging(bat1, bat2, bat2.id)
        elif chargeStrategy == 'brackets':
            prefBat = bat1 if bat1.id == self._config['battery']\
                ['charge_brackets_preferred_battery'] else bat2
            unprefBat = bat1 if prefBat.id == bat2.id else bat2
            percentPref = bat1Charge if prefBat.id == bat1.id else bat2Charge
            percentUnpref = bat1Charge if unprefBat.id == bat1.id else bat2Charge
            for bracket in self._config['battery']['charge_brackets']:
                if percentPref < bracket:
                    self._ensureCharging(bat1, bat2, prefBat)
                    break
                elif percentUnpref < bracket:
                    self._ensureCharging(bat1, bat2, unprefBat)
                    break
        
        # forced discharge
        
        forceDischarge1 = False
        forceDischarge2 = False
        should_force = (
            not ac.isACConnected() and
            bat1.isInstalled() and
            bat2.isInstalled())
        
        if not should_force or dischargeStrategy == 'system':
            forceDischarge1 = False
            forceDischarge2 = False
        elif dischargeStrategy == 'leapfrog':
            leapfrogThreshold = \
                self._config['battery']['discharge_leapfrog_threshold']
            if bat1.isDischarging():
                if bat2Charge - bat1Charge > leapfrogThreshold:
                    forceDischarge2 = True
                elif bat1Charge > leapfrogThreshold:
                    forceDischarge1 = True
            elif bat2.isDischarging():
                if bat1Charge - bat2Charge > leapfrogThreshold:
                    forceDischarge1 = True
                elif bat2Charge > leapfrogThreshold:
                    forceDischarge2 = True
            elif bat1Charge > leapfrogThreshold and bat1Charge > bat2Charge:
                forceDischarge1 = True
            elif bat2Charge > leapfrogThreshold and bat2Charge > bat1Charge:
                forceDischarge2 = True
        elif dischargeStrategy == 'chasing':
            if bat1Charge > bat2Charge:
                forceDischarge1 = True
            elif bat2Charge > bat1Charge:
                forceDischarge2 = True

        if self.getForceDischarge(bat1.id) != forceDischarge1 or \
            self.getForceDischarge(bat2.id) != forceDischarge2:
            self.setForceDischarge(bat1.id, forceDischarge1)
            self.setForceDischarge(bat2.id, forceDischarge2)
        
    def _ensureCharging(self, bat1, bat2, batteryId):
        bat1Inhibit = self.getInhibitCharge(bat1.id)
        bat2Inhibit = self.getInhibitCharge(bat2.id)
        if batteryId == bat1.id and (bat1Inhibit or \
            (not bat1.isCharging() and not bat2Inhibit)):
            self.setInhibitCharge(bat1.id, False)
            self.setInhibitCharge(bat2.id, True)
        elif batteryId == bat2.id and (bat2Inhibit or \
            (not bat2.isCharging() and not bat1Inhibit)):
            self.setInhibitCharge(bat1.id, True)
            self.setInhibitCharge(bat2.id, False)
            

class PowerSourceControllerBase(PowerSourceInfoBase, BatteryControllerBase):
    '''Power source info and control'''
    pass
