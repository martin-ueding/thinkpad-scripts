# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)
#
# Initial implementation comes from:
#     LaptopControlPanel - A Laptop Control Panel 
#     Copyright (C) 2014 Fabrice Salvaire
# The original author has given conscent to use this code within this project.
#

'''
This module provides an interface to ACPI Calls to control Thinkpad Laptop Battery.

These ACPI calls permits:
* to set the start and stop capacity threshold to charge the battery,
* to switch on battery when AC power is plugged,
* to setup a "peak shift" procedure.

(As far I know) The concept of "peak shift" is to switch temporarily electrical devices on battery
during a power peak consumption period so as to unload the grid.  This power management strategy is
relevant for country like Japan, where these peak periods represent a risk of electrical black out.

LPC - Low Pin Count Bus
EC - Embedded Controller
'''

import logging

from tps.acpi.acpicall import AcpiCallDevice, AcpiCallArguments

logger = logging.getLogger(__name__)


class ThinkpadAcpiBatteryController(object):

    _asl_base = r'\_SB.PCI0.LPC.EC.HKEY'

    either_both_battery, main_battery, secondary_battery = list(range(3))

    def __init__(self):

        self._device = AcpiCallDevice()
        
        # Battery Charge Start Threshold

        self._get_charge_start_threshold = self._defineFunction(
            name='BCTG',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              reserved=31,
                                              ),
            output_arguments=AcpiCallArguments(start_threshold=7,
                                               capability=8,
                                               can_specify_every_battery=9,
                                               reserved=30,
                                               error_status=31,
                                               ),
            )

        self._set_charge_start_threshold = self._defineFunction(
            name='BCCS',
            input_arguments=AcpiCallArguments(start_threshold=7,
                                              battery_id=9,
                                              reserved=31,
                                              ),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        # Battery Charge Stop Threshold
        
        self._get_charge_stop_threshold = self._defineFunction(
            name='BCSG',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              reserved=31),
            output_arguments=AcpiCallArguments(stop_threshold=7,
                                               capability=8,
                                               can_specify_every_battery=9,
                                               reserved=30,
                                               error_status=31,
                                               ),
            )

        self._set_charge_stop_threshold = self._defineFunction(
            name='BCSS',
            input_arguments=AcpiCallArguments(stop_threshold=7,
                                              battery_id=9,
                                              reserved=31,
                                              ),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )
            
        # Inhibit Charge
        
        self._set_inhibit_charge_state = self._defineFunction(
            name='BICS',
            input_arguments=AcpiCallArguments(inhibit_charge=0,
                                              reserved1=3,
                                              battery_id=5,
                                              reserved2=7,
                                              timer=23,
                                              reserved3=31,
                                              ),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        # Battery Discharge State (Force Discharge)

        self._get_discharge_state = self._defineFunction(
            name='BDSG',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              reserved=31),
            output_arguments=AcpiCallArguments(discharge_status=0,
                                               break_by_ac_detaching=1,
                                               reserved1=7,
                                               discharge_capability=8,
                                               can_specify_every_battery=9,
                                               can_break=10,
                                               reserved2=30,
                                               error_status=31,
                                               ),
            )

        self._set_discharge_state = self._defineFunction(
            name='BDSS',
            input_arguments=AcpiCallArguments(force_discharge=0,
                                              break_by_ac_detaching=1,
                                              reserved1=7,
                                              battery_id=9,
                                              reserved2=31),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        # Peak Shift State

        self._get_peak_shift_state = self._defineFunction(
            name='PSSG',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              reserved=31),
            output_arguments=AcpiCallArguments(inhibit_charge_status=0,
                                               reserved1=3,
                                               discharge_with_ac_capability=4,
                                               inhibit_charge_capability=5,
                                               inhibit_charge_auto_reset_capability=6,
                                               reserved2=7,
                                               inhibit_charge_effective_timer=23,
                                               reserved3=30,
                                               error_status=31,
                                               ),
            )

        self._set_peak_shift_state = self._defineFunction(
            name='PSSS',
            input_arguments=AcpiCallArguments(inhibit_charge=0,
                                              reserved1=7,
                                              timer=23,
                                              reserved2=31,
                                              ),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        self._set_peak_shift_discharge_state = self._defineFunction(
            name='PSBS',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              discharge_status=15,
                                              reserved=31),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

    def getStartThreshold(self, battery_id=main_battery):
        self._check_battery_id_for_reading(battery_id)
        result = self._get_charge_start_threshold.call(battery_id=battery_id)
        
        if result.capability != 1 and result.can_specify_every_battery != 1:
            raise ValueError("Start charge threshold unsupported!")
        
        return result.start_threshold

    def setStartThreshold(self, battery_id=main_battery, threshold=None):
        threshold = self._check_charge_threshold(threshold)
        result = self._set_charge_start_threshold.call(battery_id=battery_id,
                                                       start_threshold=threshold)
        self._check_error_status(result)
        
    def getStopThreshold(self, battery_id=main_battery):
        self._check_battery_id_for_reading(battery_id)
        result = self._get_charge_stop_threshold.call(battery_id=battery_id)
        
        if result.capability != 1 and result.can_specify_every_battery != 1:
            raise ValueError("Start charge threshold unsupported")
        
        return result.stop_threshold

    def setStopThreshold(self, battery_id=main_battery, threshold=None):
        threshold = self._check_charge_threshold(threshold)
        result = self._set_charge_stop_threshold.call(battery_id=battery_id,
                                                      stop_threshold=threshold)
        self._check_error_status(result)

    def getInhibitCharge(self, battery_id=main_battery):
        '''This is actually reading peak shift state'''
        result = self.getPeakShiftState(battery_id)
        
        if result.inhibit_charge_capability != 1:
            # and result.inhibit_charge_auto_reset_capability != 1
            raise ValueError('Inhibit charge unsupported')
            
        return result

    def setInhibitCharge(self, battery_id=main_battery, inhibit_charge=True, timer=None):
        result = self._set_inhibit_charge_state.call(battery_id=battery_id,
                                                     inhibit_charge=inhibit_charge,
                                                     timer=timer)
        self._check_error_status(result)
    
    def getForceDischarge(self, battery=main_battery):
        self._check_battery_id_for_reading(battery)
        result = self._get_discharge_state.call(battery_id=battery)
        
        if result.discharge_capability != 1 \
            and result.can_specify_every_battery != 1:
            raise ValueError('Force discharge unsupported')
            
        return result
        
    def setForceDischarge(self, battery=main_battery, 
                          force_discharge=True, break_by_ac_detaching=False):
        result = self._set_discharge_state.call(battery_id=battery,
                                                force_discharge=force_discharge,
                                                break_by_ac_detaching=break_by_ac_detaching)
        self._check_error_status(result)
        

    def getPeakShiftState(self, battery_id=main_battery):
        return self._get_peak_shift_state.call(battery_id=battery_id)
        
    def setPeakShiftState(self, inhibit_charge=True, timer=None):
        result = self._set_peak_shift_state.call(inhibit_charge=inhibit_charge,
                                                 timer=timer)
        self._check_error_status(result)
    
    def setPeakShiftDischargeState(self, battery_id=main_battery, discharge_status=None):
        result = self._set_peak_shift_discharge_state.call(inhibit_charge=inhibit_charge,
                                                           discharge_status=discharge_status)
        self._check_error_status(result)
        
    def _defineFunction(self, name, input_arguments, output_arguments):
        return self._device.defineFunction(self._asl_base + '.' + name,
                                           input_arguments, output_arguments)

    def _check_battery_id_for_reading(self, battery):
        if battery == self.either_both_battery:
            raise ValueError("Can't specify either or both battery for reading.")

    def _check_charge_threshold(self, threshold=None):
        if threshold is None:
            threshold = 0
        elif not (0 <= threshold <= 99):
            raise ValueError("Wrong charge threshold value " + str(threshold))
        return str(threshold)

    def _check_error_status(self, result):
        if result.error_status:
            raise ValueError("ACPI call failed! Error status: %s" % str(result.error_status))
