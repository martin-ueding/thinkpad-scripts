# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)
#
# Initial implementation comes from:
#     LaptopControlPanel - A Laptop Control Panel 
#     Copyright (C) 2014 Fabrice Salvaire
# The original author has given conscent to use this code within this project.
#

import logging
import string

from tps.utils import fileExists, fileRead, fileWrite, \
                      DictInitialised

logger = logging.getLogger(__name__)


class AcpiCallDevice(object):
    '''
    You can pass parameters to acpi_call by writing them after the 
    method, separated by single space. Currently, you can pass the 
    following parameter types:

    ACPI_INTEGER - by writing NNN or 0xNNN, where NNN is an integer/hex
    ACPI_STRING - by enclosing the string in quotes: "hello, world"
    ACPI_BUFFER - by writing bXXXX, where XXXX is a hex string without 
                  spaces, or by writing { b1, b2, b3, b4 }, where 
                  b1-4 are integers

    The status after a call can be read back from /proc/acpi/call:

    'not called' - nothing to report
    'Error: ' - the call failed
    '0xNN' - the call succeeded, and returned an integer
    '"..."' - the call succeeded, and returned a string
    '{0xNN, ...}' - the call succeeded, and returned a buffer
    '[...]' - the call succeeded, and returned a package which may 
              contain the above types (integer, string and buffer) 
              and other package types

    @source: https://github.com/mkottman/acpi_call
    @requires: acpi-call-dkms system package
    '''

    ACPI_CALL = '/proc/acpi/call'

    def __init__(self):
        if not AcpiCallDevice.isAvailable():
            logger.error("Could not find %s. Is module acpi_call loaded?" % AcpiCallDevice.ACPI_CALL)
            
    @staticmethod
    def isAvailable():
        return fileExists(AcpiCallDevice.ACPI_CALL)

    def call(self, asl_base, *args):
        call_request = self.encodeCallRequest(asl_base, args)
        
        logger.debug("Call ACPI Function '%s'" % call_request)
        
        if not fileWrite(AcpiCallDevice.ACPI_CALL, \
            'Unable to send ACPI CALL request!', call_request):
            return False
        
        call_result = fileRead(AcpiCallDevice.ACPI_CALL, \
            'Unable to read ACPI CALL result!')

        logger.debug("Call returned '%s'" % call_result)

        # it appears that the buffer is initialized with 'not called'
        # the command response is a null terminaed string
        call_result = call_result.split('\x00')[0]
        
        if self.checkCallError(asl_base, args, call_result):
            return False

        return self.parseCallResponse(asl_base, args, call_result)
    
    def encodeCallRequest(self, asl_base, call_args):
        call_request = asl_base + ' '
        if len(call_args) > 1:
            onCallError(asl_base, call_args, None, 'ACPI Call encoding '
                        'multiple request parameters is unsupported: %s' % call_args)
        for arg in call_args:
            if isinstance(arg, int):
                call_request += hex(arg)
            elif isinstance(arg, str) and arg.startswith('0x'):
                call_request += arg
            elif isinstance(arg, str):
                call_request += '"' + arg + '"'
            else:
            #elif isinstance(arg, (list, tuple)):
                onCallError(asl_base, call_args, None, 'ACPI Call Unknown '
                        'request argument format: %s' % arg)
        return call_request
        
    def parseCallResponse(self, asl_base, call_args, call_result):
        if call_result is None or call_result == '':
            return call_result
        elif call_result.startswith('0x'):
            return int(call_result, 16)
        elif call_result.startswith(tuple(string.digits)):
            return int(call_result)
        elif call_result.startswith('"') and call_result.endswith('"'):
            return call_result[1:-1]
        elif call_result.startswith('{') and call_result.endswith('}'):
            result_parts = call_result.strip('{} ').replace(' ', ',').split(',')
            result = []
            # yupp, this is baaaad
            for result_part in result_parts:
                result.append(self.parseCallResponse(asl_base, call_args, result_part))
            return result
        elif call_result.startswith('[') and call_result.endswith(']'):
            logger.error('ACPI Call Package type response parsing is '
                         'not yet supported for: %s' % call_result)
            return call_result
        else:
            onCallError(asl_base, call_args, call_result, 'ACPI Call Unknown '
                        'result format: %s' % call_result)

    def checkCallError(self, asl_base, call_args, call_result):
        error_msg = None
        if call_result == 'not called':
            error_msg = 'ACPI Call failed due to missing query: %s' % call_result
        elif call_result == '0x80000000':
            error_msg = 'ACPI Call failure status returned: %s' % call_result
        elif call_result.startswith('Error: AE_NOT_FOUND'):
            error_msg = 'ACPI Call failed: ASL base not found for this ' \
                        'machine: %s' % asl_base
        elif call_result.startswith('Error: '):
            error_msg = 'ACPI Call error response: %s' % call_result
        if error_msg:
            self.onCallError(asl_base, call_args, call_result, error_msg)
            return True
        return False
        
    def onCallError(self, asl_base, call_args, call_result, error_msg):
        '''Default Error hanlder'''
        logger.error(error_msg)
        raise ValueError(error_msg)

    def defineFunction(self, name, input_arguments, output_arguments):
        return AcpiCallFunction(self, name, input_arguments, output_arguments)

class AcpiCallFunction(object):

    def __init__(self, acpi_call_device, acpi_path, input_arguments, output_arguments):
        self._acpi_call_device = acpi_call_device
        self._acpi_path = acpi_path
        self._input_arguments = input_arguments
        self._output_arguments = output_arguments

    def call(self, **kwargs):
        double_word = self._input_arguments.encode(**kwargs)
        double_word = self._acpi_call_device.call(self._acpi_path, double_word)
        return self._output_arguments.decode(double_word)

class AcpiCallArguments(object):

    def __init__(self, **kwargs):
        items = sorted(list(kwargs.items()), key=lambda a: a[1])
        self._arguments = []
        lower_bit = 0
        for argument_name, upper_bit in items:
            self._arguments.append(AcpiCallArgument(argument_name, upper_bit, lower_bit))
            lower_bit = upper_bit + 1
        self._argument_names = [argument.name for argument in self._arguments]

    def encode(self, **kwargs):
        for given_argument in kwargs:
            if given_argument not in self._argument_names:
                raise ValueError("Wrong argument %s" % (given_argument))
        double_word = 0
        for argument in self._arguments:
            if argument.name in kwargs:
                value = kwargs[argument.name]
            else:
                value = 0
            double_word += argument.encode(value)
        return double_word

    def decode(self, double_word):
        values = {}
        for argument in self._arguments:
            value = argument.decode(double_word)
            if argument.name.startswith('reserved'):
                if value != 0:
                    raise ValueError("Reserved %s bits are non-zero %u" % (argument.name, value))
            else:
                values[argument.name] = value
        logger.debug(str(values))
        return DictInitialised(**values)

class AcpiCallArgument(object):

    def __init__(self, name, upper_bit, lower_bit):        
        self.name = name
        self.upper_bit = upper_bit
        self.lower_bit = lower_bit
        self.number_of_bits = upper_bit - lower_bit +1

    def _check_value(self, value):
        if self.number_of_bits == 1:
            value= bool(value)
        value = int(value)
        if value >= 2**self.number_of_bits:
            raise ValueError("Out of range")
        return value

    def encode(self, value):
        return self._check_value(value) << self.lower_bit

    def decode(self, double_word):
        value = (double_word >> self.lower_bit) & (2**self.number_of_bits -1)
        if self.number_of_bits == 1:
            return bool(value)
        else:
            return value
