# -*- coding: utf-8 -*-

# Copyright © 2016 Lukasz Czuja <pub@czuja.pl>
# Licensed under The GNU Public License Version 2 (or later)
#
# Initial implementation comes from:
#     LaptopControlPanel - A Laptop Control Panel 
#     Copyright (C) 2014 Fabrice Salvaire
# The original author has given conscent to use this code within this project.
#

import os


class ProcFile(object):

    @staticmethod
    def compile_format_list(format_list):
        format_list = list(format_list)
        if not isinstance(format_list[0], str):
            format_list = [''] + format_list
        if not isinstance(format_list[-1], str):
            format_list = format_list + ['']
        separator = True
        for item in format_list:
            if separator:
                if not isinstance(item, str):
                    raise ValueError("A separator string is expected " + str(item))
            elif isinstance(item, tuple) and len(item) == 2:
                field_name, field_type = item
                if not isinstance(field_name, str):
                    raise ValueError("A string is expected " + str(item))
                if not isinstance(field_type, type):
                    raise ValueError("A type is expected " + str(item))
            else:
                raise ValueError("A 2-tuple is expected " + str(item))
            separator = not separator

        # check separator is not '', field_name is uniq

        return format_list

    @staticmethod
    def join(arg1, **args):
        return os.path.join('/proc', arg1, **args)

    @staticmethod
    def parse_line(compiled_format_list, line):
        first_separator = compiled_format_list[0]
        if line.startswith(first_separator):
            line = line[len(first_separator):]
        else:
            raise ValueError()

        number_of_fields = len(compiled_format_list)/2 # +1 doesn't matter

        fields = {}
        for i in range(number_of_fields):
            index = 2*i +1
            field_tuple, separator = compiled_format_list[index:index+2]
            field_name, field_type = field_tuple
            if separator:
                separator_location = line.find(separator)
                if not separator_location: # must be > 0
                    raise ValueError()
            else:
                separator_location = None
            field_text = line[:separator_location]
            fields[field_name] = field_type(field_text)
            if separator_location:
                line = line[separator_location + len(separator):]

        return fields

class ProcOneLineFile(ProcFile):

    __format_list__= ()
    __file_name__ = None

    def __init__(self):
        self._path = self.join(self.__file_name__)
        self._compiled_format_list = self.compile_format_list(self.__format_list__)
        self._state = None

    def __getattr__(self, key):
        return self._state[key]

    def update(self):
        with open(self._path, 'r') as f:
            line = f.readline().rstrip()
        self._state = self.parse_line(self._compiled_format_list, line)

class LoadAverage(ProcOneLineFile):

    __file_name__ = 'loadavg'
    __format_list__= (('number_of_job_1_min', float), ' ',
                      ('number_of_job_5_min', float), ' ',
                      ('number_of_job_15_min', float), ' ',
                      ('number_of_runnable_entities', int), '/',
                      ('number_of_job_entities', int), ' ',
                      ('last_pid', int))

